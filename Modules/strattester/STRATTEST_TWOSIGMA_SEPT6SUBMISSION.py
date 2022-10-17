"""
Title: TWO SIGMA SEPT 6, 2021 SUBMISSION
Date Started: Sept 6, 2021
Version: 1
Version Start: Sept 6, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  I created this script to produce the CSV file with the hypothetical trades my chosen strategy I wished to submit to 2 Sigma for consideration would recommend
It runs STRATTEST_SINGLE_MASTER looped for every holding period of 6 months for the past 15 years as required, with a 90 day buffer period.

Here are the details:
End Date: 2021-08-03  (your documents seem to require a 90 day buffer period, so since I ran these tests on 2021-11-02, 90 days prior would be 2021-08-03)
Start Date:  2006-10-21  (this is the date 15 years (5,400 days) prior to 2021-08-03, assuming a holding period of 6 months =180 days (180 * 2 * 15 = 5,400 days))
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from timeperiodbot import timeperiodbot
from tickerportalbot import tickerportal4
from filelocations import create_nonexistent_folder
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source
from STRATTEST_SINGLE_BASE import getstratpool
# PARAMS
from Screenparams.STAGE1.SCREENPARAMS_STAGE1v5 import stage1_params
from Screenparams.STAGE2.SCREENPARAMS_STAGE2v8 import stage2_params
from Screenparams.groplusvol.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv15g import stage3_params

# SET FILTERS
strat_panel = {
    'multistageweightmode': 'no',
    'Stage 1': stage1_params,
    'Stage 2': stage2_params,
    'Stage 3': stage3_params
}

# SET DATE AND TEST NUMBER AND REGIME
todaysdate = '2021-11-26'
setnumber = 5
testregimename = 'TWO SIGMA NOV SUBMISSION'
savemode = 'csv'
# SET INVESTMENT PERIOD, START AND END DATE
investperiod = '365D'
startdate = '2006-08-07'
enddate = '2021-08-03'

# SET MINIMUM AGE PRE-TEST PERIOD
minimumage = 3
# SET RANKING METRICS
rankmeth = 'standard'
rankregime = '1isbest'
# SET MULTIPROCESSOR CHUNKSIZE
chunksize = 5
verbose = ''


def getoneholdingperiod(testregimeparent, mod_date, exist_date, testnumber):
    # BUILD FOLDERS
    testcode = 'D' + mod_date + 'T' + str(testnumber)
    testrunparent = testregimeparent / testcode
    create_nonexistent_folder(testrunparent)
    # SET START POOL
    startpool = tickerportal4(exist_date, exist_date, 'common', minimumage)
    # GET FINAL STRAT POOL
    getstratpool(verbose, testrunparent, exist_date, strat_panel, startpool, rankmeth, rankregime, savemode, chunksize, computerobject.use_cores)


if __name__ == '__main__':
    # CREATE PARENT FOLDER FOR TWO SIGMA TESTS IF NOT ALREADY THERE
    testregimeparent = computerobject.bot_dump / testregimename
    create_nonexistent_folder(testregimeparent)
    # create parent for testrun
    mod_date = todaysdate.replace("-", "")
    setrunparent = testregimeparent / f'testset{mod_date}_{setnumber}'
    create_nonexistent_folder(setrunparent)
    # object storing all holding period summaries
    allperiodsummaries = []
    # get invest dates
    allinvestdates = timeperiodbot(investperiod, startdate, enddate, 'all', '')
    # number of investment periods
    numperiods = len(allinvestdates)-1
    # for each investdate, get full stock rankings
    for testind in range(numperiods):
        # set dates
        enterdate = allinvestdates[testind]
        exitdate = allinvestdates[testind+1]
        # get full stock ranking
        getoneholdingperiod(setrunparent, mod_date, allinvestdates[testind], testind)
    playsound('C:/Windows/Media/Ring03.wav')
