"""
Title: SCREENPARAMS - STAGE 3 - rawtobmaxtostraight_magreg
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
Difference between raw graph and bmax line 1/2
    Regularity of that difference
        unifatscore_rawbmax_std 1/2
        unifatscore_rawbmax_mad 1/2
Difference between bmax graph and straight line 1/2
    Regularity of that difference
        unifatscore_bmaxstraight_std 1/2
        unifatscore_bmaxstraight_mad 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'rawtobmaxtostraight_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmaxtostraight_mag',
        'scriptweight': 1/2
    },
    {
        'scriptnickname': 'rawtobmaxtostraight_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmaxtostraight_reg',
        'scriptweight': 1/2
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtobmaxtostraight_magreg')
