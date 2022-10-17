"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Nov 9, 2020
Version: 1.00
Version Start Date: Nov 9, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
Growth 1/2
    slopescore 1/2
Loss 1/2
    age 1/2
    maxdrawdown 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_slopescoreageoldermaxdrop',
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
            'metricweight': (1/2)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'max',
            'look_back': 0
        },
        {
            'metricname': 'age',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 180,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'calibration': 'age',
            'look_back': 0
        }
        ]
        }
