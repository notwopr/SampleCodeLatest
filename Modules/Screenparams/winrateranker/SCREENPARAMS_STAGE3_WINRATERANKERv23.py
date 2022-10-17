"""
Title: SCREENPARAMS - STAGE 3 - WINRATERANKER
Date Started: Nov 26, 2020
Version: 23.00
Version Start Date: Feb 24, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Screen params.
nonrankdirection is how to rank horizontally the actual raw winrate values (not minmax converted values.  so if it is oldbareminraw winrateranker, then they are the .pct_change values.  How would you rank them.  If minxmax is the ranking system and '1isbest' is the regime, the higher .pctchange is better, so 0 is the correct value here.  If we are using winrate volranker, lower .pct_change values are better.)
"""
from STRATTEST_FUNCBASE_WINRATERANKER import winrateranker
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'WRRtruestdRsWLC2',
    'scriptweight': 0.5,
    'scriptparams': [
        {
            'metricname': 'winrateranker',
            'metricfunc': winrateranker,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'stat_type': 'std',
            'sourcetype': 'trueline',
            'winlen_ceiling': 2,
            'rankmeth': 'standard',
            'rankregime': '1isbest',
            'rawvalrankdirection': 1,
            'metricweight': 1,
            'look_back': 0
        }
        ]
    }
