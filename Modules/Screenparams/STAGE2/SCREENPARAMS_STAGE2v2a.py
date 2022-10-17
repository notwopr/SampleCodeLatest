"""
Title:  SCREEN PARAMS - STAGE 2 FILTERS
Date Started: Jan 21, 2021
Version: 2.00a
Version Start Date: Feb 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2: Based on the results of winnerthresholdfinder backtest for 1,000 trials on test period of 1 year where winner is defined as >100% growth with a dropscore < -.25 and maxdrop < -.7 for pretest period features.  This is the list of pretest period ranges for that set are.
FILTERS:

dpc_cruncher_bmax_avg
dpc_cruncher_bmax_dev
dpc_cruncher_bmin_avg
dpc_cruncher_bmin_dev
dpc_cruncher_raw_avg
dpc_cruncher_raw_dev
dpc_cruncher_true_avg
dpc_cruncher_true_dev
posnegmag_neg_dev
posnegmag_pos_dev
posnegscore_posnegrange_bmax
posnegscore_posnegrange_bmin
posnegscore_posnegrange_raw
posnegscore_posnegrange_true
posnegscore_posplusneg_bmax
posnegscore_posplusneg_bmin
posnegscore_posplusneg_raw
posnegscore_posplusneg_true
posnegscore_xposplusxneg_bmax
posnegscore_xposplusxneg_bmin
posnegscore_xposplusxneg_raw
posnegscore_xposplusxneg_true
rollingslopescore_dev
rollingslopescore_truedev
unifatscore_rawbaremaxraw_avg
unifatscore_rawbaremaxraw_dev
unifatscore_rawoldbareminraw_dev
unifatscore_rawstraight_dev
unifatscore_rawtrue_avg
unifatscore_rawtrue_dev
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_RAW import posnegmag_single, rollingslopescore_single, dpc_cruncher_single, dpc_cruncher_posneg_single


stage2_params = {
    'scriptname': 'STAGE2FILTERSv2a',
    'scriptparams': [
        {
            'metricname': 'posnegscore_posplusneg_true',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 24,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['trueline'],
            'data': 'truedpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'posplusneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_xposplusxneg_true',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.06,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['trueline'],
            'data': 'truedpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'xposplusxneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posnegrange_true',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.0014,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['trueline'],
            'data': 'truedpc',
            'statmeth': 'avg',
            'statmeth2': 'dev',
            'calcmeth': 'posnegrange',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posplusneg_bmax',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 24,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'posplusneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_xposplusxneg_bmax',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.06,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'xposplusxneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posnegrange_bmax',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.0010,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'statmeth': 'avg',
            'statmeth2': 'dev',
            'calcmeth': 'posnegrange',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posplusneg_bmin',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 24,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'posplusneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_xposplusxneg_bmin',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.06,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'xposplusxneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posnegrange_bmin',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.0011,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'statmeth': 'avg',
            'statmeth2': 'dev',
            'calcmeth': 'posnegrange',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posplusneg_raw',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 24,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': [],
            'data': 'dpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'posplusneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_xposplusxneg_raw',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.06,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': [],
            'data': 'dpc',
            'statmeth': 'avg',
            'statmeth2': '',
            'calcmeth': 'xposplusxneg',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posnegrange_raw',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.0041,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': [],
            'data': 'dpc',
            'statmeth': 'avg',
            'statmeth2': 'dev',
            'calcmeth': 'posnegrange',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_raw_avg',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.027,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': [],
            'data': 'dpc',
            'mode': 'avg',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_raw_dev',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.37,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': [],
            'data': 'dpc',
            'mode': 'dev',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_true_avg',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.027,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['trueline'],
            'data': 'truedpc',
            'mode': 'avg',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_true_dev',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.37,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['trueline'],
            'data': 'truedpc',
            'mode': 'dev',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_bmax_avg',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.027,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'mode': 'avg',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_bmax_dev',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.37,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'mode': 'dev',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_bmin_avg',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.027,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'mode': 'avg',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_bmin_dev',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0.37,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'mode': 'dev',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_pos_dev',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1.2,
            'filterdirection': 'below',
            'changetype': 'pos',
            'stat_type': 'dev',
            'metricweight': 1,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_dev',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.47,
            'filterdirection': 'below',
            'changetype': 'neg',
            'stat_type': 'dev',
            'metricweight': 1,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'rollingslopescore_truedev',
            'metricfunc': rollingslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0049,
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['trueline'],
            'data': '',
            'focuscol': 'trueline',
            'agg_type': 'dev',
            'win_len': 360,
            'look_back': 0
        },
        {
            'metricname': 'rollingslopescore_dev',
            'metricfunc': rollingslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0049,
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'focuscol': 'rawprice',
            'agg_type': 'dev',
            'win_len': 360,
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.78,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'dev',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawstraight_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 2.11,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'dev',
            'calibration': ['straight'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawtrue_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.44,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
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
            'threshold': 0.24,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'trueline',
            'stat_type': 'dev',
            'calibration': ['trueline'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawbaremaxraw_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.31,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
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
            'threshold': 0.26,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'dev',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
        }
