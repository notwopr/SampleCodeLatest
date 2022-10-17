"""
Title: SCREENPARAM - CURRENT TO ATH date
Date Started: Mar 6, 2022
Version: 1.00
Version Start Date: Mar 6, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
"""
from Modules.metriclibrary.STRATTEST_FUNCBASE_RAW import currtoathdays_single
ath_occur = 'last'
stage3_params = {
    'scriptname': f'currtoathdaysonly_descending_{ath_occur}',
    'scriptparams': [
        {
            'metricname': f'currtoathdays_descending_{ath_occur}',
            'metricfunc': currtoathdays_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'ath_occur': ath_occur,  # ath_occur designates how to calculate the preATH period.  'first' means take the date where the first ATH occur if there are several occurrences of the ATH price.  'last' means take the last occurrence.
            'min_preath_age': 2,
            'calibration': [''],
            'data': '',
            'look_back': 0
        }
        ]
        }
