"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 PART I - RESAMPLESLOPESCORE VERSION
Date Started: Aug 17, 2020
Version: 1.0
Version Start Date: Aug 17, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

FILTERS:

"""
threshold = 0.0011
aggtype = 'mean'
agg2type = 'mean'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'allsampfreqslopescore',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'aggtype': aggtype,
                'agg2type': agg2type,
                'filterdirection': 'above',
                'metricweight': 1,
                'calibration': 'noprepraw',
                'look_back': 360
            },
            {
                'metricname': 'allsampfreqslopescore',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'aggtype': aggtype,
                'agg2type': agg2type,
                'filterdirection': 'above',
                'metricweight': 1,
                'calibration': 'noprepraw',
                'look_back': 360*2
            },
            {
                'metricname': 'allsampfreqslopescore',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'aggtype': aggtype,
                'agg2type': agg2type,
                'filterdirection': 'above',
                'metricweight': 1,
                'calibration': 'noprepraw',
                'look_back': 360*3
            },
            {
                'metricname': 'allsampfreqslopescore',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'aggtype': aggtype,
                'agg2type': agg2type,
                'filterdirection': 'above',
                'metricweight': 1,
                'calibration': 'noprepraw',
                'look_back': 360*4
            },
            {
                'metricname': 'allsampfreqslopescore',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'aggtype': aggtype,
                'agg2type': agg2type,
                'filterdirection': 'above',
                'metricweight': 1,
                'calibration': 'noprepraw',
                'look_back': 360*5
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage2part1_allsampfreq'
    }
]

# STORE
stage2part1_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
