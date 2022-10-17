"""
Title:  SCREEN PARAMS - STAGE 3 - REBOUND BOT
Date Started: Nov 19, 2020
Version: 3.00
Version Start Date: Jan 11, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

FILTERS:

"""
# QUALITY PRONG IMPORTS
from genericfunctionbot import scriptjoiner

crasheventlossweight = 1/2
qualitymetricweight = 1/2

scriptlist = [
    {
        'scriptnickname': 'crasheventloss',
        'scriptfilename': 'Screenparams.SCREENPARAMS_reboundbot_losscomponent',
        'scriptweight': crasheventlossweight
    },
    {
        'scriptnickname': 'volatilityv6',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_VOLATILITYv6',
        'scriptweight': qualitymetricweight
    }
]
lossandquality_params = scriptjoiner(scriptlist, 'STAGE3_reboundbotv3')
lookback = 360*4
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
reboundbot_params = {
    'scriptname': f'reboundbotv3_{lookback}',
    'scripttype': 'ranker',
    'crashlookbacklen': lookback,
    'crashbenchticker': '^IXIC',
    'lossandquality_params': lossandquality_params
    }
