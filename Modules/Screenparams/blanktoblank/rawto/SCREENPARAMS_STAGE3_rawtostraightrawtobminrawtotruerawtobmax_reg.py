"""
Title: SCREENPARAMS - STAGE 3 - rawtostraightrawtobminrawtotrue_reg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and straight line 1/4
    Regularity of that difference
        unifatscore_rawstraight_std 1/2
        unifatscore_rawstraight_mad 1/2
Difference between raw graph and bmin line 1/4
    Regularity of that difference
        unifatscore_rawbmin_std 1/2
        unifatscore_rawbmin_mad 1/2
Difference between raw graph and true line 1/4
    Regularity of that difference
        unifatscore_rawtrue_std 1/2
        unifatscore_rawtrue_mad 1/2
Difference between raw graph and baremaxraw line 1/4
    Regularity of that difference
        unifatscore_rawbaremaxraw_std 1/2
        unifatscore_rawbaremaxraw_mad 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'rawtostraight_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtostraight_reg',
        'scriptweight': 1/4
    },
    {
        'scriptnickname': 'rawtobmin_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmin_reg',
        'scriptweight': 1/4
    },
    {
        'scriptnickname': 'rawtotrue_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtotrue_reg',
        'scriptweight': 1/4
    },
    {
        'scriptnickname': 'rawtobmax_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmax_reg',
        'scriptweight': 1/4
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtostraightrawtobminrawtotruerawtobmax_reg')
