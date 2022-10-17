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

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'stage3_slopescoremaxdrawdown',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'calibration': 'noprepraw',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_max',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'calibration': 'smoothraw',
            'stat_type': 'max',
            'look_back': 0
        }
        ]
    }
