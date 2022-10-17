"""
Title: SCREENPARAMS - STAGE 3 - LAST DIP BOT
Date Started: Oct 10, 2020
Version: 1
Version Start Date: Oct 10, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Stage 3 of Last dip bot

Last dip bot finds stocks that dipped in price at the end of their history but otherwise were quality stocks.
Scheme is as follows:
    Filter pool using
        SCREENPARAMS_STAGE2_PART1_lastdipbot
            Filter out those without a dip in last day
            Filter out those that do not have a reg1pct between 80 and 95%.
            Filter out those whose lastdiplen is not between 20 and 180 days.
            Filter out those whose reg1reg2ratio >= 1.
    Stage 3: Rank by weighing region 1's qualscore and reg1reg2ratio_single

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_lastdipbot',
    'scriptparams': [
        {
            'metricname': 'regqualscore_reg1',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1/2,
            'region': 'reg1',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'reg1reg2ratio',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1/2,
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'lastdiplen',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'reg1stats_min',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'min',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'reg1stats_avg',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'avg',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'reg1stats_max',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'stat_type': 'max',
            'calibration': 'noprepbaremaxraw',
            'look_back': 0
        }
        ]
    }
