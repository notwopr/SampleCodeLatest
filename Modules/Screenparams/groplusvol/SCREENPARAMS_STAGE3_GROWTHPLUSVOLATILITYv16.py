"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 16.00
Version Start Date: Aug 16, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Version:
15: combining several scripts (all version 15x) in different combinations.

"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'v16smooth',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv16smoothv1',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'v16growth_LB1',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv16growthv1_LB1',
        'scriptweight': 0.1
    },
    {
        'scriptnickname': 'v16growth_LB2',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv16growthv1_LB2',
        'scriptweight': 0.1
    },
    {
        'scriptnickname': 'v16growth_LB3',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv16growthv1_LB3',
        'scriptweight': 0.1
    },
    {
        'scriptnickname': 'v16growth_LB4',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv16growthv1_LB4',
        'scriptweight': 0.1
    },
    {
        'scriptnickname': 'v16growth_LB5',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv16growthv1_LB5',
        'scriptweight': 0.1
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv16')
