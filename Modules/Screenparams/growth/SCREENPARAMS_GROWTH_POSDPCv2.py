"""
Title: SCREENPARAMS - STAGE 3 - GROWTH
Date Started: Jan 7, 2021
Version: 2.00
Version Start Date: Jan 26, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
    POSDPC MAG AVG
        posnegmag_pos_avg 1/2
    POSDPC PREVALENCE
        posnegprevalence_pos 1/2

"""
from STRATTEST_FUNCBASE_RAW import posnegmag_single, posnegprevalence_single, statseglen_single


posnegprevalence_posweight = 1/2
posnegmag_posweight = 1/2
price_calib = 'trueline'
dpc_calib = 'truedpc'
stage3_params = {
    'scriptname': f'GROWTH_POSDPCv2_{dpc_calib}',
    'scriptparams': [
        {
            'metricname': 'posnegmag_pos_avg',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'stat_type': 'avg',
            'metricweight': posnegmag_posweight,
            'calibration': [price_calib],
            'data': dpc_calib,
            'look_back': 0
        },
        {
            'metricname': 'posnegprevalence_pos',
            'metricfunc': posnegprevalence_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'metricweight': posnegprevalence_posweight,
            'calibration': [price_calib],
            'data': dpc_calib,
            'look_back': 0
        }
        ]
        }
