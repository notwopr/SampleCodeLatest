"""
Title: SCREENPARAMS - STAGE 3 - rawtobmin_magreg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and bmin line
    Magnitude of that difference 1/2
        unifatscore_rawbmin_mean 1/2
        unifatscore_rawbmin_median 1/2
    Regularity of that difference 1/2
        unifatscore_rawbmin_std 1/2
        unifatscore_rawbmin_mad 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'rawtobmin_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmin_mag',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'rawtobmin_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmin_reg',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtobmin_magreg')
