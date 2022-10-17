"""
Title: AGE BOT MASTER
Date Started: Jan 4, 2021
Version: 1.00
Version Start: Jan 4, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Returns age statistics on stocks that meet specified growth rates for given time period.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import sys
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
sys.path.append("..")
from computersettings import computerobject
from agebot.AGEBOT_BASE import agebotmaster
exit()

staticdatesource = r'D:\BOT_DUMP\multitrials\D20201010T3\mktbeatpoolpctalltrialmasterdf_2018methodversions.csv'
#stocklistdf = pd.read_csv(staticdatesource)
statictrialexistdates = []#stocklistdf['existdate'].to_list()

global_params = {
    'rootdir': computerobject.bot_dump,
    'todaysdate': '2022-01-29',
    'testnumber': 1,
    'testregimename': 'agebot',
    'num_trials': 1,
    'testlen': 365,
    'rank_beg': None,
    'rank_end': None,
    'latestdate': '',
    'firstdate': '1990-01-01',
    'gr_u': None,
    'gr_l': None,
    'dir_u': None,
    'dir_l': '>',
    'chunksize': 1,
    'statictrialexistdates': statictrialexistdates
}

if __name__ == '__main__':
    agebotmaster(global_params)
    playsound('C:\Windows\Media\Ring03.wav')
