"""
Title: STAGE 2 - resampledss dev filter
Date Started: Apr 27, 2021
Version: 1.0
Version Start Date: Apr 27, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

"""
from STRATTEST_FUNCBASE_RAW import resampledslopescore_single

resamplefreq = 15
focuscol = 'rawprice'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2_params = {
    'scriptname': 'STAGE2_resampss_devfilter',
    'scriptparams': [
        {
            'metricname': 'resampledslopescore_dev',
            'metricfunc': resampledslopescore_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'resamplefreq': resamplefreq,
            'aggtype': 'dev',
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': focuscol,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
