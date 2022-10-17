"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 15.00
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
        'scriptnickname': 'v15e_LB1',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv15e',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'v15a_LB2',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv15a',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv15')
