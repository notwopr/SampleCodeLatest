"""
Title: SCREEN PARAMS - STAGE 2 PART I - fall 2020
Date Started: Sept 26, 2020
Version: 1A
Version Start Date: Oct 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Used segbackslopescore.
0.001348 == 63% annualized growth rate
"""
from STRATTEST_FUNCBASE_RAW import segbackslopescore_single


threshold = 0.001348
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2part1_params = {
    'scriptname': 'stage2part1_fall2020v1A',
    'scriptparams': [
        {
            'metricname': 'segbackslopescore_y1',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [''],
            'data': '',
            'focuscol': 'rawprice',
            'segsback': 0,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y2',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [''],
            'data': '',
            'focuscol': 'rawprice',
            'segsback': 1,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y3',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [''],
            'data': '',
            'focuscol': 'rawprice',
            'segsback': 2,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y4',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [''],
            'data': '',
            'focuscol': 'rawprice',
            'segsback': 3,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y5',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [''],
            'data': '',
            'focuscol': 'rawprice',
            'segsback': 4,
            'winlen': 360,
            'look_back': 0
        }
        ]
    }
