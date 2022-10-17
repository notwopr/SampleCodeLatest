"""
Title:  SCREEN PARAMS - STAGE 3 - REBOUND BOT
Date Started: Nov 19, 2020
Version: 1.00
Version Start Date: Nov 19, 2020
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
        'scriptnickname': 'losscontrolv41',
        'scriptfilename': 'Screenparams.losscontrol.SCREENPARAMS_STAGE3_LOSSCONTROLv41',
        'scriptweight': qualitymetricweight
    }
]
lossandquality_params = scriptjoiner(scriptlist, 'STAGE3_reboundbotv2')
lookback = 720
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'reboundbotv2_{lookback}',
    'scriptweight': 0.5,
    'scripttype': 'ranker',
    'crashlookbacklen': lookback,
    'crashbenchticker': '^IXIC',
    'lossandquality_params': lossandquality_params
    }
