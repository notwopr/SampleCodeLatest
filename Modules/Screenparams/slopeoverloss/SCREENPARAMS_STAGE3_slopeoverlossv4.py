"""
Title: SCREENPARAMS - STAGE 3 - slopeoverloss
Date Started: Nov 14, 2020
Version: 4.00
Version Start Date: Nov 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:
slopeoverloss_ratio_mean 1/2
slopeoverloss_ratio_median 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_slopeoverlossv4',
    'scriptparams': [
        {
            'metricname': 'slopeoverloss_ratio_mean',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1/2,
            'combtype': 'ratio',
            'stat_type': 'mean',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'slopeoverloss_ratio_median',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1/2,
            'combtype': 'ratio',
            'stat_type': 'median',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        }
        ]
    }
