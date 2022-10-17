"""
Title:  SCREEN PARAMS - STAGE 2 FILTERS
Date Started: Jan 21, 2021
Version: 3.00
Version Start Date: Apr 12, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
FILTERS:

dropscore	-0.25
maxdrop (lifetime)	-0.7
age < 7 years
current price <= 100
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, allpctdrops_single
from STRATTEST_FUNCBASE_RAW import age_single, currprice_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'STAGE2FILTERSv3',
    'scriptparams': [
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.25,
            'filterdirection': 'above',
            'metricweight': 0,
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
        },
        {
            'metricname': 'age_older',
            'metricfunc': age_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 365*7,
            'filterdirection': 'equalbelow',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'currentprice',
            'metricfunc': currprice_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 100,
            'filterdirection': 'equalbelow',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
