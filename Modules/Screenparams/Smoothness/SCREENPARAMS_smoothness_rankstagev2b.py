"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 2.00b
Version Start Date: Feb 13, 2021

DESCRIPTION: Previous version 2a doesn't catch cases where the avg negdpc is large compared to the typical posdpc.
We should control for maxnegdpc and avgnegdpc
STEP 3:
RANK HOW CLOSELY THE POSITIVE CURVE HUGS A STRAIGHT LINE
+
NEGDPC
    AVG NEGDPC
    MAX NEGDPC
+
ACCRETIONSCORE
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
from STRATTEST_FUNCBASE_RAW import posnegmag_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
idealcol = 'baremaxraw'
unifatweight = 1/3
accretionscoreweight = 1/3
posnegmag_negavgweight = 1/6
posnegmag_negmaxweight = 1/6
stage3_params = {
    'scriptname': 'smoothness_rankstagev2b',
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
            'metricname': 'posnegmagtrade_neg_avg',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'avg',
            'metricweight': posnegmag_negavgweight,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagtrade_neg_max',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'min',
            'metricweight': posnegmag_negmaxweight,
            'calibration': [],
            'data': 'dpc',
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
