"""
Title: STAGE 3 - Current Price
Date Started: Nov 2, 2020
Version: 1.00
Version Start Date: Nov 2, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
evenly weighs stock age, maxdrop.
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_currprice',
    'scriptparams': [
        {
            'metricname': 'currentprice',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
        }
