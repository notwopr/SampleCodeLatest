"""
Title: SCREENPARAMS - STAGE 3 - GROWTH
Date Started: Jan 7, 2021
Version: 3.00
Version Start Date: Jan 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
Divide into three equal groups, slope, consecdpc, and dpc metrics.

SLOPE
    slopescore 1/3
CONSECUTIVE POSDPC
    PSEG AVG
        statseglen_pos_avg 1/3
DPC 1/2
    POSDPC MAG AVG
        posnegmag_pos_avg 1/6
    POSDPC PREVALENCE
        posnegprevalence_pos 1/6

"""
from STRATTEST_FUNCBASE_RAW import posnegmag_single, posnegprevalence_single, statseglen_single, slopescorefocus_single

slopescoreweight = 1/3
posnegprevalence_posweight = 1/6
posnegmag_posweight = 1/6
avgpseglenweight = 1/3
focuscol = 'baremaxraw'
stage3_params = {
    'scriptname': 'GROWTHv3',
    'scriptparams': [

        {
            'metricname': 'statseglen_pos_avg',
            'metricfunc': statseglen_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': avgpseglenweight,
            'mode': 'positive',
            'stat_type': 'avg',
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
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
            'calibration': [],
            'data': 'dpc',
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
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': slopescoreweight,
            'focuscol': 'baremaxraw',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
        }
