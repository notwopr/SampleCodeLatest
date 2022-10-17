"""
Title: STAGE 3 - posnegratios
Date Started: Dec 30, 2020
Version: 1.00
Version Start Date: Dec 30, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
psegnegsegratio 1/3
posnegprevratio 1/3
posnegmagratio 1/3
"""
from STRATTEST_FUNCBASE_RAW import posnegmagratio_single, posnegprevratio_single, psegnegsegratio_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_posnegratios',
    'scriptparams': [
        {
            'metricname': 'psegnegsegratio',
            'metricfunc': psegnegsegratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1/3,
            'stat_type': 'avg',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevratio',
            'metricfunc': posnegprevratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/3,
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagratio',
            'metricfunc': posnegmagratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'stat_type': 'avg',
            'metricweight': 1/3,
            'calibration': 'raw',
            'look_back': 0
        }
        ]
    }
