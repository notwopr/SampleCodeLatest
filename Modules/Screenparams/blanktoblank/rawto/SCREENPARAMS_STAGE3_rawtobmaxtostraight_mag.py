"""
Title: SCREENPARAMS - STAGE 3 - rawtobmaxtostraight_mag
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and bmax line 1/2
    Magnitude of that difference
        unifatscore_rawbmax_mean 1/2
        unifatscore_rawbmax_median 1/2
Difference between bmax graph and straight line 1/2
    Magnitude of that difference
        unifatscore_bmaxstraight_mean 1/2
        unifatscore_bmaxstraight_median 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'rawtobmax_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmax_mag',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'bmaxtostraight_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_bmaxtostraight_mag',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtobmaxtostraight_mag')
