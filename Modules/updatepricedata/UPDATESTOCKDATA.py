"""
Title: Update Data Bot
Date Started: June 26, 2019
Version: 4.5
Version Date: Apr 8, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: List of functions needed to run to update data.

Versions:
4.2: Revise price matrix functions. 2.0 version of price matrix script.
4.3: Fixed capitalization of filename.
4.4: Replaced multiprocessor functions with generic multiprocessorshell function
4.5: made into one function call for webapp use.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_functions import delete_create_folder, join_str
from file_hierarchy import DirPaths, FileNames
from Modules.updatepricedata.UPDATEPRICEDATA_BASE import store_allprices
from Modules.updatepricedata.UPDATEPRICEDATA_BASE_TICKER import storealltickers
from Modules.updatepricedata.UPDATEPRICEDATA_BASE_DATERANGES import create_daterangedb
from Modules.updatepricedata.UPDATEPRICEDATA_BASE_PRICEMATRIX import allprice_matrix
from Modules.updatepricedata.UPDATEPRICEDATA_BASE_FULLINFOTICKERDATABASE_NOFUNDIES import create_fullinfotickerdatabase

STOCKPRICES = Path(DirPaths().eodprices_stock)
TICKERS = Path(DirPaths().tickers)
DATE_RESULTS = Path(DirPaths().date_results)
FULL_INFO_DB = Path(DirPaths().full_info_db)
INDEXPRICES = Path(DirPaths().eodprices_index)
PRICES = Path(DirPaths().eodprices)
tickerlistall_name = FileNames().fn_tickerlistall
tickerlistcommon_name = FileNames().fn_tickerlistcommon
tickerlistall_source = Path(join_str([DirPaths().tickers, f"{FileNames().fn_tickerlistall}.pkl"]))
tickerlistcommon_source = Path(join_str([DirPaths().tickers, f"{FileNames().fn_tickerlistcommon}.pkl"]))
daterangedb_name = FileNames().fn_daterangedb
daterangedb_source = Path(join_str([DirPaths().date_results, f"{FileNames().fn_daterangedb}.pkl"]))


def updatestockdata_recreatefolders():
    folder_index = [
        STOCKPRICES
    ]
    for folder in folder_index:
        delete_create_folder(folder)


# update stock data
def updatestockdata(chunksize):
    updatestockdata_recreatefolders()
    store_allprices(INDEXPRICES, '', "benchmark", chunksize)
    storealltickers(TICKERS, tickerlistall_name, tickerlistcommon_name)
    for fileloc in [tickerlistall_source, tickerlistcommon_source]:
        tlistexist = os.path.isfile(fileloc)
        while tlistexist is False:
            tlistexist = os.path.isfile(fileloc)
    store_allprices(STOCKPRICES, tickerlistall_source, "", chunksize)
    create_daterangedb(tickerlistall_source, DATE_RESULTS, daterangedb_name, 'prices', chunksize)
    tlistexist = os.path.isfile(daterangedb_source)
    while tlistexist is False:
        tlistexist = os.path.isfile(daterangedb_source)
    allprice_matrix(tickerlistcommon_name, TICKERS, STOCKPRICES, PRICES, chunksize)
    allprice_matrix('bench', TICKERS, INDEXPRICES, PRICES, chunksize)
    create_fullinfotickerdatabase(tickerlistcommon_source, tickerlistall_source, daterangedb_source, FULL_INFO_DB)
