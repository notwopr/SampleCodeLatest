"""
Title: MAXDD MASTER
Date Started: Nov 10, 2020
Version: 1.00
Version Start: Nov 10, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Run trials on whether subsequent period changes the historical maxdd of a group of stocks.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from MAXDD_BASE import prop_maxddadjusted_multitrial


# if static trial dates...
staticdatesource = r'D:\BOT_DUMP\multitrials\D20201010T3\mktbeatpoolpctalltrialmasterdf_2018methodversions.csv'
stocklistdf = pd.read_csv(staticdatesource)
statictrialexistdates = stocklistdf['existdate'].to_list()

global_params = {
    'todaysdate': '2020-11-10',
    'testnumber': 4,
    'testregimename': 'multitrials',
    'metricsetname': 'maxddchangepct',
    'num_trials': 1000,
    'testlen': 365,
    'benchticker': '^IXIC',
    'latestdate': '',
    'firstdate': '1990-01-01',
    'statictrialexistdates': statictrialexistdates,
    'basepool': 'no',
    'subtrialfolderpath': r'\Stage 1_dump\resultfiles',
    'testrunparentpath': r'D:\BOT_DUMP\multitrials\D20201010T3',
    'basepoolfntemplate': 'SCREENER_firstpass_finalists_as_of_'
}


if __name__ == '__main__':
    # run multitrials
    prop_maxddadjusted_multitrial(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
