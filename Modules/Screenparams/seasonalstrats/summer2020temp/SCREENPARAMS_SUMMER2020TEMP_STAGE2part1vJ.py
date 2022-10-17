"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 PART I Version B
Date Started: July 25, 2020
Version: 2.1
Version Start Date: July 26, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Used segbackslopescore.
Versions:

FILTERS:

"""
threshold = 0.001348
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'segbackslopescore_y1',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'segsback': 0,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescore_y2',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'segsback': 1,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescore_y3',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'segsback': 2,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescore_y4',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'segsback': 3,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescore_y5',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'segsback': 4,
                'winlen': 360,
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage2part1vJ'
    }
]

# STORE
stage2part1b_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
