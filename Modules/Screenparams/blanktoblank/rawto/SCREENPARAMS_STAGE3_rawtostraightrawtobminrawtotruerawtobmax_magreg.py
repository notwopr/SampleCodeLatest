"""
Title: SCREENPARAMS - STAGE 3 - rawtostraightrawtobminrawtotrue_magreg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Mag 1/2
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
Reg 1/2
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
        'scriptnickname': 'rawtofour_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtostraightrawtobminrawtotruerawtobmax_mag',
        'scriptweight': 1/2
    },
    {
        'scriptnickname': 'rawtofour_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtostraightrawtobminrawtotruerawtobmax_reg',
        'scriptweight': 1/2
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtostraightrawtobminrawtotruerawtobmax_magreg')
