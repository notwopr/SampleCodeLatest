"""
Title:  SCREEN PARAMS - RECOVERY BOT
Date Started: Jan 12, 2021
Version: 10.00last_pma720
Version Start Date: Mar 6, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
The recoverybot finds a stock's most recent alltime high price and its current price and calculates the fall. The worse the fall the better.  Then it calculates the stock's quality metric pre-ATH.  if it is a stock that fell a lot but is pre-ATH great quality, then it is ideal.
Versions:
10: experiment with distance to last ATH date or DTLATH, which is the time between current date and last ATH date.
FILTERS:

"""
# QUALITY PRONG IMPORTS
from Modules.screenparam_joiners import scriptjoiner

currtoathcomboweight = 2/3
qualitymetricweight = 1/3
ath_occur = 'first'
min_preath_age = 3
scriptlist = [
    {
        'scriptnickname': f'currtoathcombo_descending_{ath_occur}_mpa{min_preath_age}',
        'scriptfilename': (f'Modules.Screenparams.recoverybot.SCREENPARAMS_currtoathcombo_descending_{ath_occur}_mpa{min_preath_age}', 'stage3_params'),
        'scriptweight': currtoathcomboweight
    },
    {
        'scriptnickname': 'groplusvolv15h',
        'scriptfilename': ('Modules.Screenparams.groplusvol.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv15h', 'stage3_params'),
        'scriptweight': qualitymetricweight
    }
]

recoverybot_params = scriptjoiner(scriptlist, f'recoverybotv10d_{ath_occur}_mpa{min_preath_age}')
