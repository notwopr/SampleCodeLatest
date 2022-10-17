"""
Title: WINNERTHRESHOLD FINDER PARAMSCRIPT
Date Started: Jan 30, 2021
Version: 5.00
Version Start Date: Feb 19, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single
from STRATTEST_FUNCBASE_RAW import posnegmag_single, statseglen_single, currprice_single, paratio_single, psegnegsegratio_single, dollarsperday_single, posnegmagratio_single, posnegprevratio_single, consecsegprev_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single


stage3_params = {
    'scriptname': 'winnerthresholdfinderv5',
    'scriptparams': [
        {
            'metricname': 'statseglen_bmaxflat_max',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'look_back': 0
        },
        {
            'metricname': 'accretionscore_pos',
            'metricfunc': accretionscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'accret_type': 'pos',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'accretionscore_neg',
            'metricfunc': accretionscore_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'accret_type': 'neg',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'accretionscore_zero',
            'metricfunc': accretionscore_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'accret_type': 'zero',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'currentprice',
            'metricfunc': currprice_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'dollarsperday',
            'metricfunc': dollarsperday_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'priceageratio',
            'metricfunc': paratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'psegnegsegratio_avg',
            'metricfunc': psegnegsegratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'stat_type': 'avg',
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagratio',
            'metricfunc': posnegmagratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'stat_type': 'avg',
            'metricweight': 1,
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevratio',
            'metricfunc': posnegprevratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [''],
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
            'metricweight': 1,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
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
            'metricweight': 1,
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
            'metricweight': 1,
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
            'metricweight': 1,
            'numer_type': 'neg',
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        }
        ]
        }
