"""
Title: SCREENPARAM - positiveslope fcf plus revenue - FILTER
Date Started: Mar 4, 2021
Version: 1.00
Version Start Date: Mar 4, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description: Params for getting current marketcap.
"""
from STRATTEST_FUNCBASE_FUNDAMENTALS import fundypositiveslope_single

filterd = 'above'
threshold = 0
look_back = 0
datatype = 'revenue'
datatype1 = 'freecashflow'
stage2_params = {
    'scriptname': f'pslope_{datatype}and{datatype1}FILTER{filterd}{threshold}_LB{look_back}',
    'scriptparams': [
        {
            'metricname': f'fundypositiveslope_{datatype}',
            'metricfunc': fundypositiveslope_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': filterd,
            'metricweight': 1,
            'datatype': datatype,
            'calibration': [],
            'data': '',
            'look_back': look_back
        },
        {
            'metricname': f'fundypositiveslope_{datatype1}',
            'metricfunc': fundypositiveslope_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': filterd,
            'metricweight': 1,
            'datatype': datatype1,
            'calibration': [],
            'data': '',
            'look_back': look_back
        }
        ]
        }
