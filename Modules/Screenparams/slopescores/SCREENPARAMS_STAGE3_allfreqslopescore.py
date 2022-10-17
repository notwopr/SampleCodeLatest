"""
Title: STAGE 3 - all frequency slopescore
Date Started: Dec 16, 2020
Version: 1.0
Version Start Date: Dec 16, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

"""
from STRATTEST_FUNCBASE_RAW import allsampfreqslopescore_single

aggtype = 'composite'
agg2type = 'composite'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_allsampfreqss_{aggtype}_{agg2type}',
    'scriptparams': [
        {
            'metricname': 'allsampfreqslopescore',
            'metricfunc': allsampfreqslopescore_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'aggtype': aggtype,
            'agg2type': agg2type,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
