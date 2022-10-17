"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3 - RESAMPLESLOPESCORE VERSION
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
resamplefreq = 180
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'resampledslopescore_f15',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'resamplefreq': 15,
                'aggtype': aggtype,
                'filterdirection': 'no',
                'metricweight': 1/5,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'resampledslopescore_f30',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'resamplefreq': 30,
                'aggtype': aggtype,
                'filterdirection': 'no',
                'metricweight': 1/5,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'resampledslopescore_f60',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'resamplefreq': 60,
                'aggtype': aggtype,
                'filterdirection': 'no',
                'metricweight': 1/5,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'resampledslopescore_f90',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'resamplefreq': 90,
                'aggtype': aggtype,
                'filterdirection': 'no',
                'metricweight': 1/5,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'resampledslopescore_f180',
                'rankascending': 0,
                'threshold': threshold,
                'thresholdtype': 'absolute',
                'resamplefreq': 180,
                'aggtype': aggtype,
                'filterdirection': 'no',
                'metricweight': 1/5,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3_resampleversion'
    }
]

# STORE
stage3_params_resamp = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
