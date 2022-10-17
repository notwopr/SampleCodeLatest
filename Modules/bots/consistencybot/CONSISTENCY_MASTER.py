"""
Title: CONSISTENCY BOT MASTER
Date Started: Dec 6, 2020
Version: 1.00
Version Start: Dec 6, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  To calculate probability if a stock experiences gain X in one period, what is the probability that it'll experience the same gain in the next period.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from CONSISTENCY_BASE import consistencybotmaster
from STRATTEST_FUNCBASE_RAW import unifatshell_single

# if static trial dates...
staticdatesource = computerobject.bot_important / 'PULLOUTBOT' / 'overallstats_alltrialsummaries.csv'
alltrialsdf = pd.read_csv(staticdatesource)
alltrialsdf.sort_values(by='trialno', inplace=True, ascending=True)
statictrialexistdates = []#alltrialsdf['test_beg'].to_list()

global_params = {
    'todaysdate': '2020-12-30',
    'testnumber': 24,
    'testregimename': 'consistencybot',
    'err_prev': 0.10,
    'err_next': 0.50,
    'gain_prev': 0.80,
    'gain_next': 0.50,
    'mode': 'split',
    'filter_daterange': 'prev',
    'filterqualifiers_prev': 'no',
    'prev_filters': [
            {
                'metricname': 'unifatscore_rawtrue_mean',
                'metricfunc': unifatshell_single,
                'rankascending': 1,
                'threshold': 0.25,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 1,
                'focuscol': 'rawprice',
                'idealcol': 'trueline',
                'stat_type': 'mean',
                'calibration': 'nopreptrueline',
                'look_back': 0
            }
            ],
    'len_prev': 365,
    'len_next': 365,
    'num_trials': 100,
    'latestdate': '',
    'firstdate': '1990-01-01',
    'statictrialexistdates': statictrialexistdates,
    'verbose': ''
}


if __name__ == '__main__':
    consistencybotmaster(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
