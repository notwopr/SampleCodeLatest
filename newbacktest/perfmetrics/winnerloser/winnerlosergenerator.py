# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.perfmetrics.winnerloser.class_winloseprofile import WinLoseProfile
from newbacktest.perfmetrics.winnerloser.db_wlprofile import WinLoseProfDatabase
from newbacktest.perfmetrics.winnerloser.db_wlpool import WinLosePoolDatabase
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater_perfmetricnames import PerfMetricNameDatabase


class WinLoseGenerator:
    '''
    Generates and stores dataframes of winner/losers based on the desired criteria.  DFs are stored by stratcode+ipcode combo and then by invest_startdate
    This is unlike the portfoliogenerator, in that it doesn't randomly choose dates.  It takes an input array of them.
    '''

    def generate_bywlprofcode(self, allinvest_startdates, wlprofcode):
        '''generate winner/loser pools'''
        print(allinvest_startdates)
        for invest_startdate in allinvest_startdates:
            print(f'Invest Start_Date: {invest_startdate}\n')

            '''check if pool already exists'''
            wlpdb = WinLosePoolDatabase()
            print(f'Checking if {wlpdb._item_term} already exists for invest_startdate of "{invest_startdate}" and {wlpdb._keyname_term} "{wlprofcode}" in the {wlpdb._dbname}...', end='')
            existence = wlpdb.view_wlpool(wlprofcode, invest_startdate)
            if existence is not None and existence != 0:
                print('it does.\nMoving on to the next invest_startdate...\n\n')
                continue
            else:
                '''Generate WL Pool'''
                print(f'it does not. Generating Win Lose Pooldf for invest_startdate "{invest_startdate}" and {wlpdb._keyname_term} "{wlprofcode}"...')
                wlpdb.add_item(wlprofcode, invest_startdate)

                print(wlpdb)
                print(wlpdb.view_wlpool(wlprofcode, invest_startdate).itemdata)
            print('Moving on to the next trial...\n\n')
        print('All requested WLPools generated.')

    def generate_bywlprofile(self, wlprofile, periodlen, allinvest_startdates):
        '''create winner/loser profile you want to use'''
        wlprofile = WinLoseProfile(wlprofile, periodlen)
        WinLoseProfDatabase().add_item(wlprofile)
        wlprofcode = wlprofile.itemcode
        '''generate wlpools'''
        self.generate_bywlprofcode(allinvest_startdates, wlprofcode)
        '''add wlprofcode to perfmetricnames'''
        PerfMetricNameDatabase().add_item([wlprofcode])
        return wlprofcode
