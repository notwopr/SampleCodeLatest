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
evenly weighs slopescore and stock age.

"""

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
                'metricweight': 1/2,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'age',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 180,
                'filterdirection': 'no',
                'metricweight': 1/2,
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3_slopeandage'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
