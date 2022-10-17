"""
Title: SCREENPARAMS - STAGE 3 - GROWTH
Date Started: Jan 7, 2021
Version: 1.00
Version Start Date: Jan 17, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
GROWTH 1/2
    SLOPE
        slopescore_bmax 1/2
    FATTINESS 1/2
        unifatscore_rawbaremaxraw_avg 1/2
        unifatscore_rawbaremaxraw_dev 1/2
misc 1/2
    CONSECUTIVE POSDPC 1/2
        PSEG AVG
            statseglen_pos_avg
    DPC 1/2
        POSDPC MAG AVG
            posnegmag_pos_avg 1/2
        POSDPC PREVALENCE
            posnegprevalence_pos 1/2

"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_RAW import posnegmag_single, posnegprevalence_single, statseglen_single, slopescorefocus_single

slopescoreweight = 1/4
unifatscoreweight = 1/8
unifatscoredevweight = 1/8
posnegprevalence_posweight = 1/8
posnegmag_posweight = 1/8
avgpseglenweight = 1/4
stage3_params = {
    'scriptname': 'GROWTHv1',
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
            'metricname': 'unifatscore_rawbaremaxraw_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoreweight,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawbaremaxraw_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoredevweight,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'dev',
            'calibration': ['baremaxraw'],
            'data': '',
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
