"""
Title: SCREENPARAMS - GROWTH plus VOLATILITY
Date Started: Jan 18, 2021
Version: 5.00
Version Start Date: Feb 10, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
simple slopescore + VOLATILITY V10


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
        'scriptnickname': 'volatilityv10',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_VOLATILITYv10',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_groplusvolv5')
