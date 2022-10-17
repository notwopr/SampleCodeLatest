"""
Title: STAGE 3 - resampledslopescore
Date Started: Dec 6, 2020
Version: 1.0
Version Start Date: Dec 6, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

"""
from STRATTEST_FUNCBASE_RAW import resampledslopescore_single

aggtype = 'median'
resamplefreq = 7
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_resampss_{aggtype}_f{resamplefreq}',
    'scriptparams': [
        {
            'metricname': 'resampledslopescore',
            'metricfunc': resampledslopescore_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'resamplefreq': resamplefreq,
            'aggtype': aggtype,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
    }
