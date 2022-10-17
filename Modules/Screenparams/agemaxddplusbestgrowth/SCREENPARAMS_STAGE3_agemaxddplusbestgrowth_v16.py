"""
Title: SCREENPARAMS - STAGE 3 - agemaxdd + bestgrowth
Date Started: Nov 18, 2020
Version: 16.00
Version Start Date: Nov 18, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
STAGE3_ageoldermaxdrop 1/2
    age_older
    allpctdrop_rawoldbareminraw_max
rawtobmintostraight  1/2
    Difference between raw graph and bmin line 1/2
        Magnitude of that difference
            unifatscore_rawbmin_mean 1/2
            unifatscore_rawbmin_median 1/2
    Difference between raw graph and straight line 1/2
        Magnitude of that difference
            unifatscore_bminstraight_mean 1/2
            unifatscore_bminstraight_median 1/2


"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'STAGE3_ageoldermaxdrop',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_ageoldermaxdrop',
        'scriptweight': 1/2
    },
    {
        'scriptnickname': 'STAGE3_rawtobmintostraight_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmintostraight_mag',
        'scriptweight': 1/2
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_agemaxddplusbestgrowthv16')
