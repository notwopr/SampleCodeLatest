"""
Title: TWO SIGMA FORMATTER
Date Started: Sept 7, 2021
Version: 1
Version Start: Sept 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Once you have created all stock rankings, then run this on that parent folder.  Used to format CSV files to fit 2 Sigma's requirements and view performance.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from timeperiodbot import timeperiodbot
from filelocations import readcsv
import pandas as pd
from STRATTEST_TWOSIGMA_FORMATTER_BASE import createperiodsummary


# SET DATE AND TEST NUMBER AND REGIME
todaysdate = '2021-11-26'
setnumber = 5
testregimename = 'TWO SIGMA NOV SUBMISSION'
# SET INVESTMENT PERIOD, START AND END DATE
investperiod = '365D'
startdate = '2006-08-07'
enddate = '2021-08-03'
# SET BENCHMARK YOU WANT TO COMPARE
benchmark = '^IXIC'
# SET STARTING CAPITAL
startcapital = 100000
# SET RANK BATCH TO CHOOSE AS PORTFOLIO
rankstart = None
rankend = 10
# SAVE RECORD OF ENTER/EXIT DATES AND PORTFOLIOS?
savetimesheet = 'yes'
# ARE ALL THE SOURCEFILES FROM WHICH TO RUN ANALYSIS CONSOLIDATED IN ONE FOLDER?
consolidated = "no"
# WHAT IS THE PREFIX FOR THE SOURCEFILE?
sourcefileprefix = 'Stage 3_STAGE3_groplusvolv15g_finalists_as_of_'
# IF CONSOLIDATED, SET LOCATION OF FOLDER CONTAINING ALL SOURCEFILES
sourcefolder = Path(r'C:\Users\david\Documents\PROJECTBELUGA\BOT_DUMP\strattest_singles\testset2021111_1')
# DID THE STRAT USE MULTISTAGE MODE?
multistagemode = 'no'


if __name__ == '__main__':
    # set mod date
    mod_date = todaysdate.replace("-", "")
    # get invest dates
    allinvestdates = timeperiodbot(investperiod, startdate, enddate, 'all', '')
    # set newcapital var
    endcapital = startcapital
    benchendcapital = startcapital
    # number of investment periods
    numperiods = len(allinvestdates)-1
    # get all period summaries and analysis
    allperiodsummaries = []
    # if not consolidated, set sourcefolder
    if consolidated != 'yes':
        testregimeparent = computerobject.bot_dump / testregimename
        sourcefolder = testregimeparent / f'testset{mod_date}_{setnumber}'
    # for each investdate, get portfolio
    for testind in range(numperiods):
        # get full stock ranking
        if consolidated == 'yes':
            resultdf = readcsv(f'{sourcefileprefix}{allinvestdates[testind]}', sourcefolder)
        else:
            # set investperiod ranking file location
            if multistagemode == 'yes':
                resultfileloc = sourcefolder / f'D{mod_date}T{testind}'
                sourcefn = 'multistagerankings'
            else:
                resultfileloc = sourcefolder / f'D{mod_date}T{testind}' / 'Stage 3_parent'
                sourcefn = f'{sourcefileprefix}{allinvestdates[testind]}'
            resultdf = readcsv(sourcefn, resultfileloc)
        allperiodsummaries, endcapital, benchendcapital = createperiodsummary(resultdf, allinvestdates, testind, rankstart, rankend, endcapital, benchendcapital, benchmark, savetimesheet, allperiodsummaries)

    # final report
    overallrate = round(((endcapital / startcapital) - 1) * 100, 2)
    benchoverallrate = round(((benchendcapital / startcapital) - 1) * 100, 2)
    overallportdiff = endcapital - benchendcapital
    effectiverate = round((((endcapital/startcapital) ** (1/numperiods))-1) * 100, 2)
    bencheffectiverate = round((((benchendcapital/startcapital) ** (1/numperiods))-1) * 100, 2)
    print('\n')
    print('CONCLUSION')
    print(f'Overall, had you gone with this strategy from {startdate} to {enddate}, investing in {investperiod} periods, your capital would have gone from ${startcapital:,} to ${endcapital:,}, an overall growth rate of {overallrate:,} %, or ${round(endcapital - startcapital, 2):,} overall. This would translate to an effective investment period growth rate of {effectiverate:,} % per investment period.')
    print(f'In contrast, had you put your money in {benchmark} instead, your capital would have gone from ${startcapital:,} to ${benchendcapital:,}, an overall growth rate of {benchoverallrate:,} %, or ${benchendcapital - startcapital:,} overall. This would translate to an effective investment period growth rate of {bencheffectiverate:,} % per investment period.')
    print(f'Therefore as a result of using the strategy from {startdate} to {enddate}, your portfolio therefore would have experienced a marginal rate over {benchmark} of {round(overallrate - benchoverallrate, 2):,} %, a difference of ${round(overallportdiff, 2):,}.')

    # record if requested
    if savetimesheet == 'yes':
        # create pandas of results
        masterdf = pd.DataFrame(data=allperiodsummaries)
        # save to csv
        masterdf.to_csv(index=False, path_or_buf=sourcefolder / f"CHOI_TWOSIGMA_testset{mod_date}_{setnumber}.csv")
        playsound('C:/Windows/Media/Ring03.wav')
