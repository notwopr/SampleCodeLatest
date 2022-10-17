"""
Title: MKTBEATERFINDER MASTER
Date Started: Nov 18, 2020
Version: 1.00
Version Start: Nov 18, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Finds a list of stocks that might be marketbeaters given a current date, a testperiod start and end date and a benchmark.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from MKTBEATERFINDER_BASE import mktbeaterfinder_master
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES
from filelocations import readpkl, buildfolders_regime_testrun


filterinstructdict = [
    {
        'targetcol': 'Overall Pullout Pct',
        'comparecol': 'bydaypulloutpct_losers_max',
        'filtermeth': 'above'
    },
    {
        'targetcol': 'Difference (%)',
        'comparecol': 'bydaymargins_losers_max',
        'filtermeth': 'above'
    },
    {
        'targetcol': 'Gain/Loss Rate (%)',
        'comparecol': 'bydaygains_losers_max',
        'filtermeth': 'above'
    }
]


global_params = {
    'todaysdate': '2020-11-20',
    'testnumber': 2,
    'testregimename': 'mktbeaterfinder',
    'metricsetname': 'nasdaqmktbeaters',
    'benchticker': '^IXIC',
    'testday': 13,
    'polibsource': computerobject.bot_important / 'PULLOUTBOT' / 'masterbydaystats.csv',
    'filterinstructdict': filterinstructdict
}
# set trial date
trialdate = '2019-11-18'

if __name__ == '__main__':
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(computerobject.bot_dump, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    mktbeaterfinder_master(testrunparent, global_params, trialdate)
    playsound('C:\Windows\Media\Ring03.wav')
