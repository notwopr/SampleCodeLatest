"""
Title: SUMMER 2020 TEMP STRAT STAGE 3
Date Started: July 26, 2020
Version: 3.0
Version Start Date: Aug 11, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Layer stage.
Versions:

FILTERS:
None.
LAYERS:
??
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
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'allpctdrop_mean',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 1/2,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'meanbmaxflatseglen',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'calibration': 'baremaxraw',
                'look_back': 0
            },
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
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
