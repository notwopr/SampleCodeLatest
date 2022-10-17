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
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_regime_testrun, readpkl
from computersettings import computerobject
from STRATTEST_MULTITRIAL_MULTISTRAT_BASE import paramscriptmodifier, stratpanelmodifier, stage2stratpanelmodifier, stage3scriptloader
from STRATTEST_MULTITRIAL_BASE_LEADERBOARD import create_strattest_leaderboard
from STRATTEST_MULTITRIAL_BASE import strattest_multitrial, setpreconfigsamples
from STRATTEST_MULTITRIAL_BASE_LEADERBOARD import leaderboardsummary
#   METRIC PARAMS
#from Screenparams.SCREENPARAMS_STAGE2v5 import stage2_params
#from Screenparams.SCREENPARAMS_STAGE1v5 import stage1_params

trialrunset = readpkl('D20210427T2_STAGE1v5_finalpooltrialrunset', computerobject.bot_important)

global_params = {
    'todaysdate': '2021-05-25',
    'testnumber': 3,
    'testregimename': 'multitrials',
    'metricsetname': 'stage1plusstage3_top15',
    'num_trials': 1000,
    'trialtype': 'random',
    'fundycompatpools': 'yes',
    'rankmeth': 'standard',
    'rankregime': '1isbest',
    'testlen': 365,
    'benchticker': '^IXIC',
    'trimsize': 15,
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
    # set leaderboardcomponent sourcefolder
    sourcefolder = computerobject.bot_important / 'STRATTESTER' / 'LEADERBOARDCOMPONENTS'
    s3set1 = [
        #'SCREENPARAMS_STAGE3_agemaxddplusbestgrowth_v7',
        #'SCREENPARAMS_STAGE3_agemaxddplusbestgrowth_v10',
        #'volatility.SCREENPARAMS_STAGE3_VOLATILITYv16',
        #'volatility.SCREENPARAMS_STAGE3_VOLATILITYv18',
        #'SCREENPARAMS_STAGE3_agemaxddplusbestgrowth_v2',
        #'volatility.SCREENPARAMS_STAGE3_VOLATILITYv13',
        #'volatility.SCREENPARAMS_STAGE3_VOLATILITYv6',
        #'Smoothness.SCREENPARAMS_smoothness_rankstagev9k',
        #'Smoothness.SCREENPARAMS_smoothness_rankstagev9i_FCF',
        #'SCREENPARAMS_STAGE3_MKTBEATOVERMINv11',
        #'SCREENPARAMS_reboundbot_STAGE3v2',
        #'Smoothness.SCREENPARAMS_smoothness_rankstagev9m2_REV',
        #'Smoothness.SCREENPARAMS_smoothness_rankstagev9k_REV',
        'SCREENPARAMS_STAGE3_FALL2020v1',
        'Smoothness.SCREENPARAMS_smoothness_rankstagev9m_FCF',
        'losscontrol.SCREENPARAMS_STAGE3_LOSSCONTROLv1',
        'losscontrol.SCREENPARAMS_STAGE3_LOSSCONTROLv1_FCF',
        'SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv14a',
        'SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv14b',
        'SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv13'
    ]
    # modify stage 2 strats
    #strat_panel = stage2stratpanelmodifier(s2setup, strat_panel)
    for s3setup in s3set1:
        # modify global params
        if s3setup in [
            'volatility.SCREENPARAMS_STAGE3_VOLATILITYv6',
            'SCREENPARAMS_reboundbot_STAGE3v2',
            'SCREENPARAMS_STAGE3_MKTBEATOVERMINv11',
            'SCREENPARAMS_STAGE3_agemaxddplusbestgrowth_v10',
            'SCREENPARAMS_STAGE3_agemaxddplusbestgrowth_v7'
                ]:
            global_params.update({'rankmeth': 'minmax'})
        else:
            global_params.update({'rankmeth': 'standard'})
        # reset stratpanel
        strat_panel = {'multistageweightmode': 'no'}
        # load stage 3 strat
        stage3_params = stage3scriptloader('Screenparams.', s3setup)
        # update stratpanel with stage3 script
        strat_panel.update({'Stage 3': stage3_params})
        #strat_panel = stratpanelmodifier('Screenparams.', s3setup, strat_panel)
        # set preconfigured trial samples
        preconfigsamples = setpreconfigsamples(global_params)
        # run multitrials
        multitrialstatsdf = strattest_multitrial(computerobject.bot_dump, global_params, preconfigsamples, strat_panel)
        # create leaderboard summary
        leaderboardsummary(sourcefolder, global_params, strat_panel, multitrialstatsdf)
        # update testnumber
        testnumber = global_params['testnumber'] + 1
        global_params.update({'testnumber': testnumber})
    # create new leaderboard
    destfolder = computerobject.bot_important / 'STRATTESTER' / 'LEADERBOARDS'
    create_strattest_leaderboard(sourcefolder, destfolder)
    playsound('C:\Windows\Media\Ring03.wav')
