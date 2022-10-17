"""
Title: SCREENPARAMS - STAGE 3 - GROWTH - SLOPE COMPONENT
Date Started: Jan 26, 2021
Version: 1.00
Version Start Date: Jan 26, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
Slope Component of Growth Component

"""
from STRATTEST_FUNCBASE_RAW import rollingslopescore_single

focuscol = 'straight'
calibration = 'straight'
lookback = 0
win_len = 360
rollslopeavgweight = 1/2
rollslopedevweight = 1/2

stage3_params = {
    'scriptname': f'rollslopescore_avgplusdev_{focuscol}_LB{lookback}_WL{win_len}',
    'scriptparams': [
        {
            'metricname': 'rollingslopescore_avg',
            'metricfunc': rollingslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': rollslopeavgweight,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'agg_type': 'avg',
            'win_len': win_len,
            'look_back': lookback
        },
        {
            'metricname': 'rollingslopescore_dev',
            'metricfunc': rollingslopescore_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': rollslopedevweight,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'agg_type': 'dev',
            'win_len': win_len,
            'look_back': lookback
        }
        ]
        }
