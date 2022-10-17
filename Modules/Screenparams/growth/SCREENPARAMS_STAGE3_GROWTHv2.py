"""
Title: SCREENPARAMS - STAGE 3 - GROWTH
Date Started: Jan 7, 2021
Version: 2.00
Version Start Date: Jan 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
Divide in half metrics into Slope group and DPC group.
SLOPE 1/2
    slopescore
DPC COMPS 1/2
    CONSECUTIVE POSDPC 1/2
        PSEG AVG
            statseglen_pos_avg
    DPC 1/2
        POSDPC MAG AVG
            posnegmag_pos_avg 1/2
        POSDPC PREVALENCE
            posnegprevalence_pos 1/2

"""
from STRATTEST_FUNCBASE_RAW import posnegmag_single, posnegprevalence_single, statseglen_single, slopescorefocus_single

slopescoreweight = 1/2
posnegprevalence_posweight = 1/8
posnegmag_posweight = 1/8
avgpseglenweight = 1/4
focuscol = 'baremaxraw'
stage3_params = {
    'scriptname': 'GROWTHv2',
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
