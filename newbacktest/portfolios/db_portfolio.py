# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl_fullpath
from newbacktest.abstractclasses.db_abstract import AbstractDatabase
from file_hierarchy import DirPaths, FileNames
from newbacktest.dataframe_operations import DataFrameOperations
from Modules.dates import DateOperations
from newbacktest.datasource import DataSource
from newbacktest.stratpools.db_stratpool import StratPoolDatabase
from newbacktest.symbology.sampcode import SampCode
from newbacktest.symbology.investplancode import InvestPlanCode


class PortfolioDatabase(AbstractDatabase):
    '''
    The Portfolio Database contains a dataframe storing portfolios resulting from a given stratcode and ipcode and indexed by stratcode, then by ipcode, then by invest_startdate.
    structure = {
        <sampcode>: portfoliodf = dataframe of all tickers EOD prices from invest_startdate to invest_enddate
        ....
    }
    '''
    _emptydb = {}

    def __init__(self):
        self._dbname = "Portfolio Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_portfolio
        self._item_term = "Portfolio"

    # open database
    def _open_database(self):
        return readpkl_fullpath(self._filepath_to_db) if os.path.exists(self._filepath_to_db) else self._emptydb

    # by stratcode, ipcode, invest_startdate
    def view_item(self, sampcode):
        return self._open_database().get(sampcode, 0)

    def _get_portfoliodf(self, scobj):
        ipobject = InvestPlanCode().decode(scobj['ipcode'])
        invest_period = ipobject['periodlen']
        invest_enddate = DateOperations().plusminusdays(scobj['invest_startdate'], invest_period)
        rank_start = ipobject['batchstart']
        portsize = ipobject['portsize']
        portfolio = StratPoolDatabase().view_stratpool(scobj['stratcode'], scobj['invest_startdate']).itemdata['stock'].tolist()[rank_start:rank_start+portsize]
        ds = DataSource().opends('eodprices')
        ds = DataFrameOperations().filter_column(ds, ['date']+portfolio)
        ds.ffill(inplace=True)
        ds = DataFrameOperations().filter_bycolandrow_double(ds, '>=<=', scobj['invest_startdate'], invest_enddate, 'date', ['date']+portfolio)
        return ds

    # add item to database
    def add_item(self, sampcode):
        db_contents = self._open_database()
        if not db_contents or not db_contents.get(sampcode, 0):
            scobj = SampCode().decode(sampcode)
            if not len(StratPoolDatabase().view_stratpool(scobj['stratcode'], scobj['invest_startdate']).itemdata):
                db_contents[sampcode] = 0
                print(f'Although a stratpooldf was generated for stratcode "{scobj["stratcode"]}", all stocks were filtered out. No portfoliodf therefore can be generated for this sampcode ("{sampcode}")')
            else:
                db_contents[sampcode] = self._get_portfoliodf(scobj)
            self._save_changes(db_contents)
            print(f"{self._item_term} with sampcode '{sampcode}' successfully saved to {self._dbname}!")
        else:
            print(f"A {self._item_term} with sampcode '{sampcode}' already exists in the {self._dbname}.")
            return
