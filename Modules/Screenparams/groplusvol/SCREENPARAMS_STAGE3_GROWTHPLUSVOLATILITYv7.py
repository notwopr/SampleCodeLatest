"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 7.00
Version Start Date: Mar 1, 2021
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
        'scriptnickname': 'age_older',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_age_olderbetter',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': '2018Methodv33',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_2018METHODv33',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv7')
