"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 15.00f
Version Start Date: Oct 31, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Version: 15 is one component in combining several different LB periods of the same scheme.
1/3 GROWTH
    slopescore (GROWTH) [LB shorter]
+
1/3 SMOOTHNESS
    volv23 [LB longer]
+
1/3 RATIO
    slopescore/unifatscore ratio (RATIO) [LB shorter]

NO WEIGHT (INFO ONLY)
    currentprice
    dropscoreratio
"""
from STRATTEST_FUNCBASE_MMBM import slopetounifatratiobmin_single, dropscore_single, allpctdrops_single, dropscoreratio_single, bigjumpscore_single, unifatshell_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single, statseglen_single, currprice_single, posnegmagprevscore_single


smooth_lbp = 1348
growth_lbp = 1348
w_slopescore = 1/3
w_ratio = 1/3
w_smoothness = 1/3

bmaxflatsegweight = (1/6) * (1/3)
maxdropweight = (1/6) * (1/3)
bigjumpscore_weight = (1/6) * (1/3)
dropscore_weight = (1/6) * (1/3)
posnegmagprev_negweight = (1/6) * (1/3)
unifatscoreweight = (1/6) * (1/2) * (1/3)
unifatscoredevweight = (1/6) * (1/2) * (1/3)

stage3_params = {
    'scriptname': 'STAGE3_groplusvolv15f',
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
            'look_back': smooth_lbp
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
            'look_back': smooth_lbp
        },
        {
            'metricname': 'bigjumpscore_oldbareminraw',
            'metricfunc': bigjumpscore_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': bigjumpscore_weight,
            'bigjumpstrength': 2,
            'calibration': ['oldbareminraw'],
            'data': 'dpc',
            'look_back': smooth_lbp
        },
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
            'look_back': smooth_lbp
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
            'look_back': smooth_lbp
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
            'metricweight': posnegmagprev_negweight,
            'calibration': [],
            'data': 'dpc',
            'look_back': smooth_lbp
        },
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': dropscore_weight,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': smooth_lbp
        }
        ]
        }
