"""
Title:  SCREEN PARAMS - STAGE 2 FILTERS
Date Started: Feb 20, 2022
Version: 1
Version Start Date: Feb 20, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Return stocks who for the past X days, has better growthrate, unifatscore_rawtobaremax, unifatscore_baremintobaremax, drop_mag, drop_prev, dropscore, and maxdd than the best of all three benchmarks (Dow S&P and Nasdaq).
"""
from Modules.metriclibrary.STRATTEST_FUNCBASE_RAW import getpctchange_single
from Modules.metriclibrary.STRATTEST_FUNCBASE_MMBM import unifatshell_single, dropmag_single, dropprev_single, dropscore_single, allpctdrops_single

lookback = 360
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'STAGE2FILTERSv9',
    'scriptparams': [
            {
                'metricname': 'growthrate',
                'metricfunc': getpctchange_single,
                'threshold': 'bestbench',
                'focuscol': 'rawprice',
                'filterdirection': '>',
                'look_back': lookback,
                'better': 'bigger',
                'calibration': [],
                'data': '',
                'rankascending': 0,
                'metricweight': 1,
                'thresholdtype': 'absolute'
            },
            {
                'metricname': 'unifatscore_rawbaremaxraw_avg',
                'metricfunc': unifatshell_single,
                'focuscol': 'rawprice',
                'idealcol': 'baremaxraw',
                'stat_type': 'avg',
                'calibration': ['baremaxraw'],
                'better': 'smaller',
                'data': '',
                'look_back': lookback,
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 'bestbench',
                'filterdirection': '<',
                'metricweight': 1
            },
            {
                'metricname': 'unifatscore_bareminbaremax_avg',
                'metricfunc': unifatshell_single,
                'focuscol': 'oldbareminraw',
                'idealcol': 'baremaxraw',
                'stat_type': 'avg',
                'calibration': ['oldbareminraw', 'baremaxraw'],
                'better': 'smaller',
                'data': '',
                'look_back': lookback,
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 'bestbench',
                'filterdirection': '<',
                'metricweight': 1
            },
            {
                'metricname': 'drop_mag_avg',
                'metricfunc': dropmag_single,
                'uppercol': 'baremaxraw',
                'lowercol': 'rawprice',
                'stat_type': 'avg',
                'calibration': ['baremaxraw'],
                'better': 'bigger',
                'data': '',
                'look_back': lookback,
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 'bestbench',
                'filterdirection': '>',
                'metricweight': 1
            },
            {
                'metricname': 'drop_prev',
                'metricfunc': dropprev_single,
                'uppercol': 'baremaxraw',
                'lowercol': 'rawprice',
                'calibration': ['baremaxraw'],
                'better': 'smaller',
                'data': '',
                'look_back': lookback,
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 'bestbench',
                'filterdirection': '<',
                'metricweight': 1
            },
            {
                'metricname': 'drop_score',
                'metricfunc': dropscore_single,
                'uppercol': 'baremaxraw',
                'lowercol': 'rawprice',
                'stat_type': 'avg',
                'calibration': ['baremaxraw'],
                'better': 'bigger',
                'data': '',
                'look_back': lookback,
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 'bestbench',
                'filterdirection': '>',
                'metricweight': 1
            },
            {
                'metricname': 'allpctdrop_rawbaremaxraw_max',
                'metricfunc': allpctdrops_single,
                'calibration': ['baremaxraw'],
                'uppercol': 'baremaxraw',
                'lowercol': 'rawprice',
                'stat_type': 'min',
                'better': 'bigger',
                'data': '',
                'look_back': lookback,
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 'bestbench',
                'filterdirection': '>',
                'metricweight': 1
            }
        ]
    }
