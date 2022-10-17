"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: July 25, 2020
Version: 3.0H
Version Start Date: Aug 10, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2.2: Added squeezearea threshold.
3.0: New approach is to do absolute bareminimum then manually review the remaining pool.

            {
                'metricname': 'maxbmflatliferatio',
                'rankascending': 1,
                'threshold': 0.3,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 1/6,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmaxflatliferatio',
                'rankascending': 1,
                'threshold': 0.3,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 1/6,
                'calibration': 'baremaxraw',
                'look_back': 0
            },

            {
                'metricname': 'medianbmflatliferatio',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/6,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },

            {
                'metricname': 'maxflatseg',
                'rankascending': 1,
                'threshold': 8,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 360
            },
            {
                'metricname': 'roughnessfactor',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 0,
                'stat_type': 'roughnessfactor',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'dailystd',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'rollingsqueezearea_mean',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'win_len': 180,
                'agg_type': 'mean',
                'stat_type': 'area',
                'calibration': 'squeezeraw',
                'look_back': 0
            }
            ,
            {
                'metricname': 'benchbeatpct',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'benchstock': '^IXIC',
                'look_back': 0
            },
            {
                'metricname': 'priceageratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'currentprice',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0.0009,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'dollarsperday',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0.0009,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            }
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.3897,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'allpctdrop_mean',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.385,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'maxbmaxflatseg',
                'rankascending': 1,
                'threshold': 257,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'threshold': 205,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'squeezearea',
                'rankascending': 1,
                'threshold': 0.1196,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'stat_type': 'area',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'age',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 180,
                'filterdirection': 'above',
                'metricweight': 0,
                'look_back': 0
            },
            {
                'metricname': 'kneescore',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0.3474,
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part2v3H'
    }
]

# STORE
stage2part2_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
