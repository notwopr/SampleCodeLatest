"""
Title: smoothness
Date Started: Feb 17, 2021
Version: 10.00c
Version Start Date: Feb 22, 2021

DESCRIPTION:
STEP 3:
ACCRETIONSCORE_pos - cuz it is important that the graph is consistently growing
"""
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
accretionscore_posweight = 1
stage3_params = {
    'scriptname': 'smoothness_rankstagev10c',
    'scriptparams': [
        {
            'metricname': 'accretionscore_pos',
            'metricfunc': accretionscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': accretionscore_posweight,
            'focuscol': 'rawprice',
            'accret_type': 'pos',
            'calibration': [''],
            'data': '',
            'look_back': 0
        }
        ]
    }
