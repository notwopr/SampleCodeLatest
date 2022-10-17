"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 15.00g
Version Start Date: Oct 31, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Version: 15 is one component in combining several different LB periods of the same scheme.
V15d.1: added dropscoreratio info param
v15g: same as 15d but uses volatilityv27 for the SMOOTHNESS COMPONENT.
1/3 GROWTH
    slopescore (GROWTH) [LB shorter]
+
1/3 SMOOTHNESS
    volv27 (SMOOTHNESS) [LB longer]
+
1/3 RATIO
    slopescore/unifatscore ratio (RATIO) [LB shorter]

NO WEIGHT (INFO ONLY)
    currentprice
    dropscoreratio
"""
from Modules.metriclibrary.STRATTEST_FUNCBASE_MMBM import slopetounifatratiobmin_single, unifatshell_single, allpctdrops_single, dropscoreratio_single
from Modules.metriclibrary.STRATTEST_FUNCBASE_RAW import slopescorefocus_single, statseglen_single, posnegmag_single, globalpricegrab_single
from Modules.metriclibrary.STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single

smooth_lbp = 1095
growth_lbp = 1095
w_slopescore = 1/3
w_ratio = 1/3
w_smoothness = 1/3
unifatscoreweight_avg = 1/6 * w_smoothness
w_volv13_bmaxflatseg = 1/6 * w_smoothness
w_volv13_bmaxflatseg_avg = 1/6 * w_smoothness
w_volv13_maxdrop = 1/6 * w_smoothness
w_volv13_posnegmag_negavg = 1/6 * w_smoothness
w_volv13_accretionscore = 1/6 * w_smoothness

stage3_params = {
    'scriptname': 'STAGE3_groplusvolv15g',
    'scriptparams': [
        {
            'metricname': 'currentprice',
            'metricfunc': globalpricegrab_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 100,
            'filterdirection': 'no',
            'metricweight': 0,
            'type': 'last',
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'dropscoreratio_avg',
            'metricfunc': dropscoreratio_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 0,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'benchticker': '^IXIC',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
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
            'metricname': 'unifatscore_rawbaremaxraw_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoreweight_avg,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
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
            'metricname': 'statseglen_bmaxflat_avg',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': w_volv13_bmaxflatseg_avg,
            'mode': 'flat',
            'stat_type': 'avg',
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
            'look_back': growth_lbp
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
            'look_back': growth_lbp
        }
        ]
        }
