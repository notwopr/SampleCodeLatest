"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: July 25, 2020
Version: 6.0
Version Start Date: Sept 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2.2: Added squeezearea threshold.
3.0: New approach is to do absolute bareminimum then manually review the remaining pool.
3.0I: Best mktbeatpoolpct + poolperf candidate regardless of portsize.
6.0: Replace squeezearea with unisqueezefactor.
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.4717,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'allpctdrop_mean',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.15,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'maxbmaxflatseg',
                'rankascending': 1,
                'threshold': 292,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'mode': 'flat',
                'stat_type': 'max',
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'threshold': 90,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'mode': 'flat',
                'stat_type': 'max',
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor_mean',
                'rankascending': 1,
                'threshold': 0.1,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'stat_type': 'mean',
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
                'threshold': 0.4122,
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part2v6'
    }
]

# STORE
stage2part2_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
