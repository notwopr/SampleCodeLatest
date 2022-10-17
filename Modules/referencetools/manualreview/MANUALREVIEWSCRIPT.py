"""
Title: Manual Review Script
Date Started: Oct 29, 2020
Version: 1.0
Version Start Date: Oct 29, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Functions to take when doing manual review.
VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
import pandas as pd
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from STOCKLIBRARY_FUNCTIONS import addremove_stock, switchlist, save_stocklist, viewstocklist, constructportlib
from STOCKLIBRARY_GRAPHGRADER import graphgrader
from computersettings import computerobject
from filelocations import readpkl
from UPDATEPRICEDATA_MASTERSCRIPT import TICKERS
from MANUALREVIEWSCRIPT_RECORDPORTFOLIOS import recordportfolios

# STOCKLIST FILE LOCATIONS
STOCKLISTS = computerobject.bot_important / 'stocklists'
GRAPHGRADEPARENT = STOCKLISTS / 'graphgrades'
CURRENT_SL = GRAPHGRADEPARENT / 'CURRENT'
PAST_SL = GRAPHGRADEPARENT / 'PAST'
PORTFOLIODIR = STOCKLISTS / 'portfolios'

# GRADE candidates
stocklist = [
    'FIVN',
    'CARR',
    'FRHC',
    'KNSL',
    'PTON',
    'OKTA',
    'SHOP',
    'TEAM',
    'IMVT',
    'PAYC',
    'BAND',
    'NET',
    'SPT',
    'ZM',
    'PLMR',
    'TTD',
    'COUP',
    'EVBG',
    'MDB',
    'DDOG',
    'ARNC',
    'GSHD',
    'SQ',
    'EPAM',
    'FVRR',
    'BIPC',
    'NOW',
    'SITM',
    'BL',
    'MYOK',
    'TXG',
    'BWMX',
    'GLOB',
    'WIX',
    'EXPI',
    'DOCU',
    'CCC',
    'TWLO',
    'OTIS',
    'TDOC',
    'RNG',
    'CRNC',
    'ACMR',
    'TFFP',
    'LVGO',
    'IRTC',
    'CSTL',
    'BILL',
    'CXDO',
    'SEDG',
    'ZS',
    'CVNA',
    'AHCO',
    'CHWY',
    'APG',
    'TSLA',
    'MRNA',
    'AVLR',
    'MRTX',
    'GRWG'
]
# STEP 0: ELIMINATE BAD VISUALS USING QUICKREFERENCE_QUICKGRAPHER
    # step 0.1: run single strattest on candidate list using the badvisuals paramscript
    # step 0.2: review the graphs using quickref grapher
    # step 0.3: eliminate the bad visuals aided by the rankings set by the paramscript
# STEP 1: GRADE THE GRAPHS OF THE FINALISTS
#graphgrader(stocklist, '2020-10-31', 'nov2020candidates', CURRENT_SL, PAST_SL)
# STEP 2: RETURN THE LIST IN CSV TO CUT AND PASTE INTO SPREADSHEET
#gradesheet = readpkl('nov2020candidates_2020-10-31', CURRENT_SL)
#gradesheet.to_csv(index=False, path_or_buf=computerobject.bot_dump / 'gradesheet.csv')
# STEP 3: CUT AND PASTE IN GRAPH GRADES INTO SPREADSHEET

# STEP 4: GATHER FULL NAMES OF STOCK
#tickerdf = readpkl('tickerlist_common', TICKERS)
#tickerdf = tickerdf[tickerdf['symbol'].isin(stocklist)]
#tickerdf.reset_index(inplace=True, drop=True)
#tickerdf.to_csv(index=False, path_or_buf=computerobject.bot_dump / 'tickerdf.csv')
# STEP 5: COPY AND PASTE FULL NAMES TO SPREADSHEET
# STEP 6: ADD COMPANY INFO TO SPREADSHEET
# STEP 7: RANK EARNINGS HISTORY, PRODUCT POTENTIAL
# STEP 8: GET SLOPESCORE RANK
# STEP 9: GET DRAWDOWN RANK
# STEP 10: GET COMBINATIONS OF ALL RANKS DESIRED
# STEP 11: SAVE CSV OF RANKING SHEET
# STEP 12: RECORD TOP 10 PORTFOLIOS OF EACH RANKING TYPE TO PORT LIBRARY
sourcepath = r'C:\Users\david\Downloads\NOVEMBER 2020 PICKS ANALYSIS - STEP 4_ SAVE TO CSV.csv'
stratname = 'fall2020v1v1'
existdate = '20201031'
rankascend = False
rankbatchsize = 10
stocklistdest = PORTFOLIODIR
archivedest = STOCKLISTS
recordportfolios(stratname, existdate, rankascend, rankbatchsize, sourcepath, stocklistdest, archivedest)
playsound('C:\Windows\Media\Ring03.wav')
