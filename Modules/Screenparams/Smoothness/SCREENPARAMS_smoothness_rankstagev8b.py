"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 8.00b
Version Start Date: Feb 13, 2021

DESCRIPTION:
STEP 3:
RANK HOW CLOSELY THE POSITIVE CURVE HUGS A BAREMAXRAW
 +
HOW CLOSE IT HUGS THE OLDBAREMINRAW LINE
+
HOW CLOSE IT HUGS THE true LINE
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
bmaxweight = 1/3*1/2
bminweight = 1/3*1/2
trueweight = 1/3*1/2
accretionscoreweight = 1/2
stage3_params = {
    'scriptname': 'smoothness_rankstagev8b',
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
        },
        {
            'metricname': 'unifatscore_rawtrue_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': trueweight,
            'focuscol': 'rawprice',
            'idealcol': 'trueline',
            'stat_type': 'avg',
            'calibration': ['trueline'],
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
