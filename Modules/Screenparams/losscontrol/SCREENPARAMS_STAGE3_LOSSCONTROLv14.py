"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 14.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:  Just daily drops.
Loss Control
    daily drops 1
        average daily drops 1/2
            posnegmag_neg_mean 1/2
            posnegmag_neg_median 1/2
        posnegprev_neg 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv14',
    'scriptparams': [
        {
            'metricname': 'posnegmag_neg_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'mean',
            'metricweight': (1/2)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_median',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'median',
            'metricweight': (1/2)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevalence_neg',
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'metricweight': (1/2),
            'calibration': 'raw',
            'look_back': 0
        }
        ]
    }
