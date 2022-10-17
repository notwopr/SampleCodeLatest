"""
Title: SCREENPARAMS - STAGE 3 - rawtostraight_reg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and straight line
    Regularity of that difference
        unifatscore_rawstraight_std 1/2
        unifatscore_rawstraight_mad 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_rawtostraight_reg',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawstraight_std',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'std',
            'calibration': 'noprepraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawstraight_mad',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'mad',
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
    }
