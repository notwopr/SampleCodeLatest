"""
Title: SCREENPARAMS - STAGE 3 - bmaxtotrue_reg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between bmax graph and true line
    Regularity of that difference
        unifatscore_bmaxtrue_std 1/2
        unifatscore_bmaxtrue_mad 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_bmaxtotrue_reg',
    'scriptparams': [
        {
            'metricname': 'unifatscore_bmaxtrue_std',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'trueline',
            'stat_type': 'std',
            'calibration': 'nopreptrueline',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_bmaxtrue_mad',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'trueline',
            'stat_type': 'mad',
            'calibration': 'nopreptrueline',
            'look_back': 0
        }
        ]
    }