"""
Title: Complement Bot - Master
Date Started: Apr 20, 2020
Version: 2.0
Version Start: Oct 30, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Complement score is a measure of how well two stocks go together, i.e. if one stock goes down, the other goes up, but if one goes up, the other goes up as well.  And also measures against benchmark chosen.

VERSION NOTES

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from COMPLEMENTBOT_BASE import complement_ranker
from computersettings import computerobject
from filelocations import buildfolders_regime_testrun, buildfolders_singlechild, readpkl, readcsv
from UPDATEPRICEDATA_FILELOCATIONS import TICKERS, tickerlistcommon_name


# SET DATE AND TEST NUMBER AND REGIME
todaysdate = '2021-11-10'
testnumber = 7

# SET TEST REGIME NAME
testregimename = 'complement_bot'

existdate = ''  # enter a date only if you want to limit the data to a specific point in the past
targetstock = 'CARR'  # the stock against which you want to find a good complement out of a list of candidates

# SELECT CANDIDATE POOL FROM ALL TICKER SYMBOLS
#tickerlistdf = readpkl(tickerlistcommon_name, TICKERS)
#candidates = tickerlistdf['symbol'].tolist()

# OR SELECT CANDIDATE POOL FROM A CUSTOM SOURCE LIST
resultfileloc = Path(r'C:\Users\david\Documents\PROJECTBELUGA\BOT_DUMP\strattest_singles')
resultfilename = 'Stage 3_STAGE3_groplusvolv15d_finalists_as_of_2021-10-29'
resultdf = readcsv(resultfilename, resultfileloc)
candidates = resultdf['stock'].tolist()

# SET RANK WEIGHTS
rankweights = {
    'num_comparisons (target_candidate)': 1/12,
    'num_atleastonefalling_pct (target_candidate)': 5/12,
    'complementscore (target_candidate)': 6/12
}

# DO YOU WANT TO COMPARE IT AGAINST A BENCHMARK?
benchticker = ''

# VERBOSE PRINTING?
verbose = 'no'
# WANT TO SAVE DUMP FILES TO DISK?
savemode = 'no'
# CHUNKSIZE
chunksize = 5

if __name__ == '__main__':
    testregimeparent, testrunparent = buildfolders_regime_testrun(computerobject.bot_dump, testnumber, todaysdate, testregimename)
    dfdumpfolder = buildfolders_singlechild(testrunparent, 'dfdump')
    summaryfolder = buildfolders_singlechild(testrunparent, 'summaries')
    complement_ranker(testrunparent, summaryfolder, dfdumpfolder, existdate, candidates, targetstock, rankweights, benchticker, verbose, savemode, chunksize)
