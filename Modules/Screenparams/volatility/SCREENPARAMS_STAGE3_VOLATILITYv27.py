"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 18, 2021
Version: 27
Version Start Date: Oct 31, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Version:
same as 25

REVIEW: PRETTY much the same results as v25, with the exceptions of a few instances of differences.  But whenever there were differences, they were always localized, meaning the differences were amongst stocks adjacent to each other (at most 4), preserving the overall ranking otherwise.
bmax flatseg max
bmax flatseg avg
maxdrop
posnegmag
unifatscore_rawbaremaxraw_avg
accretionscore

NO WEIGHT (INFO ONLY)
    dropscoreratio
"""
from STRATTEST_FUNCBASE_MMBM import allpctdrops_single, dropscoreratio_single, unifatshell_single
from STRATTEST_FUNCBASE_RAW import statseglen_single, posnegmag_single
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single

unifatscoreweight_avg = 1/6
w_volv13_bmaxflatseg = 1/6
w_volv13_bmaxflatseg_avg = 1/6
w_volv13_maxdrop = 1/6
w_volv13_posnegmag_negavg = 1/6
w_volv13_accretionscore = 1/6

stage3_params = {
    'scriptname': 'VOLATILITYv27',
    'scriptparams': [
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
            'look_back': 0
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
            'look_back': 0
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
            'look_back': 0
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
            'look_back': 0
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
            'metricweight': w_volv13_posnegmag_negavg,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        }
        ]
        }
