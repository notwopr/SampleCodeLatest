"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Oct 29, 2020
Version: 1.00
Version Start Date: Oct 29, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
evenly weighs stock age, maxdrop.
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_ageyoungermaxdrop',
    'scriptparams': [
        {
            'metricname': 'maxdrop',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.25,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'calibration': 'noprepraw',
            'look_back': 0
        },
        {
            'metricname': 'age_younger',
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 180,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
        }
