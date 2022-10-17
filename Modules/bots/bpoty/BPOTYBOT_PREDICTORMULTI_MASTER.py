"""
Title: Best Part of the Year Predictor Bot Multi Accuracy Collation
Date Started: Dec 14, 2020
Version: 1.0
Version Start: Dec 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Takes a set of lookbackchunks and runs accuracy tests on each and returns dataframe with all accuracy test results.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import numpy as np
#   LOCAL APPLICATION IMPORTS
from BPOTYBOT_PREDICTORMULTI_BASE import lookbackpredictions_multi
from computersettings import computerobject


# PULLSOURCE OF BPOTY CHART
bpotysource = r'D:\BOT_DUMP\bpotybotpredictbot\D20201227T19\best12day_^IXIC_1971_to_2020.csv'

potylen = 360
global_params = {
    'todaysdate': '2021-01-22',
    'testnumber': 6,
    'testregimename': 'bpotybotpredictbot',
    'potydef': 'year',#f'{potylen}day',
    'potylen': potylen,
    'ticker': '^IXIC',
    'beg_date': "",
    'end_date': "",
    'signaltrigger': 0.8,
    'bpotysource': "",
    'verbose': '',
    'chunksize': 100
}

# SET SERIES OF LOOKBACK STRENGTHS TO TEST FOR
lbvalues = np.arange(1, 10, 1)


# EXECUTE
if __name__ == '__main__':
    lookbackpredictions_multi(computerobject.bot_dump, global_params, lbvalues)
    playsound('C:\Windows\Media\Ring03.wav')
