"""
Title: SCREENPARAMS - STAGE 3 - rawtosbmin_mag REV
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and oldbareminraw line
    Magnitude of that difference
        unifatscore_rawoldbareminraw_mean 1/2
        unifatscore_rawoldbareminraw_median 1/2

"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_rawtobmin_mag_REV',
    'datasourcetype': 'revenue',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawoldbareminraw_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mean',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_median',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        }
        ]
    }
