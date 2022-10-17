"""
Title: Best Streaks Masterscript - Current to Next
Date Started: Oct 13, 2020
Version: 1.0
Version Start Date: Oct 13, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Runs Best Streak Bot on two given time periods, ideally consecutive periods.  This was created to find out how likely if a stock is ranked high in winstreak for one period, that it would also be ranked high again in the following period.  You can adjust the criteria for each period to be compared, but ideally they should be set the same to make the comparisons less biased.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from BESTSTREAK_BASE_CURRNEXT import curr_to_next
from computersettings import computerobject
from filelocations import buildfolders_regime_testrun


# SET DATE AND TEST NUMBER
todaysdate = '2020-10-13'
testnumber = 8
# SET TEST REGIME NAME
testregimename = 'streakbot'

# VERBOSE PRINTING?
verbose = 'verbose'

# _beg, _end = dates of each respective streak period
# _benchticker = benchmark to compare stocks against in given streak period
# _periodlen = in what size timechunks over the streak period comparisons are to be made
# _avg_type = how to average the set of all amounts by which a stock beats the benchmark for each timechunk
# _rankbeg, _rankend = indices of the portion of stocklist to be used to compare to the other streak period

streakparam_dict = {
    'currbeg': '2011-01-01',
    'currend': '2013-01-01',
    'nextbeg': '2013-01-01',
    'nextend': '2015-01-01',
    'currbenchticker': '^IXIC',
    'nextbenchticker': '^IXIC',
    'currperiodlen': 15,
    'nextperiodlen': 15,
    'curravg_type': 'median',
    'nextavg_type': 'median',
    'curr_rankbeg': 0,
    'curr_rankend': 20,
    'next_rankbeg': 0,
    'next_rankend': 20,
    'trialno': 0
}


if __name__ == '__main__':

    rootdump = computerobject.bot_dump
    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdump, testnumber, todaysdate, testregimename)
    # get curr to next proportion
    curr_to_next(verbose, testrunparent, testrunparent, streakparam_dict)
    playsound('C:\Windows\Media\Ring03.wav')
