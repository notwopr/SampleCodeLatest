"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 31, 2020
Version: 38.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description: Same as version 7 but using squeezeraw instead (baremaxraw to oldbareminraw)
Loss Control
    Squeezefactor 1/2
        unifatscore_baremaxrawoldbareminraw_mean 1/2
        unifatscore_baremaxrawoldbareminraw_median 1/2
    UnifatScore 1/2
        unifatscore_rawoldbareminraw_mean 1/2
        unifatscore_rawoldbareminraw_median 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv38',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawoldbareminraw_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mean',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        }
        ]
    }
