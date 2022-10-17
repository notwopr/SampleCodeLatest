"""
Title: SCREENPARAMS - STAGE 3 - agemaxdd + bestgrowth
Date Started: Nov 18, 2020
Version: 14.00
Version Start Date: Nov 18, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
STAGE3_ageoldermaxdrop 1/2
    age_older
    allpctdrop_rawoldbareminraw_max
rawtostraight  1/4
    Difference between raw graph and straight line
        Regularity of that difference
            unifatscore_rawstraight_std 1/2
            unifatscore_rawstraight_mad 1/2

rawoldbareminraw 1/4
    Difference between raw graph and oldbareminraw line
        Regularity of that difference
            unifatscore_rawoldbareminraw_std 1/2
            unifatscore_rawoldbareminraw_mad 1/2


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
        'scriptnickname': 'STAGE3_rawtostraight_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtostraight_reg',
        'scriptweight': 1/4
    },
    {
        'scriptnickname': 'STAGE3_rawtobmin_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmin_reg',
        'scriptweight': 1/4
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_agemaxddplusbestgrowthv14')
