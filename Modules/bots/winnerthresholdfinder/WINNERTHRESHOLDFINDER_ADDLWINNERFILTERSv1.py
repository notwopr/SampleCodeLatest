"""
Title:  WINNER THRESHOLD FINDER - ADDL WINNER FILTERS
Date Started: Feb 17, 2021
Version: 1.00
Version Start Date: Feb 17, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

FILTERS:
dropscore <	-0.25
maxdrop (lifetime)  < -0.7
dropscore ratio < 1
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, allpctdrops_single, dropscoreratio_single

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
            'metricname': 'dropscoreratio_avg',
            'metricfunc': dropscoreratio_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'equalbelow',
            'metricweight': 1,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'benchticker': '^DJI',
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
