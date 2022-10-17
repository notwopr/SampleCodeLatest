"""
Title:  WINNER THRESHOLD FINDER - ADDL WINNER FILTERS
Date Started: Feb 17, 2021
Version: 2.00
Version Start Date: Feb 17, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2: removed dropscoreratio because too strict.
FILTERS:
dropscore <	-0.25
maxdrop (lifetime)  < -0.7
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, allpctdrops_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
filter_params = {
    'scriptname': 'winnerpretestfiltersv1',
    'scriptparams': [
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.25,
            'filterdirection': 'above',
            'metricweight': 1,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_max',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.70,
            'filterdirection': 'above',
            'metricweight': 1,
            'calibration': ['oldbareminraw'],
            'data': '',
            'uppercol': 'rawprice',
            'lowercol': 'oldbareminraw',
            'stat_type': 'min',
            'look_back': 0
        }

        ]
    }
