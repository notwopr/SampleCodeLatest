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

FILTERS:

"""
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single
filterdir = 'above'
threshold = 0.0011
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2part1_params = {
    'scriptname': f'stage2part1_slopescore_{filterdir}{threshold}',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': filterdir,
            'metricweight': 0,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
