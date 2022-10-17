"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 1.00
Version Start Date: Feb 13, 2021

DESCRIPTION:
STEP 3:
RANK HOW CLOSELY THE POSITIVE CURVE HUGS A STRAIGHT LINE
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
idealcol = 'baremaxraw'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'smoothness_rankstage',
    'scriptparams': [
        {
            'metricname': f'unifatscore_raw{idealcol}_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': idealcol,
            'stat_type': 'avg',
            'calibration': [idealcol],
            'data': '',
            'look_back': 0
        }
        ]
    }
