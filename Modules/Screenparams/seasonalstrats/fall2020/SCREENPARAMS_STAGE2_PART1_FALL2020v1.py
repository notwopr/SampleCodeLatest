"""
Title:  SCREEN PARAMS - STAGE 2 PART I - SLOPESCORE ONLY
Date Started: July 25, 2020
Version: 1.00
Version Start Date: Oct 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single
stage2part1_params = {
    'scriptname': 'stage2part1_fall2020v1',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.000905,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
