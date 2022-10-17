"""
Title: OPTIMAL PARAM FINDER MASTER - APPLY METRICPANEL
Date Started: July 22, 2020
Version: 1.00
Version Start: July 22, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given metricpanel complete with thresholds, run over given selection period and return mktbeatpool_pct.
VERSIONS:
1.01: Clean up code use updated code for building folders.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
import datetime as dt
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_regime_testrun, buildfolders_parent_cresult_cdump, readpkl
from tickerportalbot import tickerportal2
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source
from computersettings import computerobject
from ONETIME_GETSINGLEPASSPOOL import getsinglepasspool
from TESTPERIOD_PERFORMANCE_FUNCBASE import mktbeatpoolpct


# SET DATE AND TEST NUMBER
todaysdate = '2020-07-23'
testnumber = 3

# SET TEST REGIME NAME
if computerobject.computername == 'amdcomp':
    testregimeparent = computerobject.bot_dump2
elif computerobject.computername == 'intelcomp':
    testregimeparent = computerobject.bot_dump
testregimename = 'optimalparamfinder_applymp'

# SET EXISTENCE DATE
exist_date = '2012-01-17'

# RESULT PCT BEAT MARKET PARAMS
testlen = 365
benchticker = '^IXIC'
verbose = 'verbose'

# SET METRICPANEL
metricpanelfileloc = Path(r'C:\Users\david\Google Drive\Goals\Careers\Business\Good Business Ideas\Fund Business\Investment Strategy Research\IMPORTANTBOTOUTPUTS\METRICPANELS')
metricpanelfilename = 'ED20180601_D20200722T1_doublebound'
metricpanelparams = readpkl(metricpanelfilename, metricpanelfileloc)


if __name__ == '__main__':

    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(testregimeparent, testnumber, todaysdate, testregimename)

    # GET FULL EXTANT POOL
    fullpool = tickerportal2(exist_date, 'common')

    # GET MP ACCURACY
    # build mp check folders
    mpcheckparent, mpcheckresults, mpcheckdump = buildfolders_parent_cresult_cdump(testrunparent, 'mpcheckdump')
    # get mpcheckpool from firstpasspool
    mpcheckpool = getsinglepasspool(metricpanelparams, mpcheckresults, mpcheckdump, '', exist_date, fullpool)
    # get percentage of resulting pool that beats market
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    mktbeatpoolpct(verbose, mpcheckpool, benchticker, test_beg, test_end)
