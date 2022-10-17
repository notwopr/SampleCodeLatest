"""
Title: SCREEN PARAMS - STAGE 2 PART I - SEGSBACKSLOPESCORE PLUS SLOPESCORE
Date Started: Sept 26, 2020
Version: 1.00
Version Start Date: Oct 6, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Used segbackslopescore.
Versions:
7: just segsbackslopescore 1 thru 5yr on raw graph.
FILTERS:

"""
segsbackthreshold = 0.0019
threshold = 0.0016
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 360*5
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 360*3
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 360*4
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 360*2
            },
            {
                'metricname': 'segbackslopescore_y1',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': segsbackthreshold,
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
                'threshold': segsbackthreshold,
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
                'threshold': segsbackthreshold,
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
                'threshold': segsbackthreshold,
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
                'threshold': segsbackthreshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'segsback': 4,
                'winlen': 360,
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'stage2part1_segsbackplusslopescore'
    }
]

# STORE
stage2part1_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
