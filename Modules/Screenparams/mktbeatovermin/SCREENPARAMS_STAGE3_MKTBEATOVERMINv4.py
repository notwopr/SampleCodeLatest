"""
Title: SCREENPARAMS - STAGE 3 - mktbeatperf to minperf
Date Started: Nov 12, 2020
Version: 4.00
Version Start Date: Nov 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:

    Consecutive Negative Losses 1/2
        Average Length
            Absolute Length
                statseglen_negseg_mean
    Age 1/2
        Age_older

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_mktbeatoverminv4',
    'scriptparams': [
        {
            'metricname': 'statseglen_negseg_mean',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'mode': 'negative',
            'stat_type': 'mean',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'age_older',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 180,
            'filterdirection': 'no',
            'metricweight': (1/2),
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
    }
