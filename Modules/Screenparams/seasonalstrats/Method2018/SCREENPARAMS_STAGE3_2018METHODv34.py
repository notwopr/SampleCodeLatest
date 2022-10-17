"""
Title: SCREEN PARAMS - STAGE 3 - 2018 METHOD
Date Started: Oct 4, 2020
Version: 34
Version Start Date: Oct 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Description:

    Growth Factor: 1/2
        slopescore

    Shape Factor: 1/2
        Squeezefactor 1/2
            unisqueezefactor 1/2
                unisqueezefactor_mean 1/2
                unisqueezefactor_median 1/2
            squeezearea 1/2
        UnifatScore 1/2(VOLATILITY v3)
            Difference between raw price from true graph
                Magnitude of that difference
                    mean 1/2  unifatscore_rawoldbareminraw_mean
                    median 1/2  unifatscore_rawoldbareminraw_median
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': '2018METHODv34',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'calibration': 'noprepraw',
            'look_back': 0
        },
        {
            'metricname': 'unisqueezefactor_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'stat_type': 'mean',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'unisqueezefactor_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'stat_type': 'median',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'squeezearea',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2),
            'stat_type': 'area',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2),
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
            'metricweight': (1/2)*(1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        }
        ]
    }
