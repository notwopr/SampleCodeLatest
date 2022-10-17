"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 11.00
Version Start Date: Apr 14, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
slopescore
unifatvolscore
slopetounifatratio
"""
from STRATTEST_FUNCBASE_MMBM import unifatvolscore_single, slopetounifatratio_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single

slopescoreweight = 0
slopetounifatweight = 1
unifatvolscoreweight = 0
stage3_params = {
    'scriptname': 'STAGE3_groplusvolv12',
    'scriptparams': [
        {
            'metricname': 'slopetounifatratio',
            'metricfunc': slopetounifatratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': slopetounifatweight,
            'focuscol': 'rawprice',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatvolscore',
            'metricfunc': unifatvolscore_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': slopescoreweight,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
        }
