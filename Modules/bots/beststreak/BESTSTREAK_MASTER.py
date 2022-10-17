"""
Title: Best Streaks Masterscript
Date Started: Sept 26, 2020
Version: 1.0
Version Start Date: Sept 26, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Given date range and period len, return (1) number of periods beat market (2) avg margin beating the market and (3) the longest streak of beating the market.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from BESTSTREAK_BASE import beststreak_cruncher
from computersettings import computerobject
from filelocations import buildfolders_regime_testrun


# SET DATE AND TEST NUMBER
todaysdate = '2020-11-18'
testnumber = 6

# SET TEST REGIME NAME
testregimename = 'streakbot'

# TIME PERIOD
beg_date = '2016-10-29'
end_date = '2021-10-29'

# DEFINE PERIOD LENGTH
periodlen = 15

# WHICH BENCHMARK DO YOU WANT TO USE?
benchticker = '^IXIC'

# HOW DO YOU WANT TO CALCULATE AVERAGE MARGIN?
avg_type = 'median'
# HOW DO YOU WANT TO CALCULATE DEVIATION OF MARGIN?
dev_type = 'std'
# HOW DO YOU WANT TO WEIGHT THE IMPORTANCE OF MARGIN AND OCCURRENCES?
avgmarginweight = (1/2) * (3/4)
devmarginweight = (1/2) * (1/4)
num_mktbeatweight = 1/2

# VERBOSE REPORTING?
verbose = ''
# VERBOSE FILE?
verbosefile = 'no'
# DEFINE POOL OF STOCKS TO DRAW FROM (empty if want all existing stocks)
custompool = []

# SET MULTIPROCESSOR CHUNKSIZE
chunksize = 5

if __name__ == '__main__':
    testregimeparent = computerobject.bot_dump
    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(testregimeparent, testnumber, todaysdate, testregimename)
    beststreak_cruncher(verbose, verbosefile, beg_date, end_date, benchticker, periodlen, avg_type, dev_type, avgmarginweight, devmarginweight, num_mktbeatweight, testrunparent, 'standard', '1isbest', custompool, chunksize)
    playsound('C:/Windows/Media/Ring03.wav')
