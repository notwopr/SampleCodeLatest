"""
Title: OPTIMAL PARAM FINDER MASTER.
Date Started: July 9, 2020
Version: 1.02
Version Start: Aug 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given a date, testlen, return stats of the metric profile for the pool of stocks that beat the market for that period.
VERSIONS:
1.01: Clean up code use updated code for building folders.
1.02: Update code.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from ONETIME_MKTBEATPOOL_FILTER_firstpass import stage1_params
from OPTIMALPARAMFINDER_secondpassparams import secondpass_params
from OPTIMALPARAMFINDER_metricpanelparams_template import metricpanel_params_temp
from OPTIMALPARAMFINDER_BASE import getidealportfolio, getmetricrangesandaccuracy
from filelocations import buildfolders_regime_testrun
from computersettings import computerobject
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source
from timeperiodbot import getrandomexistdate


# SET DATE AND TEST NUMBER
todaysdate = '2020-08-10'
testnumber = 2

# SET TEST REGIME NAME
testregimename = 'optimalparamfinder'

# RESULT PCT BEAT MARKET PARAMS
testlen = 365
benchticker = '^IXIC'

# SET EXISTENCE DATE
exist_date = getrandomexistdate('', '1990-01-01', testlen, daterangedb_source)

# SET IDEAL PORTFOLIO PARAM FILTERS
firstpass_params = stage1_params
secondpass_params = secondpass_params

# SET BASE METRICPANEL
metricpanel_params_temp = metricpanel_params_temp

# TOGGLE STAGES
verbose = 'verbose'
getidealpool = 'yes'
getmetricranges = 'no'
getmpaccuracy = 'no'


if __name__ == '__main__':
    rootdump = computerobject.bot_dump
    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdump, testnumber, todaysdate, testregimename)
    # GET IDEAL PORTFOLIO
    mktbeaterpool = getidealportfolio(verbose, testrunparent, exist_date, testlen, benchticker, firstpass_params, secondpass_params)
    # GET IDEAL PORTFOLIO METRIC RANGES
    if getmetricranges == 'yes':
        newmetricpanel_params = getmetricrangesandaccuracy(testrunparent, metricpanel_params_temp, exist_date, testlen, firstpass_params, mktbeaterpool, todaysdate)
    # GET MP ACCURACY
    if getmpaccuracy == 'yes':
        getmpaccuracy(testrunparent, exist_date, newmetricpanel_params, mktbeaterpool)
