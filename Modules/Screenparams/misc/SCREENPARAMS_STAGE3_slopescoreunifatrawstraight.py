"""
Title:  MANUAL REVIEW SCRIPT - PARAMSCRIPT FOR GRAPH GRADING
Date Started: Nov 9, 2020
Version: 1.00
Version Start Date: Nov 9, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Components:
Growth 1/2
    slopescore
Noise 1/2
    unifatscore_rawstraight_mean 1/2
    unifatscore_rawstraight_median 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'stage3_slopescoreunifatrawstraight',
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
            'metricname': 'unifatscore_rawstraight_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': 'noprepraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawstraight_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
    }
