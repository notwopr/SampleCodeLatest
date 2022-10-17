"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 30, 2020
Version: 7.00
Version Start Date: Oct 30, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description: Only any time drops metrics.
Loss Control
    any-timespan drops
        average any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_mean 1/2
            allpctdrop_rawoldbareminraw_median 1/2
        max any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_max
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv7',
    'scriptparams': [
        {
            'metricname': 'allpctdrop_rawoldbareminraw_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'mean',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_median',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'median',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_max',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/2),
            'calibration': 'smoothraw',
            'stat_type': 'max',
            'look_back': 0
        }
        ]
    }
