"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 1.00
Version Start Date: Jan 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Growth v1 + VOLATILITY V7


"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'growthv1',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHv1',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'volatilityv8',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_VOLATILITYv8',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv1')
