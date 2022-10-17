"""
Title: scratchparams
"""
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single, accretiontally_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY

scratch_params = {
    'scriptname': 'accretionscores',
    'scriptparams': [
        {
            'metricname': 'accretionscore_pos',
            'metricfunc': accretionscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'accret_type': 'pos',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'accretiontally_pos',
            'metricfunc': accretiontally_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': 'rawprice',
            'accret_type': 'pos',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        ]
    }
