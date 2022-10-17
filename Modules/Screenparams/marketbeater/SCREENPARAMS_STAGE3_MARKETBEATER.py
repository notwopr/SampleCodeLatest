"""
Title: SCREENPARAMS - STAGE 3 - MARKETBEATER
Date Started: Sept 29, 2020
Version: 1.00
Version Start Date: Sept 29, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Screen params.
"""
from STRATTEST_FUNCBASE_RAW import marketbeater_single
bweights = {
    '^IXIC': 1,
    #'^INX': 0,
    #'^DJI': 0
}
mweights = {
    'pct_pos': 1/4,
    'pct_neg': 1/4,
    'avg_pos': 1/4,
    'avg_neg': 1/4
}

stage3_params = {
    'scriptname': f'STAGE3_marketbeater_{list(bweights.keys())}_{list(mweights.values())}',
    'scriptparams': [
        {
            'metricname': 'marketbeater',
            'metricfunc': marketbeater_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'pctrank',
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': 'noprepraw',
            'bweights': bweights,
            'mweights': mweights,
            'look_back': 0
        }
        ]
    }
