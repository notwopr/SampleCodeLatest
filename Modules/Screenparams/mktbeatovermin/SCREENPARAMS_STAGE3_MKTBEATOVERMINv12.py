"""
Title: SCREENPARAMS - STAGE 3 - mktbeatperf to minperf
Date Started: Nov 13, 2020
Version: 12.00
Version Start Date: Nov 13, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:

Loss Control
    Consecutive Negative Losses 1/2
        Average Length 1/2
            Absolute Length
                statseglen_negseg_mean 1/2
                statseglen_negseg_median 1/2
        Max Length 1/2
            Absolute Length 1
                statseglen_negseg_max
    Age 1/2
        Age_younger

"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'age_youngerbetter',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_age_youngerbetter',
        'scriptweight': 0.5
    },
    {
        'scriptnickname': 'losscontrolv26',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_LOSSCONTROLv26',
        'scriptweight': 0.5
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_mktbeatoverminv12')
