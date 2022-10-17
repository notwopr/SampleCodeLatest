"""
Title: TWO SIGMA - FILE JOINE
Date Started: Sept 7, 2021
Version: 1
Version Start: Nov 2, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Use this to extract all the final stage 3 files from each investment period trial, and put in one folder for easier debugging.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import shutil
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from timeperiodbot import timeperiodbot
from filelocations import create_nonexistent_folder


# SET DATE AND TEST NUMBER OF THE FOLDER FROM WHICH YOU'LL EXTRACT FILES
todaysdate = '2021-11-02'
setnumber = 2
testregimename = 'TWO SIGMA NOV SUBMISSION'
# SET INVESTMENT PERIOD, START AND END DATE
investperiod = '180D'
startdate = '2006-10-21'
enddate = '2021-08-03'
# WHAT IS THE PREFIX FOR THE SOURCEFILE?
sourcefileprefix = 'Stage 3_recoverybotv9_finalists_as_of_'
# SET FOLDER LOCATION WITH FILES TO BE COLLATED
#resultfileloc = computerobject.bot_dump / testregimename / f'testset{mod_date}_{setnumber}'


if __name__ == '__main__':
    # CREATE PARENT FOLDER FOR TWO SIGMA TESTS IF NOT ALREADY THERE
    testregimeparent = computerobject.bot_dump / testregimename
    create_nonexistent_folder(testregimeparent)
    # set target testrun parent folder
    mod_date = todaysdate.replace("-", "")
    setrunparent = testregimeparent / f'testset{mod_date}_{setnumber}'
    # create destination folder
    destfolderparent = testregimeparent / 'consolidatedresultfiles'
    testrunparent_dest = destfolderparent / f'testset{mod_date}_{setnumber}'
    create_nonexistent_folder(destfolderparent)
    create_nonexistent_folder(testrunparent_dest)
    # object storing all holding period summaries
    allperiodsummaries = []
    # get invest dates
    allinvestdates = timeperiodbot(investperiod, startdate, enddate, 'all', '')
    # number of investment periods
    numperiods = len(allinvestdates)-1
    # for each investdate, open folder, get file, copy file, paste file
    for testind in range(numperiods):
        # set investperiod ranking file location
        resultfileloc = setrunparent / f'D{mod_date}T{testind}' / 'Stage 3_parent'
        # set filename
        resultfilename = f'{sourcefileprefix}{allinvestdates[testind]}'
        # MAKE ARCHIVE
        shutil.copy2(
            resultfileloc / f"{resultfilename}.csv",
            testrunparent_dest / f"{resultfilename}.csv")
        # REPORT
        print(f'Copied {resultfilename} from {resultfileloc} to {testrunparent_dest}.')
