"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 PART I Version K
Date Started: July 25, 2020
Version: 2.1
Version Start Date: July 26, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Used segbackslopescore.
Versions:
K: Combine part I and II to make it easier for looper to run random threshval trials.
FILTERS:

"""
#threshold = 0.0019
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'segbackslopescore_y1',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0.0019,
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
                'threshold': 0.0019,
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
                'threshold': 0.0019,
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
                'threshold': 0.0019,
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
                'threshold': 0.0019,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'segsback': 4,
                'winlen': 360,
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_rawoldbareminraw',
                'rankascending': 1,
                'threshold': 0.011,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'focuscol': 'rawprice',
                'idealcol': 'oldbareminraw',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight',
                'rankascending': 1,
                'threshold': 0.042,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage2part1vK'
    }
]

# STORE
stage2part1b_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
