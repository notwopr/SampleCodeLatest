"""
Title: 2018 METHOD - STAGE 2 SUMMER2020
Date Started: Jan 2, 2021
Version: 1
Version Start Date: Jan 2, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Description:
slopescore_1yr <0.0011
slopescore_2yr <0.0011
slopescore_3yr <0.0011
slopescore_4yr <0.0011
slopescore_5yr <0.0011
segbackslopescore_y1 <0.0011
segbackslopescore_y2 <0.0011
segbackslopescore_y3 <0.0011
segbackslopescore_y4 <0.0011
segbackslopescore_y5 <0.0011
unifatscore_rawoldbareminraw_mean <0.0252
unifatscore_rawoldbareminraw_median  <0.0252
unifatscore_rawstraight_mean <0.0484
unifatscore_rawstraight_median <0.0484
"""
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single, segbackslopescore_single
from STRATTEST_FUNCBASE_MMBM import unifatshell_single

stage2_params = {
    'scriptname': 'summer2020vM_multithresh_24v2',
    'scriptparams': [
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 360*5
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 360*4
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 360*3
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 360*2
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 360
        },
        {
            'metricname': 'segbackslopescore_y2',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'segsback': 1,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y3',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'segsback': 2,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y4',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'segsback': 3,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y5',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0.0011,
            'filterdirection': 'above',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'segsback': 4,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.0252,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mean',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_median',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.0252,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawstraight_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.0484,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': ['straight'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawstraight_median',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.0484,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': ['straight'],
            'data': '',
            'look_back': 0
        }
        ]
    }
