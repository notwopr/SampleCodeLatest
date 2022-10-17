"""
Title: Best Streaks Masterscript - Current to Next - Multitrial
Date Started: Oct 13, 2020
Version: 1.0
Version Start Date: Oct 13, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Multitrial Version.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from BESTSTREAK_BASE_CURRNEXT_MULTITRIALS import beststreak_multitrials, leaderboard_beststreakbot
from computersettings import computerobject


# VERBOSE PRINTING?
verbose = ''

globalsettingsdict = {
    'todaysdate': '2020-10-25',
    'testnumber': 1,
    'testregimename': 'streakbot',
    'currentphase': 90,
    'nextphase': 360,
    'num_trials': 100,
    'latestdate': '',               # latest date a curr-nextphase can take
    'firstdate': '2000-01-01'       # earliest date a curr-nextphase can take
}

# _beg, _end = dates of each respective streak period
# _benchticker = benchmark to compare stocks against in given streak period
# _periodlen = in what size timechunks over the streak period comparisons are to be made
# _avg_type = how to average the set of all amounts by which a stock beats the benchmark for each timechunk
# _rankbeg, _rankend = indices of the portion of stocklist to be used to compare to the other streak period

trialsettings_dict = {
    'currbenchticker': '^IXIC',
    'nextbenchticker': '^IXIC',
    'currperiodlen': 1,
    'nextperiodlen': 1,
    'curravg_type': 'median',
    'nextavg_type': 'median',
    'curr_rankbeg': 0,
    'curr_rankend': 20,
    'next_rankbeg': 0,
    'next_rankend': 1000
}


if __name__ == '__main__':
    sourcefolder = computerobject.bot_important / 'beststreakbot' / 'beststreakbot_leaderdump'
    # run multitrials
    for iternum in range(1, 31):
        beststreak_multitrials(verbose, computerobject.bot_dump, globalsettingsdict, trialsettings_dict, sourcefolder)
        # update settings
        newcurrphase = 90 + globalsettingsdict['currentphase']
        newtestnumber = 1 + globalsettingsdict['testnumber']
        globalsettingsdict.update({'currentphase': newcurrphase, 'testnumber': newtestnumber})
    # save new multitrial leaderboard file
    destfolder = computerobject.bot_important / 'beststreakbot' / 'beststreakbot_leaderboards'
    leaderboard_beststreakbot(sourcefolder, destfolder)
    playsound('C:\Windows\Media\Ring03.wav')
