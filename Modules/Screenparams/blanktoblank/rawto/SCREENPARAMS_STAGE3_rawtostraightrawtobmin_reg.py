"""
Title: SCREENPARAMS - STAGE 3 - rawtostraightrawtobmin_reg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and straight line
    Regularity of that difference 1/2
        unifatscore_rawstraight_std 1/2
        unifatscore_rawstraight_mad 1/2
Difference between raw graph and bmin line
    Regularity of that difference 1/2
        unifatscore_rawbmin_std 1/2
        unifatscore_rawbmin_mad 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'rawtostraight_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtostraight_reg',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'rawtobmin_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmin_reg',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtostraightrawtobmin_reg')
