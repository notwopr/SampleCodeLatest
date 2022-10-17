"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: July 25, 2020
Version: 8.0
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
8.0:
maxdrop
allpctdrop_mean
maxbmaxflatseg
maxbmflatseg
kneescore
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.45,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [

            {
                'metricname': 'allpctdrop_mean',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.185,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'maxbmaxflatseg',
                'rankascending': 1,
                'threshold': 140,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'threshold': 120,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'kneescore',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0.26,
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part2v8'
    }
]

# STORE
stage2part2_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
