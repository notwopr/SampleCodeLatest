"""
Title: SCREEN PARAMS - STAGE 3 - 2018 METHOD
Date Started: Oct 4, 2020
Version: 7
Version Start Date: Oct 6, 2020
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
        UnifatScore 1/2
            Unifatscore_rawoldbareminraw 1/2
                unifatscore_rawoldbareminraw_mean 1/2
                Unifatscore_rawoldbareminraw_median 1/2
            Unifatscore_oldbareminrawstraight 1/2
                unifatscore_oldbareminrawstraight_mean 1/2
                Unifatscore_oldbareminrawstraight_median 1/2
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': '2018METHODv7',
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
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
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
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        }
        ]
    }
