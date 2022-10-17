"""
Title:  SCREEN PARAMS - STAGE 2 - REBOUND BOT
Date Started: Nov 19, 2020
Version: 1.00
Version Start Date: Jan 11, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Filter layer for rebound bot
Versions:

FILTERS:

"""
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single
lookback = 360*4
stage2_params = {
    'scriptname': 'reboundbot_stage2',
    'scripttype': 'filter',
    'crashlookbacklen': lookback,
    'crashbenchticker': '^IXIC',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
