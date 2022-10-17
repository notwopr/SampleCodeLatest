"""
Title: SCREENPARAMS - STAGE 3 - agemaxdd + bestgrowth
Date Started: Nov 17, 2020
Version: 10.00
Version Start Date: Nov 17, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
STAGE3_ageoldermaxdrop 1/3
    age_older
    allpctdrop_rawoldbareminraw_max
rawtostraight  1/3
    Difference between raw graph and straight line
    Magnitude of that difference
        unifatscore_rawstraight_mean 1/2
        unifatscore_rawstraight_median 1/2
rawoldbareminraw 1/3
    Difference between raw graph and oldbareminraw line
        Magnitude of that difference
            unifatscore_rawoldbareminraw_mean 1/2
            unifatscore_rawoldbareminraw_median 1/2

"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'STAGE3_ageoldermaxdrop',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_ageoldermaxdrop',
        'scriptweight': 1/3
    },
    {
        'scriptnickname': 'STAGE3_rawtostraight_mag',
        'scriptfilename': 'Screenparams.rawto.SCREENPARAMS_STAGE3_rawtostraight_mag',
        'scriptweight': 1/3
    },
    {
        'scriptnickname': 'STAGE3_rawtobmin_mag',
        'scriptfilename': 'Screenparams.rawto.SCREENPARAMS_STAGE3_rawtobmin_mag',
        'scriptweight': 1/3
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_agemaxddplusbestgrowthv10')
