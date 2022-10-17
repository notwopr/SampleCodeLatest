"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Aug 19, 2020
Version: 11
Version Start Date: Sept 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
6: compares rawprice graph to trueline graph, then trueline graph to kneescore graph
7: compares rawprice graph to oldbareminraw graph, then oldbareminraw graph to kneescore graph
11: compares rawprice graph to baremaxraw graph, then baremaxraw graph to kneescore graph
FILTERS:

"""
threshold = 0.0016
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'fatscore_rawbaremaxraw',
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
                'metricname': 'fatscore_baremaxrawstraight',
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
        'batchname': 'summer2020temp_stage3v11'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
