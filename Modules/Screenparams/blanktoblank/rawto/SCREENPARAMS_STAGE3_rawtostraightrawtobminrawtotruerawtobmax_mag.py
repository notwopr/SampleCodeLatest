"""
Title: SCREENPARAMS - STAGE 3 - rawtostraightrawtobminrawtotrue_mag
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and straight line 1/4
    Magnitude of that difference
        unifatscore_rawstraight_mean 1/2
        unifatscore_rawstraight_median 1/2
Difference between raw graph and bmin line 1/4
    Magnitude of that difference
        unifatscore_rawbmin_mean 1/2
        unifatscore_rawbmin_median 1/2
Difference between raw graph and true line 1/4
    Magnitude of that difference
        unifatscore_rawtrue_mean 1/2
        unifatscore_rawtrue_median 1/2
Difference between raw graph and baremaxraw line 1/4
    Magnitude of that difference
        unifatscore_rawbaremaxraw_mean 1/2
        unifatscore_rawbaremaxraw_median 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'rawtostraight_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtostraight_mag',
        'scriptweight': 1/4
    },
    {
        'scriptnickname': 'rawtobmin_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmin_mag',
        'scriptweight': 1/4
    },
    {
        'scriptnickname': 'rawtotrue_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtotrue_mag',
        'scriptweight': 1/4
    },
    {
        'scriptnickname': 'rawtobmax_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmax_mag',
        'scriptweight': 1/4
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtostraightrawtobminrawtotruerawtobmax_mag')
