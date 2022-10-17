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
from Screenparams.losscontrol.SCREENPARAMS_STAGE3_LOSSCONTROLv41 import stage3_params
# SET STRAT PANEL FOR THE QUALITY PRONG RANKINGS
strat_panel = {
    #'Stage1': stage1_params,
    #'Stage 2 Part I': stage2part1_params,
    #'Stage 2 Part II': stage2part2_params,
    'Stage3': stage3_params
}

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
lookback = 365
reboundbot_params = {
    'scriptname': f'reboundbotv1_{lookback}',
    'crashlookbacklen': lookback,
    'scripttype': 'ranker',
    'crashbenchticker': '^IXIC',
    'verbose': '',
    'weight_loss': 1/2,
    'weight_quality': 1/2,
    'rankmeth': 'standard',
    'rankregime': '1isbest',
    'qualitystratpanel': strat_panel
    }
