"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 PART I
Date Started: July 25, 2020
Version: 6
Version Start Date: Sept 3, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Used segbackslopescore.
Versions:
5-OLDBAREMINRAW - use oldbareminraw prices to calculate segsbackslopescore
FILTERS:
6 - trueline instead
"""
threshold = 0.0019
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'segbackslopescoreoldbareminraw_y1',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'trueline',
                'segsback': 0,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescoreoldbareminraw_y2',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'trueline',
                'segsback': 1,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescoreoldbareminraw_y3',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'trueline',
                'segsback': 2,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescoreoldbareminraw_y4',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'trueline',
                'segsback': 3,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'segbackslopescoreoldbareminraw_y5',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'trueline',
                'segsback': 4,
                'winlen': 360,
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage2part1vSEGSBACKSLOPESCORE_TRUELINE'
    }
]

# STORE
stage2part1b_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
