"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 13.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:  Just daily drops.
Loss Control
    daily drops 1
        max daily drop 1
            posnegmag_neg_max
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv13',
    'scriptparams': [
        {
            'metricname': 'posnegmag_neg_max',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'min',
            'metricweight': 1,
            'calibration': 'raw',
            'look_back': 0
        }
        ]
    }