"""
Title: SCREEN PARAMS - combining straight slopescore, segsbackslope, and rollingslope
Date Started: Jan 18, 2021
Version: 1
Version Start Date: Jan 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
segbackslopescore
    segbackslopescore_y1 1/5
    segbackslopescore_y2 1/5
    segbackslopescore_y3 1/5
    segbackslopescore_y4 1/5
    segbackslopescore_y5 1/5
rollingslopescore
straight slopescore
"""
from STRATTEST_FUNCBASE_RAW import segbackslopescore_single, slopescorefocus_single, rollingslopescore_single

focuscol = 'rawprice'
calibration = None
straightslopeweight = 1/3
rollingslopeweight_avg = (1/3) * (1/2)
rollingslopeweight_dev = (1/3) * (1/2)
segsbackslopeweight = (1/3) * (1/5)
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'slopescorecompositev1_{focuscol}',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': straightslopeweight,
            'focuscol': focuscol,
            'calibration': [calibration],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y1',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': segsbackslopeweight,
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
            'metricweight': segsbackslopeweight,
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
            'metricweight': segsbackslopeweight,
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
            'metricweight': segsbackslopeweight,
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
            'metricweight': segsbackslopeweight,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'segsback': 4,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'rollingslopescore_avg',
            'metricfunc': rollingslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': rollingslopeweight_avg,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'agg_type': 'avg',
            'win_len': 360,
            'look_back': 0
        },
        {
            'metricname': 'rollingslopescore_dev',
            'metricfunc': rollingslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': rollingslopeweight_dev,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'agg_type': 'dev',
            'win_len': 360,
            'look_back': 0
        }
        ]
    }
