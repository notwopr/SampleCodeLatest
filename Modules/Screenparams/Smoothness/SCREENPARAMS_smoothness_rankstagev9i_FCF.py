"""
Title: smoothness
Date Started: Feb 13, 2021
Version: 9.00i
Version Start Date: Feb 14, 2021

DESCRIPTION:
STEP 3:
dropscore - cuz it is important the graph suffers little drawdown as possible
+
bmaxflatseglen_max - cuz we want to minimize areas of stagnation.
+
maxdrop - cuz it is important that the graph doesnt have uncharacteristic negative spikes
+
negdpc mag avg tradeonlydpc - negdpc, important is avg dpc is high

"""
from STRATTEST_FUNCBASE_RAW import statseglen_single, posnegmag_single
from STRATTEST_FUNCBASE_MMBM import dropscore_single, allpctdrops_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
dropscoreweight = 1/4
bmaxflatsegweight = 1/4
maxdropweight = 1/4
posnegmag_negavgweight = 1/4
stage3_params = {
    'scriptname': 'smoothness_rankstagev9i_FCF',
    'datasourcetype': 'freecashflow',
    'scriptweight': 0.5,
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
        }
        ]
    }
