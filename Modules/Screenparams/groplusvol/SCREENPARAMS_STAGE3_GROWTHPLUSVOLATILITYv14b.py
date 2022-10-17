"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 14b
Version Start Date: Apr 23, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
VERSIONS:
14a: same as 14 but with only weighted metrics included.
14b: same as 14a but with slopescore added.
slopescore
slopetounifatratio
slopetodropscoreratio
"""
from STRATTEST_FUNCBASE_MMBM import slopetounifatratio_single, slopetodropscoreratio_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single


slopescoreweight = 1/2
slopetounifatweight = (1/2)*(1/2)
slopetodropweight = (1/2)*(1/2)
stage3_params = {
    'scriptname': 'STAGE3_groplusvolv14b',
    'scriptparams': [
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
        },
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
            'metricname': 'slopetodropscoreratio',
            'metricfunc': slopetodropscoreratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': slopetodropweight,
            'focuscol': 'rawprice',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
        }
