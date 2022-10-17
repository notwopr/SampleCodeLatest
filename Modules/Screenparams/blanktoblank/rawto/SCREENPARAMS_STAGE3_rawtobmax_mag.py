"""
Title: SCREENPARAMS - STAGE 3 - rawtosbmax_mag
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and baremaxraw line
    Magnitude of that difference
        unifatscore_rawbaremaxraw_mean 1/2
        unifatscore_rawbaremaxraw_median 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_rawtobmax_mag',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawbaremaxraw_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'mean',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawbaremaxraw_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2),
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'median',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        }
        ]
    }
