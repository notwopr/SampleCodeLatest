"""
Title: SCREEN PARAMS - STAGE 2 FILTERS (WINNERTHRESHOLD FINDER PARAMSCRIPT)
Date Started: Jan 30, 2021
Version: 2.00d
Version Start Date: Mar 10, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:

"""
from genericfunctionbot import scriptjoiner_removedupes_noimportlib
from Screenparams.SCREENPARAMS_STAGE2v2 import stage2_params as v2
from Screenparams.SCREENPARAMS_STAGE2v2c import stage2_params as v2c

scriptlist = [v2, v2c]
stage2_params = scriptjoiner_removedupes_noimportlib(scriptlist, 'STAGE2FILTERSv2d')
