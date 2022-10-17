"""
Title:  SCREEN PARAMS - STAGE 2 FILTERS
Date Started: Jan 21, 2021
Version: 1.00
Version Start Date: Jan 21, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

FILTERS:
slopescore over past 1 year	0.0019
slopescore over past 2 years	0.0015
slopescore over past 3 years	0.00126
slopescore over past 4 years	0.0011
slopescore over past 5 years	0.0009
slopescore (lifetime)	0.0003
dropscore	-0.25
maxdrop (lifetime)	-0.7
"""
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single
from STRATTEST_FUNCBASE_MMBM import dropscore_single, allpctdrops_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'STAGE2FILTERSv1',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0003,
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0009,
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 360*5
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 360*4
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.00126,
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 360*3
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0015,
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 360*2
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0019,
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 360
        },
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
        }

        ]
    }
