"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 3.00
Version Start Date: Feb 13, 2021

DESCRIPTION:
STEP 3:
RANK HOW CLOSELY THE POSITIVE CURVE HUGS A STRAIGHT LINE + dev of same
+
ACCRETIONSCORE
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
idealcol = 'baremaxraw'
unifatweightavg = 1/4
unifatweightdev = 1/4
accretionscoreweight = 1/2
stage3_params = {
    'scriptname': 'smoothness_rankstagev3',
    'scriptparams': [
        {
            'metricname': f'unifatscore_raw{idealcol}_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatweightavg,
            'focuscol': 'rawprice',
            'idealcol': idealcol,
            'stat_type': 'avg',
            'calibration': [idealcol],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': f'unifatscore_raw{idealcol}_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatweightdev,
            'focuscol': 'rawprice',
            'idealcol': idealcol,
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
