"""
Title: STAGE 3 - Age - Older Better
Date Started: Nov 9, 2020
Version: 1.00
Version Start Date: Nov 9, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
    Age
        Age_older
"""
from STRATTEST_FUNCBASE_RAW import age_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_age_olderbetter',
    'scriptweight': 0.5,
    'scriptparams': [
        {
            'metricname': 'age_older',
            'metricfunc': age_single,
            'rankascending': 0,
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
