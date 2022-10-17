"""
Title:  SCREEN PARAMS - RECOVERY BOT
Date Started: Jan 12, 2021
Version: 9.00first
Version Start Date: Nov 1, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
The recoverybot finds a stock's most recent alltime high price and its current price and calculates the fall. The worse the fall the better.  Then it calculates the stock's quality metric pre-ATH.  if it is a stock that fell a lot but is pre-ATH great quality, then it is ideal.
Versions:

FILTERS:

"""
# QUALITY PRONG IMPORTS
from Modules.screenparam_joiners import scriptjoiner

currtoathdiffweight = 1/2
qualitymetricweight = 1/2
ath_occur = 'first'
min_preath_age = 360
scriptlist = [
    {
        'scriptnickname': f'currtoathdiff_{ath_occur}_mpa{min_preath_age}',
        'scriptfilename': (f'Modules.Screenparams.recoverybot.SCREENPARAMS_currtoathdiff_{ath_occur}_mpa{min_preath_age}', 'stage3_params'),
        'scriptweight': currtoathdiffweight
    },
    {
        'scriptnickname': 'groplusvolv15h',
        'scriptfilename': ('Modules.Screenparams.groplusvol.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv15h', 'stage3_params'),
        'scriptweight': qualitymetricweight
    }
]

recoverybot_params = scriptjoiner(scriptlist, f'recoverybotv9_{ath_occur}_mpa{min_preath_age}')
