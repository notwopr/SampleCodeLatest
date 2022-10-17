"""
Title: SCREENPARAMS - STAGE 3 - bmaxtobmin_reg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between bmax graph and bmin line
    Regularity of that difference
        unifatscore_baremaxrawoldbareminraw_std 1/2
        unifatscore_baremaxrawoldbareminraw_mad 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_bmaxtobmin_reg',
    'scriptparams': [
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_std',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'std',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_mad',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mad',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        }
        ]
    }
