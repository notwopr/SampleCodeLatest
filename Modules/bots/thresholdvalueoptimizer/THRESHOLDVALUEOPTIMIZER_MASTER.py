"""
Title: THRESHOLD VALUE OPTIMIZER.
Date Started: ?
Version: 1.1
Version Start: July 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Uses python minimizers to locate best combination of threshold values for given metricpanel profile, using mktbeatpoolpct on testperiod as the measure of success.

VERSIONS
1.1: Update code.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from THRESHOLDVALUEOPTIMIZER_BASE import find_best_param_settings
# PARAM IMPORTS
from ONETIME_MKTBEATPOOL_FILTER_firstpass import stage1_params
#from SCREENPARAMS_SUMMER2020TEMP_STAGE2part1_2018filter import stage2part1_params
from SCREENPARAMS_SUMMER2020TEMP_STAGE2part1 import stage2part1_params
from SCREENPARAMS_SUMMER2020TEMP_STAGE2part2 import stage2part2_params
from SCREENPARAMS_SUMMER2020TEMP_STAGE2part3 import stage2part3_params

# SET DATE AND TEST NUMBER
todaysdate = '2020-08-01'
testnumber = 3

# SET TEST REGIME NAME
testregimename = 'threshvaloptimizer'

# SET EXISTENCE DATE
exist_date = '2019-07-01'

# RESULT PCT BEAT MARKET PARAMS
testlen = 365
benchticker = '^IXIC'

# SET PRE-OPTIMIZER FILTERS
preoptfilter_dict = {
    'Stage 1': stage1_params,
    'Stage 2 Part I': stage2part1_params#,
    #'Stage 2 Part II': stage2part2_params
}


# SET OPTIMIZER PARAMS
optimizer_params = stage2part2_params
lbounds = np.array([0])
ubounds = np.array([-1])
initialguess = np.array([-0.5])
verbose = 'verbose'


if __name__ == '__main__':
    testregimeparent = computerobject.bot_dump
    find_best_param_settings(lbounds, ubounds, initialguess, exist_date, testnumber, todaysdate, testregimeparent, testregimename, preoptfilter_dict, optimizer_params, testlen, benchticker, verbose)
