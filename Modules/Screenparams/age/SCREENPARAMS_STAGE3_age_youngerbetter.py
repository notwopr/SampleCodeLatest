"""
Title: STAGE 3 - Age - Younger Better
Date Started: Nov 9, 2020
Version: 1.00
Version Start Date: Nov 9, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
    Age
        Age_younger
"""
from STRATTEST_FUNCBASE_RAW import age_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_age_youngerbetter',
    'scriptparams': [
        {
            'metricname': 'age_younger',
            'metricfunc': age_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 180,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
        }
