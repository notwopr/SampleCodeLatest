"""
Title: scratchparams
"""
from STRATTEST_FUNCBASE_MMBM import dropscoreratio_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'dropscoreratio',
    'scriptparams': [
        {
            'metricname': 'dropscoreratio_avg',
            'metricfunc': dropscoreratio_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'benchticker': '^DJI',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
    }
