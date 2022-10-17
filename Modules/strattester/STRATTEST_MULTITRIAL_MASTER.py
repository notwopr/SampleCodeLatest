"""
Title: LOOP TEST MASTER
Date Started: July 10, 2020
Version: 2.00
Version Start: Oct 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given number of trials, and date range, runs a random date, returns percentage of resulting pool that beat market for each trial and summarizes all trial results.
VERSIONS:
1.01: Optimize with updated functions.  Allow for more modulatory.
2.0: Simplified for running loops over several different param scripts and recording leaderboard dict line.

'fundyagemin' = min num of rows of fundy data allowed for a stock
'lastfundyreportage'= the max allowed time has passed since most recent fundy report published
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from STRATTEST_MULTITRIAL_BASE import strattest_multitrial, setpreconfigsamples
from STRATTEST_MULTITRIAL_BASE_LEADERBOARD import leaderboardsummary, create_strattest_leaderboard
from filelocations import readpkl
#   METRIC PARAMS
#from Screenparams.SCREENPARAMS_STAGE1v5 import stage1_params
#from Screenparams.SCREENPARAMS_STAGE2v5 import stage2_params
from Screenparams.SCREENPARAMS_STAGE3_FALL2020v1 import stage3_params

# SET SCRIPT WEIGHTS IF USING MULTISTAGEWEIGHTMODE
'''
stage3A_params.update(
    {'scriptweight': (1/2)}
)
stage3B_params.update(
    {'scriptweight': (1/2)}
)

stage3C_params.update(
    {'scriptweight': (1/4)*(1/2)}
)
stage3D_params.update(
    {'scriptweight': 1/2}
)

stage3E_params.update(
    {'scriptweight': (1/2)*(1/3)}
)
stage3F_params = stage3B_params
stage3F_params.update(
    {'scriptweight': (1/2)*(1/3)}
)

'''
# SET FILTERS
strat_panel = {
    'multistageweightmode': 'no',
    #'Stage 1': stage1_params,
    #'Stage 2 Part I': stage2_params,
    #'Stage 2 Part II': stage2b_params,
    #'Stage 2 Part III': stage2c_params,
    'Stage 3': stage3_params,
    #'Stage 3': stage3A_params,
    #'Stage 3B': stage3B_params,
    #'Stage 3C': stage3C_params,
    #'Stage 3D': stage3D_params,
    #'Stage 3E': stage3E_params,
    #'Stage 3F': stage3F_params
}

# datepoolsetdir = r'D:\BOT_DUMP\dropbot\D20201209T4'
trialrunset = readpkl('D20210427T2_STAGE1v5_finalpooltrialrunset', computerobject.bot_important)

global_params = {
    'todaysdate': '2021-06-14',
    'testnumber': 1,
    'testregimename': 'multitrialsnew',
    'metricsetname': 'stage1plusstage3_top15',
    'num_trials': 1000,
    'trialtype': 'random',
    'fundycompatpools': 'yes',
    'rankmeth': 'standard',
    'rankregime': '1isbest',
    'testlen': 365,
    'benchticker': '^IXIC',
    'trimsize': None,
    'latestdate': '',
    'firstdate': '2005-01-06',
    'minimumage': 3,
    'fundyagemin': 90,
    'lastfundyreportage': 30*3,
    'existingset': trialrunset,
    'createfinalpoolset': 'no',
    'preconfigsamps': 'singlesource',
    'verbose': 'no',
    'usemultiprocessor': 'no',
    'savemode': '',
    'chunksize': 5
}


if __name__ == '__main__':
    # set preconfigured trial samples
    preconfigsamples = setpreconfigsamples(global_params)
    # run multitrials
    multitrialstatsdf = strattest_multitrial(computerobject.bot_dump, global_params, preconfigsamples, strat_panel)
    # create leaderboard summary
    sourcefolder = computerobject.bot_important / 'STRATTESTER' / 'LEADERBOARDCOMPONENTS'
    leaderboardsummary(sourcefolder, global_params, strat_panel, multitrialstatsdf)
    # create new leaderboard
    destfolder = computerobject.bot_important / 'STRATTESTER' / 'LEADERBOARDS'
    create_strattest_leaderboard(sourcefolder, destfolder)
    playsound('C:\Windows\Media\Ring03.wav')
