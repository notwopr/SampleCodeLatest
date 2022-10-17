"""
Title: SCREENPARAM - CURRENT TO ATH PRICE DIFF
Date Started: Jan 12, 2021
Version: 2.00
Version Start Date: Feb 21, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
Explanation of threshval and filterdirection
e.g. "above -.10" threshval, means return only those whose percentage drop from ATH was less than 10%.
"""
from Modules.metriclibrary.STRATTEST_FUNCBASE_RAW import currtoathdiff_single
filterd = 'above'
threshval = -0.10
stage2_params = {
    'scriptname': f'currtoathdiff_FILTER{filterd}{threshval}',
    'scriptparams': [
        {
            'metricname': 'currtoath',
            'metricfunc': currtoathdiff_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': threshval,
            'filterdirection': filterd,
            'metricweight': 1,
            'calibration': [''],
            'data': '',
            'look_back': 0
        }
        ]
        }
