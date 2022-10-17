"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 9.00
Version Start Date: Feb 14, 2021

DESCRIPTION:
STEP 3:
dropscore - cuz it is important the graph suffers little drawdown as possible
+
ACCRETIONSCORE - cuz it is important that the graph is consistently growing
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
dropscoreweight = 1/2
accretionscoreweight = 1/2
stage3_params = {
    'scriptname': 'smoothness_rankstagev9',
    'scriptparams': [
        {
            'metricname': 'accretionscore',
            'metricfunc': accretionscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': accretionscoreweight,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': dropscoreweight,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
    }
