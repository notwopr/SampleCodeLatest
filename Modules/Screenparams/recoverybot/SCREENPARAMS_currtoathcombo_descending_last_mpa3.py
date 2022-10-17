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
from Modules.metriclibrary.STRATTEST_FUNCBASE_RAW import currtoathdays_single, currtoathdiff_single
ath_occur = 'last'
min_preath_age = 3
stage3_params = {
    'scriptname': f'currtoathcombo_descending_{ath_occur}',
    'scriptparams': [
        {
            'metricname': f'currtoathdiff_{ath_occur}',
            'metricfunc': currtoathdiff_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'ath_occur': ath_occur,  # ath_occur designates how to calculate the preATH period.  'first' means take the date where the first ATH occur if there are several occurrences of the ATH price.  'last' means take the last occurrence.
            'min_preath_age': min_preath_age,
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': f'currtoathdays_descending_{ath_occur}',
            'metricfunc': currtoathdays_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'ath_occur': ath_occur,  # ath_occur designates how to calculate the preATH period.  'first' means take the date where the first ATH occur if there are several occurrences of the ATH price.  'last' means take the last occurrence.
            'min_preath_age': min_preath_age,
            'calibration': [''],
            'data': '',
            'look_back': 0
        }
        ]
        }
