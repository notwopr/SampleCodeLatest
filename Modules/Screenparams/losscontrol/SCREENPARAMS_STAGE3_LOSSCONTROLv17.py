"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 17.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description: Just bmax flatness
Loss Control
    Baremax Flatness 1
        average length 1
            absolute length 1/2
                statseglen_bmax_mean 1/2
                statseglen_bmax_median 1/2
            length to life ratio 1/2
                seglife_bmax_mean 1/2
                seglife_bmax_median 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
from STRATTEST_FUNCBASE_RAW import statseglen_single, segliferatio_single
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv17',
    'scriptparams': [
        {
            'metricname': 'statseglen_bmax_mean',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmax_median',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_mean',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_median',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'look_back': 0
        }
        ]
    }
