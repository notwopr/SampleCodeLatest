"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Aug 19, 2020
Version: 9
Version Start Date: Sept 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
6: compares rawprice graph to trueline graph, then trueline graph to kneescore graph
7: compares rawprice graph to oldbareminraw graph, then oldbareminraw graph to kneescore graph
9: compares rawprice graph to oldbareminraw graph, then oldbareminraw graph to kneescore graph but on uniform scale
FILTERS:
            {
                'metricname': 'unifatscore_rawoldbareminraw',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/3,
                'focuscol': 'rawprice',
                'idealcol': 'oldbareminraw',
                'stat_type': 'unifatscore',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/3,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'unifatscore',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_rawoldbareminraw_std',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/3,
                'focuscol': 'rawprice',
                'idealcol': 'oldbareminraw',
                'stat_type': 'unistd',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight_std',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 0,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'unistd',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            }
            {
                'metricname': 'currentprice',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 1,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            {
                'metricname': 'winrateranker_mean',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2,
                'look_back': 0
            }
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 1,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            {
                'metricname': 'unifatscore_rawoldbareminraw',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*0.40,
                'focuscol': 'rawprice',
                'idealcol': 'oldbareminraw',
                'stat_type': 'unifatscore',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*0.40,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'unifatscore',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_rawoldbareminraw_std',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*0.20,
                'focuscol': 'rawprice',
                'idealcol': 'oldbareminraw',
                'stat_type': 'unistd',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.484,
                'filterdirection': 'no',
                'metricweight': 1/7,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'allpctdrop_mean',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': -0.245,
                'filterdirection': 'no',
                'metricweight': 1/7,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'kneescore',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0.3312,
                'filterdirection': 'no',
                'metricweight': 1/6,
                'calibration': 'noprepraw',
                'look_back': 0
            },
"""
threshold = 0.0016
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'maxbmaxflatseg',
                'rankascending': 1,
                'threshold': 210.1,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2/5,
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'threshold': 115.36,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2/5,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2/5,
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'kneescore',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0.3312,
                'filterdirection': 'no',
                'metricweight': 1/2/5,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_rawoldbareminraw_std',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 1/2/5,
                'focuscol': 'rawprice',
                'idealcol': 'oldbareminraw',
                'stat_type': 'unistd',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 1/2,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            ],
        'batchtype': 'filter',
        'batchname': 'summer2020temp_stage3v9'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
