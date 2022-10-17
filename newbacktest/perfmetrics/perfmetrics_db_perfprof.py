# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.multiprocessor import MultiProcessor
from file_hierarchy import DirPaths, FileNames
from newbacktest.abstractclasses.db_abstract import AbstractDatabase
from newbacktest.perfmetrics.perfmetrics_db_funcprofile import PerfMetricFunctionDatabase
from newbacktest.perfmetrics.winnerloser.winnerlosergenerator import WinLoseGenerator
from newbacktest.perfmetrics.winnerloser.db_wlprofile import WinLoseProfDatabase
from newbacktest.portfolios.db_portfolio import PortfolioDatabase
from newbacktest.symbology.sampcode import SampCode
from newbacktest.symbology.investplancode import InvestPlanCode


class PerfProfileLib(AbstractDatabase):
    '''
    The Performance Profile Library contains all available performance profiles in a list, readily available to create a dataframe.
    A performance profile is summary of a sampcode's underlying portfolio performance.
    db structure = [
        {'sampcode': <sampcode>, 'periodlen': <periodlen>, ...},
        {'sampcode': <sampcode>, 'periodlen': <periodlen>, ...},
        ...
    ]
    '''

    _emptydb = []

    def __init__(self):
        self._dbname = "Performance Profile Library"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_perfprofilelib
        self._item_term = "Performance Profile"

    def view_item(self, term):
        pass

    def add_item(self, item):
        pass

    def _get_perfmetricval(self, perfprofile, perfmetricname):
        perfmetricfunc = PerfMetricFunctionDatabase().metricfuncname_to_metricfuncobj(perfmetricname)
        perfmetricargs = PerfMetricFunctionDatabase().get_metricfuncargdict(perfmetricname, perfprofile)
        return perfmetricfunc(**perfmetricargs)

    def _sync_single(self, perfmetricnames, perfprofile):
        u = {m: self._get_perfmetricval(perfprofile, m) for m in perfmetricnames if m not in perfprofile}
        if u:
            print(f'{u}\nadded to profile\n"{perfprofile["sampcode"]}"\n')
        else:
            print(f'Profile\n"{perfprofile["sampcode"]}"\nalready up-to-date.\n')
        perfprofile.update(u)
        return perfprofile

    def generate_wlpools(self, perfmetricnames, allsampcodes):
        '''wlpools are specific to periodlen and startdates
        perfprofiles are specific to samples which are specific to startdates and periodlen
        since the purpose of this is to gather wlpools to calc winlose metric, the only relevant wlpools are the ones that share the same startdate and periodlens.  Therefore, generate wlpools for sampcode dates whose periodlens match those of each winlose metric to be calculated.
        '''
        listofwlprofcodes = [m for m in perfmetricnames if m.startswith('WLP')]
        if not listofwlprofcodes:
            return
        # get all periodlens from all sampcodes
        startdates_byperiodlen = {}
        for sampcode in allsampcodes:
            scobj = SampCode().decode(sampcode)
            ipobj = InvestPlanCode().decode(scobj['ipcode'])
            p = ipobj['periodlen']
            startdates_byperiodlen[p] = startdates_byperiodlen.get(p, []) + [scobj['invest_startdate']]
        # get all periodlens from all wlprofcodes
        for wlprofcode in listofwlprofcodes:
            p = WinLoseProfDatabase().view_item(wlprofcode).periodlen
            startdates = startdates_byperiodlen.get(p, 0)
            if startdates:
                print(f'WLPools are needed for perf metric "{wlprofcode}".  Running WLPool generation process...')
                WinLoseGenerator().generate_bywlprofcode(startdates, wlprofcode)

    def sync_samples(self, perfmetricnames):
        print(self)
        allperfprofiles = self.view_database()
        # add missing samples
        allavailsampcodes = set(PortfolioDatabase().view_database().keys())
        if allperfprofiles:
            currentsampcodes = set(i['sampcode'] for i in allperfprofiles)
            sampcodes_add = allavailsampcodes.difference(currentsampcodes)
            print(f'{len(sampcodes_add)} new sampcodes available to add.')
            allperfprofiles += [{'sampcode': sc} for sc in sampcodes_add]
        else:
            print('No performance profiles in the database. Adding available sampcodes.')
            allperfprofiles = [{'sampcode': s} for s in allavailsampcodes]
        # if perfmetricnames contains winlose metrics, gather corresponding wlpooldfs first otherwise multiprocessorpool within a pool error will occur
        self.generate_wlpools(perfmetricnames, allavailsampcodes)
        # update all entries with missing perfmetrics
        print('Updating performance profiles with new metrics...')
        updatedprofiles = MultiProcessor().mp_mapasync_getresults(self._sync_single, allperfprofiles, 'no', (perfmetricnames,))
        self._save_changes(updatedprofiles)
