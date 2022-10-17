"""
Title: SCREENPARAMS - STAGE 3 - rawtotruetostraight_magreg
Date Started: Oct 31, 2020
Version: 1.00
Version Start Date: Oct 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

Difference between raw graph and true line 1/4
    Magnitude of that difference
        unifatscore_rawtrue_mean 1/2
        unifatscore_rawtrue_median 1/2
Difference between true graph and straight line 1/4
    Magnitude of that difference
        unifatscore_truestraight_mean 1/2
        unifatscore_truestraight_median 1/2
Difference between raw graph and true line 1/4
    Regularity of that difference
        unifatscore_rawtrue_std 1/2
        unifatscore_rawtrue_mad 1/2
Difference between true graph and straight line 1/4
    Regularity of that difference
        unifatscore_truestraight_std 1/2
        unifatscore_truestraight_mad 1/2
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'rawtotruetostraight_mag',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtotruetostraight_mag',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'rawtotruetostraight_reg',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_rawtotruetostraight_reg',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_rawtotruetostraight_magreg')
