"""
Title: STAGE 3 - posnegratio product margindpc
Date Started: Jan 1, 2021
Version: 1.00
Version Start Date: Jan 1, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
psegnegsegratio * posnegprevratio * posnegmagratio
but on margindpc data
Versions:

"""
from STRATTEST_FUNCBASE_RAW import posnegratioproduct_single
bweights = {
    '^IXIC': 1,
    #'^INX': 0,
    #'^DJI': 0
}
stat_type = 'avg'
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_posnegratioproduct_margindpc_{stat_type}',
    'scriptparams': [
        {
            'metricname': 'posnegratioproduct',
            'metricfunc': posnegratioproduct_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'stat_type': stat_type,
            'calibration': 'nonzerodpcmargins',
            'bweights': bweights,
            'look_back': 0
        }
        ]
    }
