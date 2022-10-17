"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 PART I
Date Started: July 25, 2020
Version: 2.1
Version Start Date: July 26, 2020
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
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metric_category': 'priceandstock',
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
                'metric_category': 'priceandstock',
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
                'metric_category': 'priceandstock',
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
                'metric_category': 'priceandstock',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 360*2
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metric_category': 'priceandstock',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 360
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part1'
    }
]

# STORE
stage2part1_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
