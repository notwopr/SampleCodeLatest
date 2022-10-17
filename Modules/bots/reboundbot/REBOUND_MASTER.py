"""
Title: REBOUND MASTER
Date Started: Nov 12, 2020
Version: 1.00
Version Start: Nov 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Find stocks that have greatest promise for rebound.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from REBOUND_BASE import rebound_single_event
from STRATTEST_SINGLE_BASE import getperfstats
from filelocations import buildfolders_regime_testrun
from Screenparams.SCREENPARAMS_STAGE3_LOSSCONTROLv41 import stage3_params

# SET QUALITY STRAT PANEL
strat_panel = {
    #'Stage1': stage1_params,
    #'Stage 2 Part I': stage2part1_params,
    #'Stage 2 Part II': stage2part2_params,
    'Stage3': stage3_params
}
global_params = {
    'todaysdate': '2020-11-14',
    'testnumber': 7,
    'testregimename': 'rebound',
    'eventname': 'coronavirus',
    'eventstart': '2020-02-19',
    'eventend': '2020-03-23',
    'verbose': '',
    'weight_loss': 1/2,
    'weight_quality': 1/2,
    'rankmeth': 'minmax',
    'rankregime': '1isbest',
    'qualitystratpanel': strat_panel
}


# PERFORMANCE SETTINGS
calcperfstats = 'yes'
testlen = 60
benchticker = '^IXIC'
verbose = 'verbose'

if __name__ == '__main__':
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(computerobject.bot_dump, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    reboundranks = rebound_single_event(testrunparent, global_params)
    reboundstocks = reboundranks['STOCK'].tolist()[:30]
    # GET TEST PERIOD PERFORMANCE STATS OF FINAL STRAT POOL
    if calcperfstats == 'yes':
        if len(reboundstocks) != 0:
            getperfstats(verbose, testrunparent, '2020-07-01', testlen, reboundstocks, benchticker)
    playsound('C:\Windows\Media\Ring03.wav')
