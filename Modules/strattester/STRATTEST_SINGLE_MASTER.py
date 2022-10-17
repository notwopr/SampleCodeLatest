"""
Title: STRAT TEST SINGLE TRIAL MASTER
Date Started: July 10, 2020
Version: 2
Version Start: Oct 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given an existence date, runs pool thru first pass screening, runs again through given screening method, and returns percentage of resulting pool that beat market during the test period.
VERSIONS:
1.01: Optimize with updated functions.  Allow for more modulatory.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from timeperiodbot import getrandomexistdate
from tickerportalbot import tickerportal4, tickerportal5, tickerportal6
from filelocations import readpkl, buildfolders_regime_testrun, readcsv
import pandas as pd
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source
from UPDATEPRICEDATA_MASTERSCRIPT import tickerlistcommon_source, daterangedb_source_fundies
from STRATTEST_SINGLE_BASE import getstratpool, getperfstats
# PARAMS
from Screenparams.STAGE1.SCREENPARAMS_STAGE1v5 import stage1_params
#from Screenparams.STAGE2.SCREENPARAMS_STAGE2v8 import stage2_params

#from Screenparams.seasonalstrats.fall2020.SCREENPARAMS_STAGE2_PART1_FALL2020v1 import stage2part1_params
#from Screenparams.seasonalstrats.fall2020.SCREENPARAMS_STAGE2_PART2_FALL2020v1B import stage2part2_params
#from Screenparams.groplusvol.SCREENPARAMS_STAGE3_GROWTHPLUSVOLATILITYv15g import stage3_params
#from Screenparams.volatility.SCREENPARAMS_STAGE3_VOLATILITYv24 import stage3_params
from Screenparams.agemaxddplusbestgrowth.SCREENPARAMS_STAGE3_agemaxddplusbestgrowth_v2 import stage3_params as stage3A_params
from Screenparams.volatility.SCREENPARAMS_STAGE3_VOLATILITYv13 import stage3_params as stage3B_params
# SET SCRIPT WEIGHTS IF USING MULTISTAGEWEIGHTMODE

stage3A_params.update(
    {'scriptweight': (1/2)}
)
stage3B_params.update(
    {'scriptweight': (1/2)}
)
'''
stage3C_params.update(
    {'scriptweight': (1/4)*(1/2)}
)
stage3D_params.update(
    {'scriptweight': 1/2}
)

stage3E_params.update(
    {'scriptweight': (1/2)*(1/3)}
)
stage3F_params = stage3B_params
stage3F_params.update(
    {'scriptweight': (1/2)*(1/3)}
)

'''
# SET FILTERS
strat_panel = {
    'multistageweightmode': 'yes',
    'Stage 1': stage1_params,
    #'Stage 2 Part I': stage2_params,
    #'Stage 2 Part II': stage2part2_params,
    #'Stage 2 Part III': stage2c_params,
    #'Stage 3': stage3_params,
    'Stage 3A': stage3A_params,
    'Stage 3B': stage3B_params,
    #'Stage 3C': stage3C_params,
    #'Stage 3D': stage3D_params,
    #'Stage 3E': stage3E_params,
    #'Stage 3F': stage3F_params
}


# SET DATE AND TEST NUMBER AND REGIME
todaysdate = '2021-11-26'
testnumber = 1
testregimename = 'strattest_singles'
savemode = 'csv'
# SET MINIMUM AGE PRE-TEST PERIOD
minimumage = 3
fundyagemin = 360
lastfundyreportage = 30*6  # the max allowed time has passed since most recent fundy report published
# SET EXISTENCE DATE
exist_date = '2021-01-01'# getrandomexistdate('2017-01-01', '2000-01-01', testlen, daterangedb_source)

# MUST THE TICKERS HAVE FUNDAMENTALS AVAILABLE?
fundycompatpools = 'no'
# DO YOU WANT TO USE AN EXISTING STARTING POOL?
basepool = 'no'
#basepooldir = Path(r'C:\Users\david\Documents\PROJECTBELUGA\BOT_DUMP\strattest_singles')
#basepoolfn = 'Stage 1_STAGE1v5_finalists_as_of_2021-03-09'
#resultfileloc = Path(r'C:\Users\david\Documents\PROJECTBELUGA\BOT_DUMP\strattest_singles\D20211118T1\Stage 1_parent')
#resultfilename = 'Stage 1_STAGE1v5_finalists_as_of_2021-01-01'
#resultdf = readcsv(resultfilename, resultfileloc)
#custompool = resultdf['stock'].tolist()


# SET RANKING METRICS
rankmeth = 'standard'
rankregime = '1isbest'
# SET MULTIPROCESSOR CHUNKSIZE
chunksize = 5

# PERFORMANCE SETTINGS
calcperfstats = 'no'
testlen = 365
benchticker = '^IXIC'
verbose = ''


if __name__ == '__main__':
    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(computerobject.bot_dump, testnumber, todaysdate, testregimename)
    # SET START POOL
    if basepool == 'yes':
        basepooldf = readpkl(basepoolfn, basepooldir)
        startpool = basepooldf['stock'].tolist()
    elif basepool == 'custom':
        startpool = custompool
    else:
        if fundycompatpools == 'yes':
            startpool = tickerportal6(daterangedb_source_fundies, exist_date, exist_date, 'common', minimumage, fundyagemin, lastfundyreportage)
        else:
            startpool = tickerportal4(exist_date, exist_date, 'common', minimumage)
    # GET FINAL STRAT POOL
    finalstratpool = getstratpool(verbose, testrunparent, exist_date, strat_panel, startpool, rankmeth, rankregime, savemode, chunksize, computerobject.use_cores)
    # GET TEST PERIOD PERFORMANCE STATS OF FINAL STRAT POOL
    if calcperfstats == 'yes':
        if len(finalstratpool) != 0:
            getperfstats(verbose, exist_date, testlen, finalstratpool, benchticker)
    playsound('C:/Windows/Media/Ring03.wav')
