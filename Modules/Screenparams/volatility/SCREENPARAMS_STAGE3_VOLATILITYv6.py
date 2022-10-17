"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 7, 2021
Version: 6.00
Version Start Date: Jan 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
CONSECUTIVE NEGDPC
    NEGSEG AVG
        statseglen_neg_avg
DPC
    NEGDPC MAG AVG
        posnegmag_neg_avg
    NEGDPC PREVALENCE
        posnegprevalence_neg
FATTINESS
    unifatscore_rawtrue_avg
    unifatscore_rawtrue_dev
DROP STATS
    drop_score (dropprevalence * dropmag)
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, unifatshell_single
from STRATTEST_FUNCBASE_RAW import posnegmag_single, posnegprevalence_single, statseglen_single

dropmetrics_total = 1/4
unifatscoreweight = 1/8
unifatscoredevweight = 1/8
posnegprevalence_negweight = 1/8
posnegmag_negweight = 1/8
avgnegseglenweight = 1/4

stage3_params = {
    'scriptname': 'VOLATILITYv6',
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
            'metricname': 'posnegmag_neg_avg',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'avg',
            'metricweight': posnegmag_negweight,
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
            'metricname': 'unifatscore_rawtrue_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoreweight,
            'focuscol': 'rawprice',
            'idealcol': 'trueline',
            'stat_type': 'avg',
            'calibration': ['trueline'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawtrue_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoredevweight,
            'focuscol': 'rawprice',
            'idealcol': 'trueline',
            'stat_type': 'dev',
            'calibration': ['trueline'],
            'data': '',
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
