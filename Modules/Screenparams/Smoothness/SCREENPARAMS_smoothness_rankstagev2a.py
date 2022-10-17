"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 2.00a
Version Start Date: Feb 13, 2021

DESCRIPTION: Same as version2 except unifatscore is calculated with rawprice as the denominator.
STEP 3:
RANK HOW CLOSELY THE POSITIVE CURVE HUGS A STRAIGHT LINE
+
ACCRETIONSCORE
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
idealcol = 'baremaxraw'
unifatweight = 1/2
accretionscoreweight = 1/2
stage3_params = {
    'scriptname': 'smoothness_rankstagev2a',
    'scriptparams': [
        {
            'metricname': f'unifatscore_raw{idealcol}_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatweight,
            'focuscol': idealcol,
            'idealcol': 'rawprice',
            'stat_type': 'avg',
            'calibration': [idealcol],
            'data': '',
            'look_back': 0
        },
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
        }
        ]
    }
