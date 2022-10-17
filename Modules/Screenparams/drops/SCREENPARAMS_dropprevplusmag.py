"""
Title: SCREENPARAMS - drop prev + drop mag
Date Started: Feb 16, 2021
Version: 1.00
Version Start Date: Feb 16, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
"""
from STRATTEST_FUNCBASE_MMBM import dropmag_single, dropprev_single
uppercol = 'oldbareminraw'
lowercol = 'rawprice'
calibcol = 'oldbareminraw'
dropmagweight = 1/2
dropprevweight = 1/2
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'dropprevplusmag_{uppercol}to{lowercol}',
    'scriptparams': [
        {
            'metricname': 'drop_mag_avg',
            'metricfunc': dropmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': dropmagweight,
            'uppercol': uppercol,
            'lowercol': lowercol,
            'stat_type': 'avg',
            'calibration': [calibcol],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'drop_prev',
            'metricfunc': dropprev_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': dropprevweight,
            'uppercol': uppercol,
            'lowercol': lowercol,
            'calibration': [calibcol],
            'data': '',
            'look_back': 0
        }
        ]
    }
