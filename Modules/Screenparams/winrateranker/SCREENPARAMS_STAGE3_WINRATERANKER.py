"""
Title: SCREENPARAMS - STAGE 3 - WINRATERANKER
Date Started: Sept 29, 2020
Version: 2.00
Version Start Date: Nov 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Screen params.
Versions:
2: convert syntax.
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_winrateranker_bmin_avg',
    'scriptparams': [
        {
            'metricname': 'winrateranker_true_std',
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'stat_type': 'avg',
            'sourcetype': 'oldbareminraw',
            'rankmeth': 'minmax',
            'rankregime': '1isbest',
            'nonrankdirection': 1,
            'metricweight': 1,
            'look_back': 0
        }
        ]
    }
