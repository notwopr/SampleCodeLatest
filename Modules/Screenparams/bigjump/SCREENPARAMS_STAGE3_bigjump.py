"""
Title: SCREENPARAMS - STAGE 3 - bigjump
Date Started: Oct 11, 2020
Version: 1.00
Version Start Date: Oct 24, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:
True graph == oldbareminraw graph.  See Investment Research Journal for reasoning.
    bigjump_mag_oldbareminraw 1



"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_bigjump',
    'scriptparams': [
        {
            'metricname': 'bigjump_mag_oldbareminraw',
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 1,
            'bigjumpstrength': 2,
            'calibration': 'oldbareminraw',
            'look_back': 0
        }
        ]
    }
