"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 16
Version Start Date: Aug 16, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Version:
16: same as 15 version but separate smooth and growth components out.
SMOOTHNESS
    volv13 (SMOOTHNESS)

"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, allpctdrops_single
from STRATTEST_FUNCBASE_RAW import statseglen_single, posnegmag_single, currprice_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single

smooth_lbp = 5 * 365
w_smoothness = 1
w_volv13_dropscore = 1/5 * w_smoothness
w_volv13_bmaxflatseg = 1/5 * w_smoothness
w_volv13_maxdrop = 1/5 * w_smoothness
w_volv13_posnegmag_negavg = 1/5 * w_smoothness
w_volv13_accretionscore = 1/5 * w_smoothness

stage3_params = {
    'scriptname': 'STAGE3_groplusvolv16smooth',
    'scriptparams': [
        {
            'metricname': 'currentprice',
            'metricfunc': currprice_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 100,
            'filterdirection': 'no',
            'metricweight': 0,
            'calibration': [],
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
            'metricweight': w_volv13_accretionscore,
            'focuscol': 'rawprice',
            'accret_type': 'pos',
            'calibration': [''],
            'data': '',
            'look_back': smooth_lbp
        },
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': w_volv13_dropscore,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': smooth_lbp
        },
        {
            'metricname': 'statseglen_bmaxflat_max',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': w_volv13_bmaxflatseg,
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'look_back': smooth_lbp
        },
        {
            'metricname': 'allpctdrop_rawbaremaxraw_max',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.70,
            'filterdirection': 'no',
            'metricweight': w_volv13_maxdrop,
            'calibration': ['baremaxraw'],
            'data': '',
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'min',
            'look_back': smooth_lbp
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
            'metricweight': w_volv13_posnegmag_negavg,
            'calibration': [],
            'data': 'dpc',
            'look_back': smooth_lbp
        }
        ]
        }