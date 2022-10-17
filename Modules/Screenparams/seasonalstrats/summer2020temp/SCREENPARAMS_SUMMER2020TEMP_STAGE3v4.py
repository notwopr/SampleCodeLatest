"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: July 25, 2020
Version: 4.0
Version Start Date: Aug 21, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
4.0: Experiment with changerate and posnegtrend metrics.

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'posnegmag_neg',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'neg',
                'metricweight': 1/8,
                'calibration': 'raw',
                'look_back': 360
            },
            {
                'metricname': 'posnegmag_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'pos',
                'metricweight': 1/8,
                'calibration': 'raw',
                'look_back': 360
            },
            {
                'metricname': 'posnegprevalence_neg',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'neg',
                'metricweight': 1/8,
                'calibration': 'raw',
                'look_back': 360
            },
            {
                'metricname': 'posnegprevalence_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'pos',
                'metricweight': 1/8,
                'calibration': 'raw',
                'look_back': 360
            },
            {
                'metricname': 'prevalencetrend_neg',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changewinsize': 1,
                'changetype': 'neg',
                'metricweight': 1/8,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'prevalencetrend_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changewinsize': 1,
                'changetype': 'pos',
                'metricweight': 1/8,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'changeratetrend_neg',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changewinsize': 1,
                'changetype': 'neg',
                'metricweight': 1/8,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'changeratetrend_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changewinsize': 1,
                'changetype': 'pos',
                'metricweight': 1/8,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage3v4'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
