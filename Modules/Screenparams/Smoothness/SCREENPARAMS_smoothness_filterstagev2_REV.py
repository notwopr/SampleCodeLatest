"""
Title: smoothness - filterstage
Date Started: Feb 13, 2021
Version: 2.00
Version Start Date: Feb 13, 2021

DESCRIPTION:
STEP 1:
FILTER OUT NON POSITIVE SLOPES
"""
from STRATTEST_FUNCBASE_SMOOTHNESS import positiveslope_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'smoothness_filterstagev2',
    'datasourcetype': 'revenue',
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
        }
        ]
    }
