"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: July 25, 2020
Version: 3.0A
Version Start Date: Aug 10, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2.2: Added squeezearea threshold.
3.0: New approach is to do absolute bareminimum then manually review the remaining pool.
3.0A: Experimenting.
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
                'metricweight': 1/3,
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
                'metricweight': 1/3,
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'winrateranker_composite',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/3,
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage3v3B'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
