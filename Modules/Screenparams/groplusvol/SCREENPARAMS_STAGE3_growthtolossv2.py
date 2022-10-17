"""
Title: SCREENPARAMS - STAGE 3 - growth to loss
Date Started: Nov 28, 2020
Version: 2
Version Start Date: Nov 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description: Only any time drops metrics.
growth to loss

"""
from STRATTEST_FUNCBASE_MMBM import growthtoloss_single

gmeth = 'resampslopescore'
lmeth = 'unifatscore'
stat_type = 'median'
combtype = 'sum'
aggtype = 'median'
agg2type = 'mean'
resamplefreq = 120
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_rsss{resamplefreq}_{aggtype}_ufrtos_{stat_type}_{combtype}',
    'scriptparams': [
        {
            'metricname': 'growthtoloss',
            'metricfunc': growthtoloss_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': 1,
            'groparams': {
                'gmeth': gmeth,
                'resamplefreq': resamplefreq,
                'aggtype': aggtype,
                'agg2type': agg2type,
                'freqlist': [7, 15, 30, 60, 90]
            },
            'lossparams': {
                'lmeth': lmeth,
                #'uppercol': 'rawprice',
                #'lowercol': 'oldbareminraw',
                'idealcol': 'straight',
                'focuscol': 'rawprice',
                'stat_type': stat_type,
            },
            'calibration': 'noprepoldbareminraw',
            'combtype': combtype,
            'look_back': 0
        }
        ]
    }
