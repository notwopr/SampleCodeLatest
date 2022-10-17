"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: July 25, 2020
Version: 3.0I
Version Start Date: Aug 21, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2.2: Added squeezearea threshold.
3.0: New approach is to do absolute bareminimum then manually review the remaining pool.
3.0I: Best mktbeatpoolpct + poolperf candidate regardless of portsize.
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'squeezearea',
                'rankascending': 1,
                'threshold': 0.10,
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
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part2v3L'
    }
]

# STORE
stage2part2_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
