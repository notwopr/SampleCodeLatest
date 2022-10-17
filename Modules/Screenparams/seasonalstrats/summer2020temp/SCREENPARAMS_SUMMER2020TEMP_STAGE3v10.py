"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Aug 19, 2020
Version: 10
Version Start Date: Sept 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
8: compares rawprice graph to trueline graph, then trueline graph to kneescore graph; but on uniform scale
10: compares rawprice graph to baremaxraw graph, then baremaxraw graph to kneescore graph; but on uniform scale
FILTERS:

"""
threshold = 0.0016
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'unifatscore_rawbaremaxraw',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'focuscol': 'rawprice',
                'idealcol': 'baremaxraw',
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_baremaxrawstraight',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'focuscol': 'baremaxraw',
                'idealcol': 'straight',
                'calibration': 'baremaxraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage3v10'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
