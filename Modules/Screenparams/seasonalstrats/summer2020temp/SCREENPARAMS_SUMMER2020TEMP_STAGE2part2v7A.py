"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: Aug 19, 2020
Version: 7A
Version Start Date: Sept 6, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

"""
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
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
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part2v7A'
    }
]

# STORE
stage2part2_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
