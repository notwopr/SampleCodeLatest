"""
Title:  SCREEN PARAMS - STAGE 2 FILTERS
Date Started: Jan 21, 2021
Version: 8
Version Start Date: Aug 17, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Filter out second stage stocks.
Versions:
8: eliminate stocks that don't meet desired minimum slopescore based on age.
FILTERS:
age >= 300 DAYS
slopescore >= minslopescore acceptable
"""
from Modules.metriclibrary.STRATTEST_FUNCBASE_RAW import age_single, slopescorelitmus_single, dgfslopescore_single, slopescorefocus_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'STAGE2FILTERSv8',
    'scriptparams': [
        {
            'metricname': 'age_older',
            'metricfunc': age_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 300,
            'filterdirection': '>=',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'dgfslopescore',
            'metricfunc': dgfslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'dgf': 1,
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [],
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
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'sslitmusratio',
            'metricfunc': slopescorelitmus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'dgf': 1,
            'threshold': 1,
            'filterdirection': '>=',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
