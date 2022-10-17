"""
Title: SCREENPARAMS - STAGE 3 - rawtostraight_mag REV
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and straight line
    Magnitude of that difference
        unifatscore_rawstraight_mean 1/2
        unifatscore_rawstraight_median 1/2

"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_rawtostraight_mag_REV',
    'datasourcetype': 'revenue',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawstraight_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': ['straight'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawstraight_median',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': ['straight'],
            'data': '',
            'look_back': 0
        }
        ]
    }
