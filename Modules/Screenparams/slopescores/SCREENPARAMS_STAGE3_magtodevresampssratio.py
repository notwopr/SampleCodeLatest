"""
Title: STAGE 3 - Mag to dev resampleslopescore ratio
Date Started: Apr 27, 2021
Version: 1.0
Version Start Date: Apr 27, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

"""
from STRATTEST_FUNCBASE_RAW import resampledslopescore_single, magtodevresampssratio_single

resamplefreq = 15
focuscol = 'rawprice'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_resampss_metrics',
    'scriptparams': [
        {
            'metricname': 'resampledslopescore_avg',
            'metricfunc': resampledslopescore_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'resamplefreq': resamplefreq,
            'aggtype': 'avg',
            'filterdirection': 'no',
            'metricweight': 0,
            'focuscol': focuscol,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'resampledslopescore_dev',
            'metricfunc': resampledslopescore_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'resamplefreq': resamplefreq,
            'aggtype': 'dev',
            'filterdirection': 'no',
            'metricweight': 0,
            'focuscol': focuscol,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'magtodevresampssratio',
            'metricfunc': magtodevresampssratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'resamplefreq': resamplefreq,
            'aggtype_mag': 'avg',
            'aggtype_dev': 'dev',
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': focuscol,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
