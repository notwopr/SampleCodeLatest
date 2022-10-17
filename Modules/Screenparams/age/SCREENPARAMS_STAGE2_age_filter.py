"""
Title: STAGE 2 - Age - Filter
Date Started: Jan 5, 2021
Version: 1.00
Version Start Date: Jan 5, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
"""
from STRATTEST_FUNCBASE_RAW import age_single

filterdir = 'below'
threshval = 1295
stage2_params = {
    'scriptname': f'STAGE2_age_filter{filterdir}{threshval}',
    'scriptparams': [
        {
            'metricname': 'age_older',
            'metricfunc': age_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshval,
            'filterdirection': filterdir,
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
        }
