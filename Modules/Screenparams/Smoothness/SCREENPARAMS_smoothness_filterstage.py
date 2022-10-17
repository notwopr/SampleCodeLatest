"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 1.00
Version Start Date: Feb 13, 2021

DESCRIPTION:
STEP 1:
FILTER OUT NON POSITIVE SLOPES
STEP 2:
FILTER OUT THOSE WHOSE SUCCESSIVE VALUES ARE NOT ALWAYS GREATER THAN THEIR PREVIOUS VALUES (OR INSTEAD RANK THEM)
"""
from STRATTEST_FUNCBASE_SMOOTHNESS import positiveslope_single, accretionscore_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'smoothness_filterstage',
    'scriptparams': [
        {
            'metricname': 'positiveslope',
            'metricfunc': positiveslope_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'accretionscore',
            'metricfunc': accretionscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'equalabove',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 0
        }
        ]
    }
