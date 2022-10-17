"""
Title: MAX DRAWDOWN
Date Started: Jan 17, 2021
Version: 1.00
Version Start Date: Jan 17, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
evenly weighs stock age, maxdrop.
"""
from STRATTEST_FUNCBASE_MMBM import allpctdrops_single
from STRATTEST_FUNCBASE_RAW import age_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'maxdrawdown',
    'scriptparams': [
        {
            'metricname': 'allpctdrop_rawoldbareminraw_max',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': '',
            'uppercol': 'rawprice',
            'lowercol': 'oldbareminraw',
            'stat_type': 'min',
            'look_back': 360*2
        },
        {
            'metricname': 'age_older',
            'metricfunc': age_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 360,
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
        }
