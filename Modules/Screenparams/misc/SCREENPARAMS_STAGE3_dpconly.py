"""
Title: SCREEN PARAMS - STAGE 3 - DPC ONLY
Date Started: Jan 11, 2021
Version: 1
Version Start Date: Jan 11, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: All metrics.
Versions:

"""
from STRATTEST_FUNCBASE_RAW import dpc_cruncher_single

dpctype = 'bmindpc'
mode = 'avg'
stage3_params = {
    'scriptname': f'STAGE3_dpconly_{dpctype}_{mode}',
    'scriptparams': [
        {
            'metricname': f'dpc_cruncher_{dpctype}_{mode}',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': dpctype,
            'mode': mode,
            'look_back': 0
        }
        ]
    }
