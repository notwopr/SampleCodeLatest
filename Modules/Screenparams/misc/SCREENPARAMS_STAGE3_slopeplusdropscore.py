"""
Title: SCREENPARAMS - STAGE 3 - slope plus dropscore
Date Started: Jan 16, 2021
Version: 1.00
Version Start Date: Jan 16, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'slopescore',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_slopescore',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'dropscore',
        'scriptfilename': 'Screenparams.SCREENPARAMS_dropscore',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_slopeplusdropscore_straight')
