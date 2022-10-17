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
from UPDATEPRICEDATA_BASE import store_allfundies
from UPDATEPRICEDATA_BASE_DATERANGES import create_daterangedb
from UPDATEPRICEDATA_BASE_FULLINFOTICKERDATABASE import create_fullinfotickerdatabase
from UPDATEPRICEDATA_FILELOCATIONS import FULL_INFO_DB, FUNDIES, FUNDIESDATE_DUMP, FUNDIESDATE_RESULTS, tickerlistall_source, tickerlistcommon_source, daterangedb_source, daterangedb_name_fundies, daterangedb_source_marketcap, daterangedb_source_fundies

chunksize = 5
if __name__ == '__main__':

    '''DELETE ALL EXCEPT INDEXPRICE FOLDER'''
    folder_index = [
        FULL_INFO_DB,
        FUNDIES,
        FUNDIESDATE_DUMP,
        FUNDIESDATE_RESULTS
    ]
    for folder in folder_index:
        delete_create_folder(folder)

    '''DOWNLOAD FUNDAMENTALS'''
    store_allfundies(FUNDIES, tickerlistall_source, chunksize)

    '''CREATE FUNDIES DATE DATABASE (DEPENDENT ON FUNDAMENTALS DOWNLOAD)'''
    create_daterangedb(FUNDIESDATE_DUMP, tickerlistall_source, FUNDIES, FUNDIESDATE_RESULTS, daterangedb_name_fundies, 'fundies', chunksize)
    tlistexist = os.path.isfile(daterangedb_source_fundies)
    while tlistexist is False:
        tlistexist = os.path.isfile(daterangedb_source_fundies)

    '''CREATE FULL INFO DATABASE'''
    create_fullinfotickerdatabase(tickerlistcommon_source, tickerlistall_source, daterangedb_source, daterangedb_source_marketcap, daterangedb_source_fundies, FULL_INFO_DB)
    playsound('C:\Windows\Media\Ring03.wav')
