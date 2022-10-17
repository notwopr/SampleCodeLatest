"""
Title: 2018 METHOD - STAGE 3
Date Started: Sept 29, 2020
Version: 15
Version Start Date: Oct 11, 2020
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

    Shape Factor: 1/2 (VOLATILITY v1)
        Difference between true graph and straight line 1/2
            Magnitude of that difference 1/2
                mean 1/2  unifatscore_oldbareminrawstraight_mean
                median 1/2  unifatscore_oldbareminrawstraight_median
            Regularity of that difference 1/2
                Std 1/2  unifatscore_oldbareminrawstraight_std
                mad 1/2  unifatscore_oldbareminrawstraight_mad
        Difference between raw price from true graph 1/2
            Magnitude of that difference 1/2
                mean 1/2  unifatscore_rawoldbareminraw_mean
                median 1/2  unifatscore_rawoldbareminraw_median
            Regularity of that difference 1/2
                Std 1/2  unifatscore_rawoldbareminraw_std
                mad 1/2  unifatscore_rawoldbareminraw_mad
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': '2018METHODv15',
    'scriptparams': [
        {
            'metricname': 'unifatscore_rawoldbareminraw_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mean',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_std',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'std',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_mad',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mad',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_mean',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_median',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_std',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'std',
            'calibration': 'noprepoldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_mad',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/2)*(1/2)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'mad',
            'calibration': 'noprepoldbareminraw',
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
        },
        ]
    }
