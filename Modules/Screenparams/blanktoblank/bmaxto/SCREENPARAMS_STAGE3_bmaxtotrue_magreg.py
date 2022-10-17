"""
Title: SCREENPARAMS - STAGE 3 - bmaxtotrue_magreg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between bmax graph and true line
    Magnitude of that difference 1/2
        unifatscore_bmaxtrue_mean 1/2
        unifatscore_bmaxtrue_median 1/2
    Regularity of that difference 1/2
        unifatscore_bmaxtrue_std 1/2
        unifatscore_bmaxtrue_mad 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'bmaxtotrue_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_bmaxtotrue_mag',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'bmaxtotrue_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_bmaxtotrue_reg',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_bmaxtotrue_magreg')
