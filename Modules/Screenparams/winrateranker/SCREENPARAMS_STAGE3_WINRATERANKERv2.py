"""
Title: SCREENPARAMS - STAGE 3 - WINRATERANKER
Date Started: Sept 29, 2020
Version: 2.00
Version Start Date: Oct 7, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Screen params.
Description:

    Winrate: 1/2
    Bmflatness: 1/2
        avg length 1/4
        avglen to life 1/4
        max length 1/4
        max len to life 1/4
Versions:
2: Winrateranker uses the oldbareminraw graph and because of that it has limitations in that for example, you get a graph that is virtually flat for the entirely lifespan save for the last few days, and if it is large enough, it ranks very well.  To combat this problem, I need to add metrics that guard against bmflatness.
    Winrateranker measures consistency of how well it ranks over various rolling window averages.
    It's not so much the bmflatlinescore or the proportion that the graph is bmflat, but rather the maxbmflat length, maxbmflatliferatio, average bmflatseglen and avgbmflatsegliferatio

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'winrateranker_composite',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'look_back': 0
            },
            {
                'metricname': 'avgbmflatseglen',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*(1/4),
                'mode': 'flat',
                'stat_type': 'avg',
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatliferatio',
                'rankascending': 1,
                'threshold': 0.3,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*(1/4),
                'mode': 'flat',
                'stat_type': 'max',
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'threshold': 360,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*(1/4),
                'mode': 'flat',
                'stat_type': 'max',
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'avgbmflatliferatio',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*(1/4),
                'mode': 'flat',
                'stat_type': 'avg',
                'calibration': 'oldbareminraw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'WINRATERANKERv2'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
