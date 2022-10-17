"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 11.00
Version Start Date: Apr 14, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
slopescore
dropscore
unifatscore_rawbaremaxraw_avg
unifatscore_rawbaremaxraw_dev
slopetounifatratio
slopetodropscoreratio
"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single, dropscore_single, slopetounifatratio_single, slopetodropscoreratio_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single

unifatscoreweight = 0
unifatscoredevweight = 0
slopescoreweight = 0
dropscoreweight = 0
slopetounifatweight = 1/2
slopetodropweight = 1/2
stage3_params = {
    'scriptname': 'STAGE3_groplusvolv11',
    'scriptparams': [
        {
            'metricname': 'slopetounifatratio',
            'metricfunc': slopetounifatratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': slopetounifatweight,
            'focuscol': 'rawprice',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'slopetodropscoreratio',
            'metricfunc': slopetodropscoreratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': slopetodropweight,
            'focuscol': 'rawprice',
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
            'focuscol': 'rawprice',
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': dropscoreweight,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
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
        }
        ]
        }
