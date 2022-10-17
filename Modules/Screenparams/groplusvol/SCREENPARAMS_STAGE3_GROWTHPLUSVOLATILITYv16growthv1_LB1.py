"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 16 growth
Version Start Date: Aug 16, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Version:
16: same as version 15 but growth/ratio components separated from smoothness components
1/2 GROWTH
    slopescore (GROWTH)
1/2 RATIO
    slopescore/unifatscore ratio (RATIO)
"""
from STRATTEST_FUNCBASE_MMBM import slopetounifatratiobmin_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single

growth_lbp = 1 * 365
w_slopescore = 1/2
w_ratio = 1/2

stage3_params = {
    'scriptname': 'STAGE3_groplusvolv16growth_LB1',
    'scriptparams': [
        {
            'metricname': 'slopetounifatratiobmin',
            'metricfunc': slopetounifatratiobmin_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': w_ratio,
            'focuscol': 'rawprice',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': growth_lbp
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': w_slopescore,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': growth_lbp
        }
        ]
        }
