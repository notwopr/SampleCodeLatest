"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 37.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description: Same as version 7 but using squeezeraw instead (baremaxraw to oldbareminraw)
Loss Control
    any-timespan drops
        average any-timespan drops 1
            allpctdrop_baremaxrawoldbareminraw_mean 1/2
            allpctdrop_baremaxrawoldbareminraw_median 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv37',
    'scriptparams': [
        {
            'metricname': 'allpctdrop_baremaxrawoldbareminraw_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/2),
            'calibration': 'squeezeraw',
            'stat_type': 'mean',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_baremaxrawoldbareminraw_median',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/2),
            'calibration': 'squeezeraw',
            'stat_type': 'median',
            'look_back': 0
        }
        ]
    }
