"""
Title:  SCREEN PARAMS - STAGE 2 FILTERS
Date Started: Jan 21, 2021
Version: 2.00b
Version Start Date: Feb 18, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
2b: v2 + v2a
FILTERS:

"""
from genericfunctionbot import scriptjoiner_removedupes_noimportlib
from Screenparams.SCREENPARAMS_STAGE2v2 import stage2_params as v2
from Screenparams.SCREENPARAMS_STAGE2v2a import stage2_params as v2a

scriptlist = [v2, v2a]
stage2_params = scriptjoiner_removedupes_noimportlib(scriptlist, 'STAGE2FILTERSv2b')
