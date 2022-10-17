"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Aug 19, 2020
Version: 1.00
Version Start Date: Sept 23, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
evenly weighs slopescore and stock age and squeezefactor metrics.

"""
slopew = 1/5            # slopescore
squeezew = 1/5          # squeeze metrics overall
sqaw = 0.5                # squeezearea
unisqw = 1 - sqaw       # unisqueeze metrics
pnegsegw = 1/5        # posnegseg metrics
posnegmagw = 1/5      # posnegmag metrics
posnegprevw = 1/5     # posnegprev metrics

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': slopew,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'squeezearea',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': squeezew*sqaw,
                'stat_type': 'area',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor_mean',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*squeezew*unisqw,
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
                'metricweight': (1/2)*squeezew*unisqw,
                'stat_type': 'median',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'psegnegsegratio',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': pnegsegw*(1/3),
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'avgpseglen',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': pnegsegw*(1/3),
                'mode': 'positive',
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'avgnegseglen',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': pnegsegw*(1/3),
                'mode': 'negative',
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmag_neg',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'neg',
                'stat_type': 'avg',
                'metricweight': posnegmagw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmag_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'pos',
                'stat_type': 'avg',
                'metricweight': posnegmagw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmagratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'stat_type': 'avg',
                'metricweight': posnegmagw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegprevratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': posnegprevw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegprevalence_neg',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'neg',
                'metricweight': posnegprevw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegprevalence_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'pos',
                'metricweight': posnegprevw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3_slopesqueezeposnegseg'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
