"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 7, 2021
Version: 11.00
Version Start Date: Jan 20, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Versions:
11: same as v10 except add fattiness back in.
Description:
DPC
    NEGDPC MAG AVG
        posnegmag_neg_avg
    NEGDPC PREVALENCE
        posnegprevalence_neg
DROP STATS
    drop_score (dropprevalence * dropmag)
FATTINESS
    unifatscore_rawbaremaxraw_avg
    unifatscore_rawbaremaxraw_dev
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, unifatshell_single
from STRATTEST_FUNCBASE_RAW import posnegmag_single, posnegprevalence_single

dropmetrics_total = 1/3
posnegprevalence_negweight = 1/6
posnegmag_negweight = 1/6
unifatscoreweight = 1/6
unifatscoredevweight = 1/6

stage3_params = {
    'scriptname': 'VOLATILITYv11',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawbaremaxraw_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoreweight,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawbaremaxraw_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoredevweight,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'dev',
            'calibration': ['baremaxraw'],
            'data': '',
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
