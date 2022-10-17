"""
Title: 2018 METHOD - STAGE 3
Date Started: Sept 29, 2020
Version: 24
Version Start Date: Oct 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Description:

    Growth Factor: 1/2
        slopescore 1/2
            slopescore_1yr 1/5
            slopescore_2yr 1/5
            slopescore_3yr 1/5
            slopescore_4yr 1/5
            slopescore_5yr 1/5
        segbackslopescore 1/2
            segbackslopescore_y1 1/5
            segbackslopescore_y2 1/5
            segbackslopescore_y3 1/5
            segbackslopescore_y4 1/5
            segbackslopescore_y5 1/5

    Shape Factor: 1/2 (VOLATILITY v3)
        Difference between raw price from bmin graph
            Magnitude of that difference
                mean 1/2  unifatscore_rawoldbareminraw_mean
                median 1/2  unifatscore_rawoldbareminraw_median
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
from STRATTEST_FUNCBASE_MMBM import unifatshell_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single, segbackslopescore_single
stage3_params = {
    'scriptname': '2018METHODv33',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawoldbareminraw_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
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
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw'],
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
            'metricweight': (1/2)*(1/2)*(1/5),
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
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
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
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
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
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
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
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 360
        },
        {
            'metricname': 'segbackslopescore_y1',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'segsback': 0,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y2',
            'metricfunc': segbackslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
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
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
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
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
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
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'segsback': 4,
            'winlen': 360,
            'look_back': 0
        },
        ]
    }
