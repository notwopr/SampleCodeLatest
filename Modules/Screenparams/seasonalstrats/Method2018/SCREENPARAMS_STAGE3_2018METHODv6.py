"""
Title: SCREEN PARAMS - STAGE 3 - 2018 METHOD
Date Started: Oct 4, 2020
Version: 6
Version Start Date: Oct 6, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Description:

    Growth Factor: 1/2
        slopescore

    Shape Factor: 1/2
        unisqueezefactor_mean 1/2
        unisqueezefactor_median 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': '2018METHODv6',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'calibration': 'noprepraw',
            'look_back': 0
        },
        {
            'metricname': 'unisqueezefactor_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'stat_type': 'mean',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'unisqueezefactor_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'stat_type': 'median',
            'calibration': 'squeezeraw',
            'look_back': 0
        }
        ]
    }
