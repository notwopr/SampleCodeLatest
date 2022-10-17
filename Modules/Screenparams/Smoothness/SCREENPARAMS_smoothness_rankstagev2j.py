"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 2.00j
Version Start Date: Feb 13, 2021

DESCRIPTION: Previous version 2a doesn't catch cases where the avg negdpc is large compared to the typical posdpc.
We should control for maxnegdpc and avgnegdpc
STEP 3:
RANK HOW CLOSELY THE POSITIVE CURVE HUGS A BAREMAXRAW
 +
HOW CLOSE IT HUGS THE OLDBAREMINRAW LINE
+
NEGDPC
    AVG NEGDPC tradeonlydpc
    negdpc prev
    posnegmagratio tradeonlydpc
+
CONSECDPC
    AVG NEG
    PSEGNEGSEGRATIO
    consecsegprev_neg
+
maxdrop
+
ACCRETIONSCORE

prevalence, magnitude, ratio
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single, allpctdrops_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single
from STRATTEST_FUNCBASE_RAW import posnegmag_single, posnegmagratio_single, statseglen_single, psegnegsegratio_single, consecsegprev_single, posnegprevalence_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
bmaxweight = 1/6
bminweight = 1/6
accretionscoreweight = 1/3
posnegmag_negavgweight = 1/21
posnegprevalence_negweight = 1/21
posnegmagratioweight = 1/21
avgnegseglenweight = 1/21
psegnegsegratioweight = 1/21
consecsegprevweight = 1/21
maxdropweight = 1/21
stage3_params = {
    'scriptname': 'smoothness_rankstagev2j',
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
            'metricname': 'posnegprevalence_neg',
            'metricfunc': posnegprevalence_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'metricweight': posnegprevalence_negweight,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagratiotrade',
            'metricfunc': posnegmagratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'stat_type': 'avg',
            'metricweight': posnegmagratioweight,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_neg_avg',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': avgnegseglenweight,
            'mode': 'negative',
            'stat_type': 'avg',
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'psegnegsegratio',
            'metricfunc': psegnegsegratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': psegnegsegratioweight,
            'stat_type': 'avg',
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'consecsegprev_neg',
            'metricfunc': consecsegprev_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': consecsegprevweight,
            'numer_type': 'neg',
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
        },
        {
            'metricname': 'allpctdrop_rawbaremaxraw_max',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.70,
            'filterdirection': 'no',
            'metricweight': maxdropweight,
            'calibration': ['baremaxraw'],
            'data': '',
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'min',
            'look_back': 0
        }
        ]
    }
