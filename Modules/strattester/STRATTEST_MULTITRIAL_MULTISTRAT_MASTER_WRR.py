"""
Title: STRAT TEST MULTITRIAL MULTISTRAT PANEL MASTER
Date Started: July 10, 2020
Version: 2.00
Version Start: Oct 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given number of trials, and date range, runs a random date, returns percentage of resulting pool that beat market for each trial and summarizes all trial results.
VERSIONS:
1.01: Optimize with updated functions.  Allow for more modulatory.
2.0: Simplified for running loops over several different param scripts and recording leaderboard dict line.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_regime_testrun
from computersettings import computerobject
from STRATTEST_MULTITRIAL_MULTISTRAT_BASE import multistrat_multitrials_winrateranker
from STRATTEST_MULTITRIAL_BASE_LEADERBOARD import create_strattest_leaderboard
#   METRIC PARAMS
from Screenparams.SCREENPARAMS_STAGE3_WINRATERANKERv22 import stage3_params


global_params = {
    'todaysdate': '2021-01-25',
    'testnumber': 5,
    'testregimename': 'multitrials',
    'metricsetname': 'winrateranker_top30',
    'num_trials': 100,
    'rankmeth': 'minmax_nan',
    'rankregime': '1isbest',
    'testlen': 365,
    'benchticker': '^IXIC',
    'trimsize': 30,
    'latestdate': '',
    'firstdate': '2000-01-01',
    'preconfigsamps': 'singlesource',
    'verbose': 'no',
    'usemultiprocessor': 'no',
    'savemode': '',
    'chunksize': 5
}

# SET FILTERS
strat_panel = {
    #'Stage 1': stage1_params,
    'Stage 3': stage3_params
}


if __name__ == '__main__':
    # set leaderboardcomponent sourcefolder
    sourcefolder = computerobject.bot_important / 'STRATTESTER' / 'LEADERBOARDCOMPONENTS'
    # set winlen ceiling
    winlen_ceiling = 2
    for sourcetype in ['straight', 'trueline', 'rawprice']:
        if sourcetype == 'rawprice':
            statgroup = ['mean']
        else:
            statgroup = ['mean', 'std']
        for stat_type in statgroup:
            for rankmeth in ['standard']:
                multistrat_multitrials_winrateranker(computerobject.bot_dump, sourcefolder, global_params, strat_panel, sourcetype, stat_type, rankmeth, winlen_ceiling)
    # create new leaderboard
    destfolder = computerobject.bot_important / 'STRATTESTER' / 'LEADERBOARDS'
    create_strattest_leaderboard(sourcefolder, destfolder)
    playsound('C:\Windows\Media\Ring03.wav')
