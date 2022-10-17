"""
Title: EXITSTRAT MASTER
Date Started: Dec 1, 2020
Version: 1.00
Version Start: Dec 1, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Trying to figure out whether it is good to take out small profits along the way or keep 100% exposed until end of term?
Conclusion: It seems like for a stock that has a consistent upwards trajectory, the hold strategy is better. You'd gain more by the extra amount of capital exposed.  But if the stock plummets, you'd be better off by limiting your exposure  by keeping a constant exposure amount.
Example:
'stock': 'SHOP',
'beg_date': '2019-05-10',
'end_date': '2020-05-10',
HOLD networth change (173.91337943824138) %
STRAT networth change (110.6624843190174) %
HOLD after tax networth change (86.95668971912069) %
STRAT after tax networth change (55.3312421595087) %
diff_networth (STRAT minus HOLD): (-23.091568308544417 %)
diff_atnetworth (STRAT minus HOLD): (-16.915921867853626 %)
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from EXITSTRAT_BASE import exitstrat_multitrial
from EXITSTRAT_PARAMS_filter import stage2_params
from EXITSTRAT_PARAMS_ranker import stage3_params


global_params = {
    'todaysdate': '2020-12-05',
    'testnumber': 12,
    'testregimename': 'exitstrat',
    'num_trials': 1000,
    'testlen': 365,
    'latestdate': '',
    'firstdate': '1990-01-01',
    'taxrate': 0.5,
    'cap_start': 1000,
    'selltrigger': 0.10,
    'rankmeth': 'standard',
    'rankregime': '1isbest',
    'verbose': 'verbose',
    'filterpanel': {
        #'Stage 1': stage1_params,
        'Stage 2': stage2_params,
        'Stage 3': stage3_params
    }
}


if __name__ == '__main__':
    # run multitrials
    exitstrat_multitrial(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
