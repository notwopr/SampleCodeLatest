"""
Title: 2018 METHOD - STAGE 3
Date Started: Sept 29, 2020
Version: 1
Version Start Date: Sept 29, 2020
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

    Shape Factor: 1/2
        unisqueezefactor 1/2
            unisqueezefactor_mean 1/2
            unisqueezefactor_median 1/2
        squeezearea 1/2
"""

stage3_params = {
    'scriptname': '2018METHODv1',
    'scriptparams': [
        {
            'metricname': 'unisqueezefactor_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2),
            'stat_type': 'mean',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'unisqueezefactor_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2),
            'stat_type': 'median',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'squeezearea',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2),
            'stat_type': 'area',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'look_back': 360*5
        },
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'look_back': 360*3
        },
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'look_back': 360*4
        },
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'look_back': 360*2
        },
        {
            'metricname': 'slopescore',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'look_back': 360
        },
        {
            'metricname': 'segbackslopescore_y1',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'segsback': 0,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y2',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'segsback': 1,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y3',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'segsback': 2,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y4',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'segsback': 3,
            'winlen': 360,
            'look_back': 0
        },
        {
            'metricname': 'segbackslopescore_y5',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/5),
            'calibration': 'noprepraw',
            'segsback': 4,
            'winlen': 360,
            'look_back': 0
        }
        ]
    }