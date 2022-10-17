"""
Title: SCREENPARAMS - STAGE 3 - WINRATERANKER
Date Started: Nov 26, 2020
Version: 20.00
Version Start Date: Nov 26, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Screen params.
nonrankdirection is how to rank horizontally the actual raw winrate values (not minmax converted values.  so if it is oldbareminraw winrateranker, then they are the .pct_change values.  How would you rank them.  If minxmax is the ranking system and '1isbest' is the regime, the higher .pctchange is better, so 0 is the correct value here.  If we are using winrate volranker, lower .pct_change values are better.)
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'winraterankerv20',
    'scriptparams': [
        {
            'metricname': 'winrateranker_bmin_mad',
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'stat_type': 'mad',
            'sourcetype': 'oldbareminraw',
            'winlen_ceiling': 2,
            'rankmeth': 'standard',
            'rankregime': '1isbest',
            'rawvalrankdirection': 0,
            'metricweight': 1,
            'look_back': 0
        }
        ]
    }
