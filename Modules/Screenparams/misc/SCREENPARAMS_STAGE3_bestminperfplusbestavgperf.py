"""
Title: SCREENPARAMS - STAGE 3 - combining best minperf plus best avgperf (best as of 12.31.20 according to BACKTEST LEADERBOARD)
Date Started: Dec 31, 2020
Version: 1.00
Version Start Date: Dec 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
Best Minperf Strat = agemaxddplusbestgrowthv10 - 1/2 weight
    STAGE3_ageoldermaxdrop 1/3
        age_older
        allpctdrop_rawoldbareminraw_max
    rawtostraight  1/3
        Difference between raw graph and straight line
        Magnitude of that difference
            unifatscore_rawstraight_mean 1/2
            unifatscore_rawstraight_median 1/2
    rawoldbareminraw 1/3
        Difference between raw graph and oldbareminraw line
            Magnitude of that difference
                unifatscore_rawoldbareminraw_mean 1/2
                unifatscore_rawoldbareminraw_median 1/2
Best avgperf Strat = STAGE3_mktbeatoverminv11 - 1/2 weight
    Loss Control
        Consecutive Negative Losses 1/2
            Max Length 1
                Absolute Length 1
                    statseglen_negseg_max
        Age 1/2
            Age_younger
"""
from genericfunctionbot import scriptjoiner

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
scriptlist = [
    {
        'scriptnickname': 'STAGE3_mktbeatoverminv11',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_MKTBEATOVERMINv11',
        'scriptweight': 1/2
    },
    {
        'scriptnickname': 'STAGE3_agemaxddplusbestgrowthv10',
        'scriptfilename': 'Screenparams.SCREENPARAMS_STAGE3_agemaxddplusbestgrowth_v10',
        'scriptweight': 1/2
    }
]
stage3_params = scriptjoiner(scriptlist, 'STAGE3_bestavgperfplusminperf_123120')
