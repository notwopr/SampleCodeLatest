"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 7, 2021
Version: 9.00
Version Start Date: Jan 19, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Versions:
9: replace negdpcmag and prev with one indexscore
Description:
CONSECUTIVE NEGDPC
    NEGSEG AVG
        statseglen_neg_avg
DPC
    POSNEGMAGPREVSCORE_NEG_AVG
DROP STATS
    drop_score (dropprevalence * dropmag)
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single
from STRATTEST_FUNCBASE_RAW import statseglen_single, posnegmagprevscore_single

dropmetrics_total = 1/3
posnegdpc_negweight = 1/3
avgnegseglenweight = 1/3

stage3_params = {
    'scriptname': 'VOLATILITYv9',
    'scriptparams': [
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
            'metricname': 'posnegmagprevscore_neg_avg',
            'metricfunc': posnegmagprevscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'avg',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': dropmetrics_total,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
        }
