"""
Title:  MANUAL REVIEW SCRIPT - PARAMSCRIPT FOR GRAPH GRADING
Date Started: Nov 4, 2020
Version: 1.00
Version Start Date: Nov 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Components:
max any-timespan drops 1
    allpctdrop_rawoldbareminraw_max


"""
from STRATTEST_FUNCBASE_MMBM import allpctdrops_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'stage3_maxdrawdown',
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
            'look_back': 0
        }
        ]
    }
