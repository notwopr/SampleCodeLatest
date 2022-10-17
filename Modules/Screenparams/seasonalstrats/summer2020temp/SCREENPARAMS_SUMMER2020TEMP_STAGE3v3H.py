"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3v3G
Date Started: Aug 19, 2020
Version: 3G
Version Start Date: Aug 19, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

FILTERS:

"""
threshold = 0.0016
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'squeezearea',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1,
                'stat_type': 'area',
                'calibration': 'squeezeraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage3v3H'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
