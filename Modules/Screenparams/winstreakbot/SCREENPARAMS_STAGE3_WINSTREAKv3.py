"""
Title: SCREEN PARAMS - STAGE 3 - WINSTREAK BOT
Date Started: Oct 4, 2020
Version: 3
Version Start Date: Oct 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Paramscript for using winstreakbot in Strattester.

"""
look_back = 180
periodlen = 30
avgtype = 'mean'
avgmarginweight = 0.5
num_mktbeatweight = 0.5
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'winstreak_LB{look_back}_PD{periodlen}_{avgtype}',
    'look_back': look_back,
    'periodlen': periodlen,
    'benchticker': '^IXIC',
    'avgmarginweight': avgmarginweight,
    'num_mktbeatweight': num_mktbeatweight,
    'avg_type': avgtype
    }
