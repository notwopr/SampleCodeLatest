"""
Title: Best Part of the Year Predictor Bot
Date Started: Dec 13, 2020
Version: 1.0
Version Start: Dec 13, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Takes an existing BPOTY chart, and given predictor strat, returns prediction accuracy results.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from BPOTYBOT_PREDICTOR_BASE import lookbackpredictions
from computersettings import computerobject


# PULLSOURCE OF BPOTY CHART
bpotysource = r'D:\BOT_DUMP\bpotybot\D20201227T1\besthalf_^IXIC_1971_to_2020.csv'

global_params = {
    'todaysdate': '2020-12-27',
    'testnumber': 23,
    'testregimename': 'bpotybotpredictbot',
    'lookbackchunks': 1,
    'potydef': '15day',
    'potylen': 15,
    'signaltrigger': 0.45,
    'beg_date': '',
    'end_date': '',
    'ticker': '^IXIC',
    'verbose': '',
    'bpotysource': bpotysource
}


if __name__ == '__main__':
    lookbackpredictions(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
