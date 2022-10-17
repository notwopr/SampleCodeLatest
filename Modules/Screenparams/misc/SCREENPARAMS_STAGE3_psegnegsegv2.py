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

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'psegnegsegratio',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/5,
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'avgpseglen',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/5,
                'mode': 'positive',
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'avgnegseglen',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/5,
                'mode': 'negative',
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmag_neg',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'neg',
                'metricweight': 1/5/2,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmag_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'pos',
                'metricweight': 1/5/2,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegprevalence_neg',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'neg',
                'metricweight': 1/5/2,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegprevalence_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'pos',
                'metricweight': 1/5/2,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.35,
                'filterdirection': 'no',
                'metricweight': 1/3,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmagratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegprevratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3_psegnegsegv2'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
