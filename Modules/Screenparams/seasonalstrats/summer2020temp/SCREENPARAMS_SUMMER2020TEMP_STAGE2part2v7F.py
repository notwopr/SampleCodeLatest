"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: July 25, 2020
Version: 7F
Version Start Date: Sept 7, 2020
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
                'metricname': 'maxdrop',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.3938,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'allpctdrop_mean',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.35,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'maxbmaxflatseg',
                'rankascending': 1,
                'threshold': 167.2,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'threshold': 210.46,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'age',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 180,
                'filterdirection': 'above',
                'metricweight': 0,
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor',
                'rankascending': 1,
                'threshold': 0.1,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'kneescore',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0.3042,
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_rawoldbareminraw',
                'rankascending': 1,
                'threshold': 0.05,
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
                'threshold': 0.05,
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
        'batchname': 'summer2020temp_stage2part2v7F'
    }
]

# STORE
stage2part2_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
