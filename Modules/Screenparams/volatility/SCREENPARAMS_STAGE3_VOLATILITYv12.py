"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 7, 2021
Version: 12.00
Version Start Date: Feb 25, 2021
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
        'scriptnickname': 'age_younger',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_age_youngerbetter',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'volatilityv6',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_VOLATILITYv6',
        'scriptweight': 0.5
    }
]

stage3_params = scriptjoiner(scriptlist, 'VOLATILITYv12')
