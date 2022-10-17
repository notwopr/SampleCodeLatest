"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 13.00
Version Start Date: Apr 14, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
slopescore 1/2
smoothness 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'slopescore',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_slopescore',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'smoothness_rankstagev9k',
        'scriptfilename': 'Screenparams.Smoothness.SCREENPARAMS_smoothness_rankstagev9k',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv13')
