"""
Title: WINNER THRESHOLD FINDER MASTER
Date Started: Jan 28, 2021
Version: 1.00
Version Start: Jan 28, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Over several trials, finds the metricvalue ranges of winning stocks.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from WINNERTHRESHOLDFINDER_BASE import winnerthreshfinder_master
from filelocations import readpkl
from WINNERTHRESHOLDFINDER_PARAMSCRIPTv5 import stage3_params
from WINNERTHRESHOLDFINDER_ADDLWINNERFILTERSv2 import filter_params
# if static trial dates...
statictrialbaseloc = computerobject.bot_dump / 'winnerthreshfinder' / 'D20210217T5'
statictrialexistdates = readpkl('trialdatedata', statictrialbaseloc)
global_params = {
    'todaysdate': '2021-02-19',
    'testnumber': 1,
    'testregimename': 'winnerthreshfinder',
    'metricsetname': 'nasdaq_1yr_1000trials',
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
        'max_dropscore_bench_err': 0,
        'addlpretestfilters': filter_params
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
    winnerthreshfinder_master(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
