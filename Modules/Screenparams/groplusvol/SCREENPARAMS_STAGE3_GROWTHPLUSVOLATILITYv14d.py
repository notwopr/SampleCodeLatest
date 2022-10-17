"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 14.00d
Version Start Date: Aug 13, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Version: Same as 14c except try without redundant unifatscore prong.
1/3 GROWTH
    slopescore (GROWTH)
+
1/3 SMOOTHNESS
    volv13 (SMOOTHNESS)
+
1/3 RATIO
    slopescore/unifatscore ratio (RATIO)

PAST 2 YEARS LOOKBACK PERIOD
"""
from STRATTEST_FUNCBASE_MMBM import slopetounifatratiobmin_single, dropscore_single, allpctdrops_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single, statseglen_single, posnegmag_single, currprice_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single

lookbackperiod = 2 * 365
w_slopescore = 1/3
w_ratio = 1/3
w_smoothness = 1/3
w_volv13_dropscore = 1/5 * w_smoothness
w_volv13_bmaxflatseg = 1/5 * w_smoothness
w_volv13_maxdrop = 1/5 * w_smoothness
w_volv13_posnegmag_negavg = 1/5 * w_smoothness
w_volv13_accretionscore = 1/5 * w_smoothness

stage3_params = {
    'scriptname': 'STAGE3_groplusvolv14d',
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
            'look_back': lookbackperiod
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
            'look_back': lookbackperiod
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
            'look_back': lookbackperiod
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
            'look_back': lookbackperiod
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
            'look_back': lookbackperiod
        },
        {
            'metricname': 'slopetounifatratiobmin',
            'metricfunc': slopetounifatratiobmin_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': w_ratio,
            'focuscol': 'rawprice',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': lookbackperiod
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': w_slopescore,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': lookbackperiod
        }
        ]
        }
