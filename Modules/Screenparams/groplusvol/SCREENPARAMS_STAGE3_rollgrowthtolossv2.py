"""
Title: SCREENPARAMS - STAGE 3 - rolling growth to loss
Date Started: Dec 27, 2020
Version: 2
Version Start Date: Feb 25, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description: Only any time drops metrics.
growth to loss

"""
from STRATTEST_FUNCBASE_MMBM import rollgrowthtoloss_single
win_len = 30
agg_type = 'avg'
gmeth = 'slopescore'
focuscol = 'rawprice'
lmeth = 'allpctdrop'
stat_type = 'min'
combtype = 'ratio'
#aggtype = 'median'
#agg2type = 'mean'
#resamplefreq = 120
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_rollgrowthtolossv2',
    'scriptparams': [
        {
            'metricname': 'rollgrowthtoloss',
            'metricfunc': rollgrowthtoloss_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': 1,
            'groparams': {
                'gmeth': gmeth,
                'focuscol': focuscol,
                #'resamplefreq': resamplefreq,
                #'aggtype': aggtype,
                #'agg2type': agg2type,
                #'freqlist': [7, 15, 30, 60, 90]
            },
            'lossparams': {
                'lmeth': lmeth,
                'uppercol': 'baremaxraw',
                'lowercol': 'rawprice',
                'allcalibrations': ['baremaxraw'],
                #'idealcol': 'baremaxraw',
                #'focuscol': 'rawprice',
                'stat_type': stat_type,
            },
            'calibration': [],
            'data': '',
            'combtype': combtype,
            'agg_type': agg_type,
            'win_len': win_len,
            'look_back': 0
        }
        ]
    }
