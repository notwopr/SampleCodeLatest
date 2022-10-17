"""
Title: SCREEN PARAMS - STAGE 3 - 2018 METHOD VERSION 4
Date Started: Oct 4, 2020
Version: 4
Version Start Date: Oct 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Description:

    Growth Factor: 1/2
        slopescore

    Shape Factor: 1/2
        squeezearea
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': '2018METHODv4',
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
            'metricname': 'squeezearea',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1/2,
            'stat_type': 'area',
            'calibration': 'squeezeraw',
            'look_back': 0
        }
        ]
    }
