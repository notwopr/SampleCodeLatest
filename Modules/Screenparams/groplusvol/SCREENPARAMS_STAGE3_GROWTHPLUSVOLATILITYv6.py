"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 6.00
Version Start Date: Feb 24, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
best avgperf as of 2.24.21 - minmax	reboundbotv2_720
+
best dipscore as of same - standard	WRRtruestdRsWLC2


"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'reboundbotv2_720',
        'scriptfilename': 'Screenparams.SCREENPARAMS_reboundbot_STAGE3v2',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'WRRtruestdRsWLC2',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_WINRATERANKERv23',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv6')
