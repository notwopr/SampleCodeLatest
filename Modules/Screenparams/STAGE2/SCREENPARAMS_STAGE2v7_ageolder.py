"""
Title:  SCREEN PARAMS - STAGE 2 FILTERS
Date Started: Jan 21, 2021
Version: 7
Version Start Date: Aug 13, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
7: don't eliminate by dropscore or maxdrop thresholds.  only age at this stage.
FILTERS:
age >= 2 yrs
"""
from STRATTEST_FUNCBASE_RAW import age_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'STAGE2FILTERSv7_ageolder',
    'scriptparams': [
        {
            'metricname': 'age_older',
            'metricfunc': age_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1.5*365,
            'filterdirection': 'equalabove',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
