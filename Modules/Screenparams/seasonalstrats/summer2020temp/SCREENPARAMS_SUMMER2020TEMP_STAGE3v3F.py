"""
Title: SUMMER 2020 TEMP STRAT - STAGE 2 Part II
Date Started: July 25, 2020
Version: 3.0F
Version Start Date: Aug 10, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2.2: Added squeezearea threshold.
3.0: New approach is to do absolute bareminimum then manually review the remaining pool.
3.0A: Experimenting.
3.0D: try without slopescore stage and use clusterscore findings as stage 3.
3.0F: After finding the right additional filters based on clusterscore findings, I can revert Stage 3 back to the original v3B.

            {
                'metricname': 'winrateranker_composite',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/3,
                'look_back': 0
            }
            {
                'metricname': 'squeezearea_mad',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 0,
                'stat_type': 'mad',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'squeezearea_devcomposite',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/3,
                'stat_type': 'devcomposite',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'nonzeromediandpcscore',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'dollarsperday',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0.0009,
                'filterdirection': 'no',
                'metricweight': 1/3,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'winrateranker_median',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/3,
                'look_back': 0
            },
            {
                'metricname': 'smoothsqueeze_ratio',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 0,
                'stat_type': 'ssratio',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'posnegdevscore_std',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0.03,
                'filterdirection': 'no',
                'metricweight': 0,
                'devmeth': 'std',
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'priceageratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'allpctdrop_mean',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 1/2,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'meanbmaxflatseglen',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'calibration': 'baremaxraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage3v3F'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
