"""
Title: SCREENPARAMS - STAGE 3 - rawtobmax_magreg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and bmin line
    Magnitude of that difference 1/2
        unifatscore_rawbaremaxraw_mean 1/2
        unifatscore_rawbaremaxraw_median 1/2
    Regularity of that difference 1/2
        unifatscore_rawbaremaxraw_std 1/2
        unifatscore_rawbaremaxraw_mad 1/2
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
        'scriptnickname': 'rawtobmax_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmax_reg',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtobmax_magreg')
