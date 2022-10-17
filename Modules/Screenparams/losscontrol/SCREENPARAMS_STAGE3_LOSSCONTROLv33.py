"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 33.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:
Loss Control
    Consecutive Negative Losses 1
        Max Length 1
            length to life ratio 1
                seglife_negseg_max
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv33',
    'scriptparams': [
        {
            'metricname': 'seglife_negseg_max',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'mode': 'negative',
            'stat_type': 'max',
            'calibration': 'nonzeroraw',
            'look_back': 0
        }
        ]
    }