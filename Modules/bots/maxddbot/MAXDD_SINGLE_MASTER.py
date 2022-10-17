"""
Title: MAXDD SINGLE STOCK MASTER
Date Started: Nov 11, 2020
Version: 1.00
Version Start: Nov 11, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Run trials on whether testperiod period changes the historical maxdd of a stock.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from MAXDD_SINGLE_BASE import prop_maxddadjusted_multitrial_singlestock


# if static trial dates...
staticdatesource = r'D:\BOT_DUMP\multitrials\D20201010T3\mktbeatpoolpctalltrialmasterdf_2018methodversions.csv'
#stocklistdf = pd.read_csv(staticdatesource)
statictrialexistdates = []#stocklistdf['existdate'].to_list()

global_params = {
    'todaysdate': '2020-12-17',
    'testnumber': 2,
    'testregimename': 'multitrials',
    'metricsetname': 'maxddchangepct',
    'num_trials': 200,
    'testlen': 365,
    'stock': 'ADBE',
    'benchticker': '^IXIC',
    'corrmethod': 'pearson',
    'statictrialexistdates': statictrialexistdates
}


if __name__ == '__main__':
    # run multitrials
    prop_maxddadjusted_multitrial_singlestock(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
