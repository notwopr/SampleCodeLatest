"""
Title: smoothness
Date Started: Feb 17, 2021
Version: 10.00
Version Start Date: Feb 17, 2021

DESCRIPTION:
STEP 3:
ACCRETIONSCORE_pos - cuz it is important that the graph is consistently growing
ACCRETIONSCORE_neg
ACCRETIONSCORE_zero
"""
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
accretionscore_posweight = 1/3
accretionscore_negweight = 1/3
accretionscore_zeroweight = 1/3
stage3_params = {
    'scriptname': 'smoothness_rankstagev10',
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
        },
        {
            'metricname': 'accretionscore_neg',
            'metricfunc': accretionscore_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': accretionscore_negweight,
            'focuscol': 'rawprice',
            'accret_type': 'neg',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'accretionscore_zero',
            'metricfunc': accretionscore_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': accretionscore_zeroweight,
            'focuscol': 'rawprice',
            'accret_type': 'zero',
            'calibration': [''],
            'data': '',
            'look_back': 0
        }
        ]
    }
