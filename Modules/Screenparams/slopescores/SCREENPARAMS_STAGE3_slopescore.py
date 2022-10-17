"""
Title:  SCREEN PARAMS - SLOPESCORE ONLY
Date Started: Nov 5, 2020
Version: 1.00
Version Start Date: Nov 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

FILTERS:

"""
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single

focuscol = 'rawprice'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_slopescoreonly_{focuscol}',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': focuscol,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
