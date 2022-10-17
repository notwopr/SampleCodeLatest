"""
Title: DROP STOCK BOT MASTER
Date Started: Dec 8, 2020
Version: 1.00
Version Start: Dec 8, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Tells you whether to drop a stock based on the current day of the investing period you are in. Uses findings from pulloutbot data.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from DROPSTOCKBOT_BASE import dropbot_multitrialcruncher
from filelocations import readpkl

fndatepoolset = 'D20201209T4_trialrunset'
datepoolsetdir = r'D:\BOT_DUMP\dropbot\D20201209T4'
trialrunset = []#readpkl('D20201209T4_trialrunset', Path(datepoolsetdir))

global_params = {
    'todaysdate': '2021-04-15',
    'testnumber': 1,
    'testregimename': 'dropbot',
    'candidate_profile': {
        #'growth_curr': -0.037456,
        #'growth_err': 0.03,
        #'margin_curr': -0.095825,
        #'margin_err': 0.03,
        #'beatpct_curr': 1,
        #'beatpct_err': 0.03,
        },
    'ideal_profile': {
        'mktbeater': 'yes',
        #'min_gain': 0.80,
        #'min_margin': 0.30
        },
    'trialtype': 'full',
    'benchgain_currfilter': 'no',
    'benchgain_curr': '',
    'benchgain_err': 0.05,
    'num_trials': 1,
    'daysinvested': 39,
    'investperiod': 365,
    'benchticker': '^IXIC',
    'latestdate': '',
    'firstdate': '2020-02-25',
    'existingset': trialrunset,
    'chunksize': 100
}

if __name__ == '__main__':
    dropbot_multitrialcruncher(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
