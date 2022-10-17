"""
Title: SCREENPARAMS - STAGE 3 - GROWTH
Date Started: Jan 24, 2021
Version: 5.00
Version Start Date: Jan 24, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

ideal slopescore 1/2
closeness to idealslope 1/2
    unifatscore_raw{ideal}_avg 1/2
    unifatscore_raw{ideal}_dev 1/2
"""
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
idealcol = 'straight'
idealcalib = 'straight'
slopeweight = 1/2
closeavgweight = 1/4
closedevweight = 1/4
stage3_params = {
    'scriptname': f'GROWTHv5_{idealcol}',
    'scriptparams': [
        {
            'metricname': f'slopescore_{idealcol}',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': slopeweight,
            'focuscol': idealcol,
            'calibration': [idealcalib],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': f'unifatscore_raw{idealcol}_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': closeavgweight,
            'focuscol': 'rawprice',
            'idealcol': idealcol,
            'stat_type': 'avg',
            'calibration': [idealcalib],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': f'unifatscore_raw{idealcol}_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': closedevweight,
            'focuscol': 'rawprice',
            'idealcol': idealcol,
            'stat_type': 'dev',
            'calibration': [idealcalib],
            'data': '',
            'look_back': 0
        }
        ]
        }
