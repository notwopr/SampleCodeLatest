"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 9.00h
Version Start Date: Feb 14, 2021

DESCRIPTION:
STEP 3:
dropscore - cuz it is important the graph suffers little drawdown as possible
+
bmaxflatseglen_max - cuz we want to minimize areas of stagnation.
+
maxdrop - cuz it is important that the graph doesnt have uncharacteristic negative spikes
"""
from STRATTEST_FUNCBASE_RAW import statseglen_single
from STRATTEST_FUNCBASE_MMBM import dropscore_single, allpctdrops_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
dropscoreweight = 1/3
bmaxflatsegweight = 1/3
maxdropweight = 1/3
stage3_params = {
    'scriptname': 'smoothness_rankstagev9h',
    'scriptparams': [
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
        },
        {
            'metricname': 'statseglen_bmaxflat_max',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': bmaxflatsegweight,
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
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
