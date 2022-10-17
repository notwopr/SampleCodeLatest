"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 18.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description: Just bmax flatness
Loss Control
    Baremax Flatness 1
        max length 1
            absolute length 1/2
                statseglen_bmax_max
            length to life ratio 1/2
                seglife_bmax_max

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv18',
    'scriptparams': [
        {
            'metricname': 'statseglen_bmax_max',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_max',
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'baremaxraw',
            'look_back': 0
        }
        ]
    }
