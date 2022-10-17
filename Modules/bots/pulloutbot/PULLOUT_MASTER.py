"""
Title: PULLOUT BOT MASTER
Date Started: Nov 17, 2020
Version: 1.00
Version Start: Nov 17, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  To tell you when and if you should exit a position in a stock based on the likelihood it will end up beating the market by the end of the testperiod.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from PULLOUT_BASE import pulloutbotmaster
from filelocations import readpkl

# if static trial dates...
statictrialexistdates = readpkl('trialdatedata', computerobject.bot_dump / 'pulloutbot' / 'D20210115T4')

global_params = {
    'todaysdate': '2021-01-15',
    'testnumber': 4,
    'testregimename': 'pulloutbot',
    'metricsetname': 'pullout_1000trials_nasdaq_1yr',
    'num_trials': 1000,
    'testlen': 365,
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
    'latestdate': '',
    'firstdate': '1990-01-01',
    'statictrialexistdates': statictrialexistdates
}


if __name__ == '__main__':
    pulloutbotmaster(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
