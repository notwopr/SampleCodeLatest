"""
Title: SCREENPARAMS - STAGE 3 - MARKETBEATERv2
Date Started: Sept 29, 2020
Version: 2.00
Version Start Date: Sept 29, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Screen params.
"""
from STRATTEST_FUNCBASE_RAW import marketbeaterv2_single
bweights = {
    '^IXIC': 1,
    #'^INX': 0,
    #'^DJI': 0
}
avgtype = 'median'
usedev = 'no'

stage3_params = {
    'scriptname': f'STAGE3_marketbeaterv2_{list(bweights.keys())}_{avgtype}_{usedev}',
    'scriptparams': [
        {
            'metricname': 'marketbeaterv2',
            'metricfunc': marketbeaterv2_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'calibration': 'noprepraw',
            'bweights': bweights,
            'avgtype': avgtype,
            'usedev': usedev,
            'look_back': 0
        }
        ]
    }
