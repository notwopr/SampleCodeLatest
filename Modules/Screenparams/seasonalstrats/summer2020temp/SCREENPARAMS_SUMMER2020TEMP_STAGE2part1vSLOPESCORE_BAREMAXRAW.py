"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 PART I
Date Started: July 25, 2020
Version: 5
Version Start Date: Sept 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
5-BAREMAXRAW - use oldbareminraw prices to calculate slopescore
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
                'metricweight': 0,
                'calibration': 'noprepbaremaxraw',
                'look_back': 360*5
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepbaremaxraw',
                'look_back': 360*3
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepbaremaxraw',
                'look_back': 360*4
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepbaremaxraw',
                'look_back': 360*2
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': threshold,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepbaremaxraw',
                'look_back': 360
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part1vSLOPESCORE_BAREMAXRAW'
    }
]

# STORE
stage2part1_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
