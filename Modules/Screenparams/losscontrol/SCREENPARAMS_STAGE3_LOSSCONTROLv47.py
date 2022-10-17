"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 47.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description: Same as version 7 but using squeezeraw instead (baremaxraw to oldbareminraw)
Loss Control
    UnifatScore 1
    raw to trueline 1/2
        unifatscore_rawtrue_mean 1/2
        unifatscore_rawtrue_median 1/2
    trueline to straight 1/2
        unifatscore_truestraight_mean 1/2
        unifatscore_truestraight_median 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv47',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawtrue_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'trueline',
            'stat_type': 'mean',
            'calibration': 'nopreptrueline',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawtrue_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'trueline',
            'stat_type': 'median',
            'calibration': 'nopreptrueline',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_truestraight_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'trueline',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': 'nopreptrueline',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_truestraight_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'trueline',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': 'nopreptrueline',
            'look_back': 0
        }
        ]
    }
