"""
Title: SCREEN PARAMS - rollingslopescore
Date Started: Jan 18, 2021
Version: 1
Version Start Date: Jan 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

"""
from STRATTEST_FUNCBASE_RAW import rollingslopescore_single

focuscol = 'rawprice'
calibration = None
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage_params = {
    'scriptname': f'rollingslopescore_avg_{focuscol}',
    'scriptparams': [
        {
            'metricname': 'rollingslopescore_avg',
            'metricfunc': rollingslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [calibration],
            'data': '',
            'focuscol': focuscol,
            'agg_type': 'avg',
            'win_len': 360,
            'look_back': 0
        }
        ]
    }
