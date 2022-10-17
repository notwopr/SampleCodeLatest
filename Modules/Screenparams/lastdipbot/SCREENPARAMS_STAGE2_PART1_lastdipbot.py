"""
Title: SCREEN PARAMS - STAGE 2 PART I - LAST DIP BOT
Date Started: Oct 10, 2020
Version: 1.00
Version Start Date: Oct 11, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Filters out stocks that don't have dip activity at the end of the given price history. (filters out stocks whose baremaxraw-bareminraw value on the last day of the price history is 0)

"""
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2part1_params = {
    'scriptname': 'STAGE2_PART1_lastdipbot',
    'scriptparams': [
        {
            'metricname': 'dipfinder',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'reg1pct',
            'rankascending': 0,
            'lowerthreshold': 0.8,
            'upperthreshold': 0.95,
            'thresholdtype': 'absolute',
            'filterdirection': 'between',
            'metricweight': 0,
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'reg1reg2ratio',
            'rankascending': 1,
            'threshold': 1,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'lastdiplen',
            'rankascending': 0,
            'lowerthreshold': 20,
            'upperthreshold': 180,
            'thresholdtype': 'absolute',
            'filterdirection': 'between',
            'metricweight': 0,
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        }
        ]
    }
