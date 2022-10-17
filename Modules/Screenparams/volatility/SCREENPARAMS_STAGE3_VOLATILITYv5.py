"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Oct 11, 2020
Version: 5.00
Version Start Date: Oct 24, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:
True graph == oldbareminraw graph.  See Investment Research Journal for reasoning.
    bigjump_mag_oldbareminraw 1/2
    Difference between raw price from oldbareminraw graph 1/2
        Magnitude of that difference
            mean 1/2  unifatscore_rawoldbareminraw_mean
            median 1/2  unifatscore_rawoldbareminraw_median


"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_VOLATILITYv5',
    'scriptparams': [
        {
            'metricname': 'bigjump_mag_oldbareminraw',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1/2,
            'bigjumpstrength': 2,
            'calibration': 'oldbareminraw',
            'look_back': 0
        },
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
        }
        ]
    }
