"""
Title:  SCREEN PARAMS - STAGE 3 - REBOUNDBOT - LOSS COMPONENT
Date Started: Jan 8, 2021
Version: 1.00
Version Start Date: Jan 8, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description: The loss paramscript for the rebound bot.
"""
from STRATTEST_FUNCBASE_RAW import getpctchange_single


# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'stage3_reboundbot_losscomponent',
    'scriptparams': [
        {
            'metricname': 'crasheventloss',
            'metricfunc': getpctchange_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
