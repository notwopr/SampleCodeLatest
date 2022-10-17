"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 4.00
Version Start Date: Feb 5, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Growth v1 + VOLATILITY V7 + shapev1


"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'growthv2',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHv1',
        'scriptweight': 1/3
    },
    {
        'scriptnickname': 'volatilityv7',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_VOLATILITYv7',
        'scriptweight': 1/3
    },
    {
        'scriptnickname': 'shapev1',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_SHAPEv1',
        'scriptweight': 1/3
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv4')
