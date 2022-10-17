"""
Title: SCREEN PARAMS - segsbackslopescore
Date Started: Jan 18, 2021
Version: 1
Version Start Date: Jan 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

    segbackslopescore_y1 1/5
    segbackslopescore_y2 1/5
    segbackslopescore_y3 1/5
    segbackslopescore_y4 1/5
    segbackslopescore_y5 1/5
"""
from STRATTEST_FUNCBASE_RAW import segbackslopescore_single

focuscol = 'oldbareminraw'
calibration = 'oldbareminraw'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage_params = {
    'scriptname': f'segsbackslopescore_{focuscol}',
    'scriptparams': [
        {
            'metricname': 'segbackslopescore_y1',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/5,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'segsback': 0,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y2',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/5,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'segsback': 1,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y3',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/5,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'segsback': 2,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y4',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/5,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'segsback': 3,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y5',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/5,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'segsback': 4,
            'winlen': 360,
            'look_back': 0
        }
        ]
    }
