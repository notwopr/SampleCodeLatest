"""
Title: SCREENPARAMS - STAGE 3 - truetostraight_magreg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between true graph and straight line
    Magnitude of that difference 1/2
        unifatscore_truestraight_mean 1/2
        unifatscore_truestraight_median 1/2
    Regularity of that difference 1/2
        unifatscore_truestraight_std 1/2
        unifatscore_truestraight_mad 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'truetostraight_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_truetostraight_mag',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'truetostraight_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_truetostraight_reg',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_truetostraight_magreg')
