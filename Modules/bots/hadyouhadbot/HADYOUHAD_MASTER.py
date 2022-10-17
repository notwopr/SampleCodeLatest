"""
Title: Quick Reference - HAD YOU HAD
Date Started: Feb 26, 2019
Version: 1.4
Version Start: Sept 24, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Quickly pull up print out of various functions.
VERSIONS:
1.2:  Add growthrates by X period.  use geometric formula.
1.3: Update code.
1.4: Streamline code.
Quick Graph.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from HADYOUHAD_BASE import hadyouhadinvested
from filelocations import buildfolders_regime_testrun, readpkl
from computersettings import computerobject
from HADYOUHAD_METRICPANEL import hadyouhad_params

# SET DATE AND TEST NUMBER
todaysdate = '2021-08-15'
testnumber = 1

# SET TEST REGIME NAME
testregimename = 'hadyouhadinvested'

# LOAD PORTFOLIOS TO TEST
portlib = readpkl('portfoliolibrary', computerobject.bot_important / 'stocklists')

# SET TIME PERIOD TO TEST
beg_date = '2021-01-22'
end_date = '2021-08-12'

# SET STARTING CAPITAL
startcapital = 100000
metricpanel_params = ''

# averaging method for port growth
avgmeth = 'mean'
remove_outliers = 'no'
strength = 1.5

# REPORT PARAMS
verbose = 'no'
plot = 'no'

# METRIC PARAMSCRIPT FOR METRICS COMPARISON
metricpanelscript = hadyouhad_params

if __name__ == '__main__':
    testregimeparent = computerobject.bot_dump
    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(testregimeparent, testnumber, todaysdate, testregimename)
    hadyouhadinvested(startcapital, beg_date, end_date, portlib, testrunparent, avgmeth, remove_outliers, verbose, plot, strength, metricpanelscript)
    playsound('C:\Windows\Media\Ring03.wav')
