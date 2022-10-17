"""
Title: SCREENPARAM - Marketcap - FILTER
Date Started: Mar 4, 2021
Version: 1.00
Version Start Date: Mar 4, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description: Params for getting current marketcap.
"""
from STRATTEST_FUNCBASE_FUNDAMENTALS import currmarketcap_single

filterd = 'betweeninclusive'
upperthreshold = 20000000000
lowerthreshold = 15000000000
stage2_params = {
    'scriptname': f'currmarketcap_FILTER{filterd}{upperthreshold}and{lowerthreshold}',
    'scriptparams': [
        {
            'metricname': 'currmarketcap',
            'metricfunc': currmarketcap_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'upperthreshold': upperthreshold,
            'lowerthreshold': lowerthreshold,
            'filterdirection': filterd,
            'metricweight': 1,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
        }
