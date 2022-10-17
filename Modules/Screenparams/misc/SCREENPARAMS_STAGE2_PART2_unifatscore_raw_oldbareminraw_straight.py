"""
Title: SCREEN PARAMS - STAGE 2 PART 2 - unifatscore_rawoldbareminraw and oldbareminraw to straight
Date Started: Sept 29, 2020
Version: 1
Version Start Date: Sept 29, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
DESCRIPTION:
Unifatscore_rawoldbareminraw
Unifatscore_oldbareminrawstraight

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'unifatscore_rawoldbareminraw_mean',
                'rankascending': 1,
                'threshold': 0.0252,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'focuscol': 'rawprice',
                'idealcol': 'oldbareminraw',
                'stat_type': 'mean',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight_mean',
                'rankascending': 1,
                'threshold': 0.0484,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'mean',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'rawtooldbareminrawtostraight'
    }
]

# STORE
stage2part2_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
