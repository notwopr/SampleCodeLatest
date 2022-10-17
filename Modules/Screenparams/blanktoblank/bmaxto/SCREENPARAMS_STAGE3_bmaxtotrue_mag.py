"""
Title: SCREENPARAMS - STAGE 3 - bmaxtotrue_mag
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between bmax graph and true line
    Magnitude of that difference
        unifatscore_bmaxtrue_mean 1/2
        unifatscore_bmaxtrue_median 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_bmaxtotrue_mag',
    'scriptparams': [
        {
            'metricname': 'unifatscore_bmaxtrue_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'trueline',
            'stat_type': 'mean',
            'calibration': 'nopreptrueline',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_bmaxtrue_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'trueline',
            'stat_type': 'median',
            'calibration': 'nopreptrueline',
            'look_back': 0
        }
        ]
    }
