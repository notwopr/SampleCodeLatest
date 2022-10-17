"""
Title:  MANUAL REVIEW SCRIPT - PARAMSCRIPT FOR ELIMINATING BAD VISUALS
Date Started: Nov 4, 2020
Version: 1.00
Version Start Date: Nov 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Components:
    squeeze component 1/2
        volume of squeezearea 1/2
            squeezearea
        avg squeeze thickness 1/2
            squeezearea_mean 0
        stability of squeezearea volume 0
            squeezearea_std 0
            squeezearea_mad 0
    smooth component 0
        volume of smootharea 0
            smootharea
        avg squeeze thickness 0
            smootharea_mean
        stability of smootharea volume 0
            smootharea_std 0
            smootharea_mad 0
I removed weights for squeeze stability metrics because the smootharea stability takes care of that, and I chose that over squeezearea stability because it is more accurate depiction of the actual fluctuation (squeezearea creates an area where there was an alltime high, and so it doesn't show the actual shape of the graph).
I also removed smootharea volume because the only volume that matters is the squeezearea volume.
The question then is what is the balance between the stability and the volume metrics.
Actually, don't we care more about the avg "thickness" of the smootharea rather than the deviation?
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
badvisuals_params = {
    'scriptname': 'manualreview_badvisualsranker',
    'scriptparams': [
        {
            'metricname': 'squeezearea',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'stat_type': 'area',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'squeezearea_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'stat_type': 'mean',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'squeezearea_std',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'std',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'squeezearea_mad',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'mad',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'smootharea',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'area',
            'calibration': 'smoothraw',
            'look_back': 0
        },
        {
            'metricname': 'smootharea',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'mean',
            'calibration': 'smoothraw',
            'look_back': 0
        },
        {
            'metricname': 'smootharea_std',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'std',
            'calibration': 'smoothraw',
            'look_back': 0
        },
        {
            'metricname': 'smootharea_mad',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'mad',
            'calibration': 'smoothraw',
            'look_back': 0
        }
        ]
    }
