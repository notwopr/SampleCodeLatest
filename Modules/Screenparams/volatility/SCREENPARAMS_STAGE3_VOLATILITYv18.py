"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 7, 2021
Version: 18.00
Version Start Date: Feb 26, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Versions:

FILTERS:

"""
# QUALITY PRONG IMPORTS
from genericfunctionbot import scriptjoiner

scriptlist = [
    {
        'scriptnickname': 'age_older',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_age_olderbetter',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'smoothness_rankstagev9i',
        'scriptfilename': 'Screenparams.Smoothness.SCREENPARAMS_smoothness_rankstagev9i',
        'scriptweight': 0.5
    }
]

stage3_params = scriptjoiner(scriptlist, 'VOLATILITYv18')
