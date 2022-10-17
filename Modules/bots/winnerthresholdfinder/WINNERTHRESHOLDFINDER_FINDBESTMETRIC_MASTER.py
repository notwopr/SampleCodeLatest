"""
Title: WINNER THRESHOLD FINDER BASE - BEST METRIC MASTER
Date Started: Feb 7, 2021
Version: 1.00
Version Start: Feb 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Gets losers and winners for each trial.  For each metric requested, find min and max values for that trial for both loser and winner groups.  If neither group ranges overlap, go to next trial.  If the two groups never overlap for all trials requested, then record metricname with each of its trial's records. Go to next metric in list.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from WINNERTHRESHOLDFINDER_FINDBESTMETRIC_BASE import bestmetricfinder_master
from filelocations import readpkl
from WINNERTHRESHOLDFINDER_PARAMSCRIPTv4 import stage3_params

# if static trial dates...
statictrialbaseloc = computerobject.bot_dump / 'winnerthreshfinder' / 'D20210201T3'
statictrialexistdates = []#readpkl('trialdatedata', statictrialbaseloc)
global_params = {
    'todaysdate': '2021-02-07',
    'testnumber': 2,
    'testregimename': 'bestmetricreporter',
    'metricsetname': 'nasdaq_1yr',
    'num_trials': 1000,
    'testlen': 365,
    'metricscript': stage3_params,
    'benchticker': '^IXIC',
    'winnerdefined': {
        #'beatbench': 'yes',
        'min_gain': 1.00,
        #'max_unifatscore': 'bench',
        'max_unifatscore_bench_err': 0,
        #'max_dropscore': 'bench',
        'max_dropscore_bench_err': 0
    },
    'loserdefined': {
        #'beatbench': 'no',
        'max_gain': 0.30,
        #'min_unifatscore': 'bench',
        'min_unifatscore_bench_err': 0,
        #'min_dropscore': 'bench',
        'min_dropscore_bench_err': 0
    },
    'minimumage': 180,
    'latestdate': '',
    'firstdate': '1995-01-01',
    'statictrialexistdates': statictrialexistdates,
    'statictrialbaseloc': statictrialbaseloc,
    'rankmeth': 'standard',
    'rankregime': '1isbest',
    'savemode': '',
    'chunksize': 5
}


if __name__ == '__main__':
    bestmetricfinder_master(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
