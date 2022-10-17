"""
Title: scratchparams
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, dropscoreratio_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'dropscoreplusdropscoreratio',
    'scriptparams': [
        {
            'metricname': 'drop_score_avg',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/2,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'dropscoreratio_avg',
            'metricfunc': dropscoreratio_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 1/2,
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
