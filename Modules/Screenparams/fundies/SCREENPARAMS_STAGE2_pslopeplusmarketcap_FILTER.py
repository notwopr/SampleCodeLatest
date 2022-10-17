"""
Title: SCREENPARAM - positiveslope plus marketcap - FILTER
Date Started: Mar 5, 2021
Version: 1.00
Version Start Date: Mar 5, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description: Params for getting current marketcap.
"""
from STRATTEST_FUNCBASE_FUNDAMENTALS import fundypositiveslope_single, currmarketcap_single

filterd = 'above'
threshold = 0
look_back = 0
datatype = 'freecashflow'
filterd_marketcap = 'betweeninclusive'
upperthreshold = 10000000000
lowerthreshold = 1000000000
stage2_params = {
    'scriptname': f'pslope_{datatype}FILTER{filterd}{threshold}_LB{look_back}plusmarketcap{filterd}{upperthreshold}and{lowerthreshold}',
    'scriptparams': [
        {
            'metricname': f'fundypositiveslope_{datatype}',
            'metricfunc': fundypositiveslope_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': threshold,
            'filterdirection': filterd,
            'metricweight': 1,
            'datatype': datatype,
            'calibration': [],
            'data': '',
            'look_back': look_back
        },
        {
            'metricname': 'currmarketcap',
            'metricfunc': currmarketcap_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'upperthreshold': upperthreshold,
            'lowerthreshold': lowerthreshold,
            'filterdirection': filterd_marketcap,
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': look_back
        }
        ]
        }
