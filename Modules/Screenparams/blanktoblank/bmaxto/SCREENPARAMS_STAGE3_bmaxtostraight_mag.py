"""
Title: SCREENPARAMS - STAGE 3 - bmaxtostraight_mag
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between bmax graph and straight line
    Magnitude of that difference
        unifatscore_bmaxstraight_mean 1/2
        unifatscore_bmaxstraight_median 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_bmaxtostraight_mag',
    'scriptparams': [
        {
            'metricname': 'unifatscore_bmaxstraight_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_bmaxstraight_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        }
        ]
    }
