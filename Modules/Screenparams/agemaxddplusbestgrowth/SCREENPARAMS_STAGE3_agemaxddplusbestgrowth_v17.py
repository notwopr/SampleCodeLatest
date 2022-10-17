"""
Title: SCREENPARAMS - STAGE 3 - agemaxdd + bestgrowth
Date Started: Nov 18, 2020
Version: 17.00
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
        Regularity of that difference
            unifatscore_rawbmin_std 1/2
            unifatscore_rawbmin_mad 1/2
    Difference between raw graph and straight line 1/2
        Regularity of that difference
            unifatscore_bminstraight_std 1/2
            unifatscore_bminstraight_mad 1/2


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
        'scriptnickname': 'STAGE3_rawtobmintostraight_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtobmintostraight_reg',
        'scriptweight': 1/2
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_agemaxddplusbestgrowthv17')
