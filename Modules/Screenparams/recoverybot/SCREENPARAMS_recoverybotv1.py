"""
Title:  SCREEN PARAMS - RECOVERY BOT
Date Started: Jan 12, 2021
Version: 1.00
Version Start Date: Jan 12, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
The recoverybot finds a stock's most recent alltime high price and its current price and calculates the fall. The worse the fall the better.  Then it calculates the stock's quality metric pre-ATH.  if it is a stock that fell a lot but is pre-ATH great quality, then it is ideal.
Versions:

FILTERS:

"""
# QUALITY PRONG IMPORTS
from genericfunctionbot import scriptjoiner

currtoathdiffweight = 1/2
qualitymetricweight = 1/2

scriptlist = [
    {
        'scriptnickname': 'currtoathdiff',
        'scriptfilename': 'Screenparams.SCREENPARAMS_currtoathdiff',
        'scriptweight': currtoathdiffweight
    },
    {
        'scriptnickname': 'volatilityv6',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_VOLATILITYv6',
        'scriptweight': qualitymetricweight
    }
]

recoverybot_params = scriptjoiner(scriptlist, 'recoverybotv1')
