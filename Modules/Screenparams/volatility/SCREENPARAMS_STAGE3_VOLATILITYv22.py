"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 7, 2021
Version: 22.00
Version Start Date: Apr 14, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
"""
from STRATTEST_FUNCBASE_MMBM import unifatvolscore_single

stage3_params = {
    'scriptname': 'VOLATILITYv22',
    'scriptparams': [
        {
            'metricname': 'unifatvolscore',
            'metricfunc': unifatvolscore_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
        }
