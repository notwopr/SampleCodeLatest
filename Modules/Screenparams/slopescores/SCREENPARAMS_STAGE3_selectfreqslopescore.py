"""
Title: STAGE 3 - select sample frequency slopescore
Date Started: Dec 12, 2020
Version: 1.0
Version Start Date: Dec 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

"""
from STRATTEST_FUNCBASE_RAW import selectsampfreqslopescore_single

aggtype = 'median'
agg2type = 'mean'
freqlist = [7, 15, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_selectss_{aggtype}_{agg2type}_f{freqlist}',
    'scriptparams': [
        {
            'metricname': 'selectsampfreqslopescore',
            'metricfunc': selectsampfreqslopescore_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'freqlist': freqlist,
            'aggtype': aggtype,
            'agg2type': agg2type,
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': 'noprepraw',
            'look_back': 0
        }
        ]
    }
