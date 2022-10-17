"""
Title: Update Data Bot
Date Started: June 26, 2019
Version: 4.4
Version Date: Feb 28, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: List of functions needed to run to update data.

Versions:
4.2: Revise price matrix functions. 2.0 version of price matrix script.
4.3: Fixed capitalization of filename.
4.4: Replaced multiprocessor functions with generic multiprocessorshell function
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from filelocations import delete_create_folder
from UPDATEPRICEDATA_BASE import store_allprices
from UPDATEPRICEDATA_BASE_TICKER import storealltickers
from UPDATEPRICEDATA_BASE_DATERANGES import create_daterangedb
from UPDATEPRICEDATA_BASE_PRICEMATRIX import allprice_matrix
from UPDATEPRICEDATA_BASE_FULLINFOTICKERDATABASE_NOFUNDIES import create_fullinfotickerdatabase
from UPDATEPRICEDATA_FILELOCATIONS import STOCKPRICES, TICKERS, DATES, DATE_DUMP, DATE_RESULTS, FULL_INFO_DB, INDEXPRICES, tickerlistall_name, tickerlistcommon_name, alltickerfiles, tickerlistall_source, tickerlistcommon_source, PRICES, daterangedb_name, daterangedb_source

chunksize = 5
if __name__ == '__main__':

    '''DELETE ALL EXCEPT INDEXPRICE FOLDER'''
    folder_index = [
        STOCKPRICES,
        TICKERS,
        DATES,
        DATE_DUMP,
        DATE_RESULTS,
        FULL_INFO_DB
    ]
    for folder in folder_index:
        delete_create_folder(folder)

    '''BENCHMARK DOWNLOAD (INDEPENDENT)'''
    store_allprices(INDEXPRICES, '', "benchmark", chunksize)

    '''TICKERLIST DOWNLOAD'''
    storealltickers(TICKERS, tickerlistall_name, tickerlistcommon_name)

    '''STOCKPRICE DOWNLOAD (DEPENDENT ON TICKERLIST DOWNLOAD)'''
    # WAIT UNTIL TICKERLIST FILES EXIST
    for fileloc in alltickerfiles:
        tlistexist = os.path.isfile(fileloc)
        while tlistexist is False:
            tlistexist = os.path.isfile(fileloc)

    # DOWNLOAD STOCK PRICES
    store_allprices(STOCKPRICES, tickerlistall_source, "", chunksize)

    '''CREATE DATE DATABASE (DEPENDENT ON STOCK PRICE DOWNLOAD)'''
    create_daterangedb(DATE_DUMP, tickerlistall_source, STOCKPRICES, DATE_RESULTS, daterangedb_name, 'prices', chunksize)
    tlistexist = os.path.isfile(daterangedb_source)
    while tlistexist is False:
        tlistexist = os.path.isfile(daterangedb_source)

    '''CREATE FULL INFO DATABASE'''
    create_fullinfotickerdatabase(tickerlistcommon_source, tickerlistall_source, daterangedb_source, FULL_INFO_DB)

    '''CREATE PRICE HISTORY MATRIX (DEPENDENT ON STOCK PRICE DOWNLOAD)'''
    #allprice_matrix(tickerlistall_source, STOCKPRICES, PRICES)
    allprice_matrix(tickerlistcommon_source, STOCKPRICES, PRICES)
    #allprice_matrix('faang', STOCKPRICES, PRICES)
    allprice_matrix('bench', INDEXPRICES, PRICES)
