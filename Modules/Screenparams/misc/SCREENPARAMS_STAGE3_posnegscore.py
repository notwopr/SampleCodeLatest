"""
Title: STAGE 3 - posnegscore
Date Started: Dec 19, 2020
Version: 1.0
Version Start Date: Dec 19, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

"""
from STRATTEST_FUNCBASE_RAW import posnegscore_single
avgmeth = 'median'
devmeth = 'mad'

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_posnegscore_{avgmeth}_{devmeth}',
    'scriptparams': [
        {
            'metricname': f'posnegscore_{avgmeth}_{devmeth}',
            'metricfunc': posnegscore_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'avgmeth': avgmeth,
            'devmeth': devmeth,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': 'raw',
            'look_back': 0
        }
        ]
    }
