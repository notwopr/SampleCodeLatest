"""
Title: OPTIMAL PARAM FINDER - second pass params
Date Started: Mar 15, 2020
Version: 3.01
Version Start Date: June 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Scratch parambatcher for research
Versions:
3.01: Remove specialized litmus test function with using standard paramdict filtermethod.

FILTERS:
volscore < NASDAQ
slopescore > 0.0006 (20% per year)
posareamargin > 0
posareapct > 0.90
masterssindexscore < 0.60
,
,
            {
                'metricname': 'volscore',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': '^IXIC',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 0
            }
                        {
                            'metricname': 'allpctdrop_avgminusdev',
                            'rankascending': 1,
                            'thresholdtype': 'absolute',
                            'threshold': -0.15,
                            'filterdirection': 'above',
                            'metricweight': 0,
                            'calibration': 'squeezeraw',
                            'stat_type': 'comp-devcomp',
                            'look_back': 0
                        },
            {
                'metricname': 'posareamargin',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'benchstock': '^IXIC',
                'look_back': 0
            },
            {
                'metricname': 'posareapct',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0.95,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'benchstock': '^IXIC',
                'look_back': 0
            },
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.08,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            }

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [

            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0.0006,
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'squeezearea',
                'rankascending': 1,
                'threshold': 0.10, #0.10, #0.08
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'stat_type': 'area',
                'calibration': 'squeezeraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'optimalparamfinder_secondpassparams'
    }
]

# STORE
secondpass_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
