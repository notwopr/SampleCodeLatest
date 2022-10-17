"""
Title: SCREENPARAMS - STAGE 3 - slopeoverloss
Date Started: Nov 14, 2020
Version: 7.00
Version Start Date: Nov 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:
avg 1/2
    slopeoverloss_ratio_avg
slopeoverloss_ratio_max 1/2

"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'slopeoverlossv5',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_slopeoverlossv5',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'slopeoverlossv3',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_slopeoverlossv3',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_slopeoverlossv7')
