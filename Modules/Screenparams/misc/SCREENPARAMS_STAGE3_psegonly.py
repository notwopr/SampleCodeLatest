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
pseglen
negseglen
psegnegsegratio
avgposdpc
avgnegdpc
maxpseglen (no weight)
maxnegseglen (no weight)
"""
from STRATTEST_FUNCBASE_RAW import psegnegsegratio_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'psegnegsegratio',
                'metricfunc': psegnegsegratio_single,
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'stat_type': 'avg',
                'calibration': [],
                'data': 'dpc',
                'look_back': 0
            },
            {
                'metricname': 'avgpseglen',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'mode': 'positive',
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3_psegonly'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
