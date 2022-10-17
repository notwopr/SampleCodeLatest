"""
Title: Update Price Data File Locations
Date Started: Dec 7, 2020
Version: 1.0
Version Date: Dec 7, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Set commonly retrieved filelocs in a separate file to avoid loading updatepricedata scripts into cache for functions not related to updating pricedata.
Versions:
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from machinesettings import _machine
from file_functions import join_str


class FileNames:
    fn_tickerlistall = 'tickerlist_all'
    fn_tickerlistcommon = 'tickerlist_common'
    fn_fullinfodb = 'fullinfo_db'
    fn_pricematrix_common = 'allpricematrix_common'
    fn_pricematrix_bench = 'allpricematrix_bench'
    fn_pricematrix_commonplusbench = 'allpricematrix_commonplusbench'
    fn_daterangedb = 'daterangedb_prices'
    fn_daterangedb_marketcap = 'daterangedb_marketcap'
    fn_daterangedb_fundies = 'daterangedb_fundies'
    fn_db_wlprofile = 'db_wlprofile'
    fn_db_metricfunction = 'db_metricfunction'
    fn_db_ingredient = 'db_ingredient'
    fn_db_stagerecipe = 'db_stagerecipe'
    fn_db_strategycookbook = 'db_strategycookbook'
    fn_db_stratpool = 'db_stratpool'
    fn_db_investplan = 'db_investplan'
    fn_db_portfolio = 'db_portfolio'
    fn_db_sampcode = 'db_sampcode'
    fn_db_perfprofilelib = 'db_perfprofilelib'
    fn_db_perfmetricfunction = 'db_perfmetricfunction'
    fn_db_wlprofile = 'db__wlprofile'
    fn_db_wlpool = 'db_wlpool'
    fn_db_perfmetricnames = 'db_perfmetricnames'
    fn_db_cloudsample = 'db_cloudsample'


# contains all main directory paths in string form
class DirPaths:
    dataroot = _machine.dataroot
    auth = join_str([dataroot, 'AUTH'])
    # STOCK DATA
    stockdata = join_str([dataroot, 'STOCKDATA'])
    # tickers
    tickers = join_str([stockdata, 'tickers'])
    # eod prices
    eodprices = join_str([stockdata, 'eodprices'])
    eodprices_stock = join_str([eodprices, 'stockprices'])
    eodprices_index = join_str([eodprices, 'indexprices'])
    # marketcap and fundamentals
    marketcap = join_str([stockdata, 'marketcap'])
    fundies = join_str([stockdata, 'fundies'])
    # dates
    dates = join_str([stockdata, 'dates'])
    date_dump = join_str([dates, 'dump'])
    date_results = join_str([dates, 'results'])
    marketcapdate_dump = join_str([dates, 'marketcapdump'])
    marketcapdate_results = join_str([dates, 'marketcapdateresults'])
    fundiesdate_dump = join_str([dates, 'fundiesdump'])
    fundiesdate_results = join_str([dates, 'fundiesresults'])
    # full info db
    full_info_db = join_str([stockdata, 'fullinfodb'])
    # DATABASES
    dbparent = join_str([dataroot, 'DATABASES'])
    # winlose tester
    winlosetester = join_str([dataroot, 'WINLOSETESTER'])
    # strattester
    strattester = join_str([dataroot, 'STRATTESTER'])
    strattester_testruns = join_str([strattester, 'STRATTESTER_TESTRUNS'])
    strattester_stockperfreports = join_str([strattester, 'STRATTESTER_STOCKPERFREPORTS'])
    strattester_allperiodstatdf = join_str([strattester, 'STRATTESTER_ALLPERIODSTATDF'])
    # MISC BOT DUMP DATA
    bot_dump = join_str([dataroot, 'BOT_DUMP'])
