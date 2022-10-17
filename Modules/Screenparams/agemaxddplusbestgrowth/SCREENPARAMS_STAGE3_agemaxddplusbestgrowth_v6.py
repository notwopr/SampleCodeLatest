"""
Title: SCREENPARAMS - STAGE 3 - agemaxdd + bestgrowth
Date Started: Nov 17, 2020
Version: 6.00
Version Start Date: Nov 17, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
STAGE3_ageoldermaxdrop 1/2
    age_older
    allpctdrop_rawoldbareminraw_max
bestgrowth 1/2
    2018METHODv6

"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'STAGE3_ageoldermaxdrop',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_ageoldermaxdrop',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': '2018METHODv6',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_2018METHODv6',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_agemaxddplusbestgrowthv6')
