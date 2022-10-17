"""
Title: SCREEN PARAMS - STAGE 2 FILTERS (WINNERTHRESHOLD FINDER PARAMSCRIPT)
Date Started: Jan 30, 2021
Version: 2.00c
Version Start Date: Feb 5, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_RAW import rollingslopescore_single, dpc_cruncher_single, dpc_cruncher_posneg_single


stage2_params = {
    'scriptname': 'STAGE2FILTERSv2c(winnerthresholdfinderv3)',
    'scriptparams': [
        {
            'metricname': 'dpc_cruncher_bmax_avg',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 1.43,
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
            'threshold': 119.18,
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
            'threshold': 0.332,
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
            'threshold': 5.74,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'mode': 'dev',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_true_avg',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 1.3,
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
            'threshold': 108.35,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'calibration': ['trueline'],
            'data': 'truedpc',
            'mode': 'dev',
            'look_back': 0
        },
        {
            'metricname': 'posnegscore_posnegrange_bmax',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.00144,
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
            'metricname': 'posnegscore_posnegrange_bmin',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.00166,
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
            'metricname': 'posnegscore_posnegrange_true',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.00281,
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
            'threshold': 1420,
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
            'metricname': 'posnegscore_posplusneg_bmin',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 199,
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
            'metricname': 'posnegscore_posplusneg_true',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 602.43,
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
            'metricname': 'posnegscore_xposplusxneg_bmax',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 1.43,
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
            'metricname': 'posnegscore_xposplusxneg_bmin',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 0.664,
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
            'metricname': 'posnegscore_xposplusxneg_true',
            'metricfunc': dpc_cruncher_posneg_single,
            'rankascending': 0,
            'threshold': 1.3,
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
            'metricname': 'rollingslopescore_truedev',
            'metricfunc': rollingslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.00483,
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
            'metricname': 'unifatscore_rawoldbareminraw_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 2733087,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'dev',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        }
        ]
        }
