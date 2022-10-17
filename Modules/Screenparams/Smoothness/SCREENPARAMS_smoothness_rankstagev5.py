"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 5.00
Version Start Date: Feb 13, 2021

DESCRIPTION:
STEP 3:
RANK HOW CLOSELY THE POSITIVE CURVE HUGS A BAREMAXRAW
 +
HOW CLOSE IT HUGS THE OLDBAREMINRAW LINE
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
topidealcol = 'baremaxraw'
bmaxweight = 1/2
bminweight = 1/2

stage3_params = {
    'scriptname': 'smoothness_rankstagev5',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawbaremaxraw_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': bmaxweight,
            'focuscol': 'baremaxraw',
            'idealcol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': bminweight,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'avg',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        }
        ]
    }
