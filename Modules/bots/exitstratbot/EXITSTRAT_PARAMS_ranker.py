"""
Title: EXIT STRAT PARAMS - FILTER PARAMS
Date Started: Dec 1, 2020
Version: 1.00
Version Start: Dec 1, 2020
Author: David Hyongsik Choi
slopescore + unifatscore_rawstraight_avg
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'exitstratparams',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2),
            'calibration': 'noprepraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawstraight_avg',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'avg',
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
    }
