"""
Title: WINNER THRESHOLD FINDER BASE - BEST METRIC
Date Started: Feb 7, 2021
Version: 1.00
Version Start: Feb 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Gets losers and winners for each trial.  For each metric requested, find min and max values for that trial for both loser and winner groups.  If neither group ranges overlap, go to next trial.  If the two groups never overlap for all trials requested, then record metricname with each of its trial's records. Go to next metric in list.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_singlechild, readpkl, buildfolders_regime_testrun, savetopkl
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, PRICES
from timeperiodbot import getrandomexistdate_multiple
from genericfunctionbot import multiprocessorshell
from WINNERTHRESHOLDFINDER_FINDBESTMETRIC_BASE_CRUNCHER import metricfuncoverlaptester, getwinnerloserpools_singletrial
from STRATTEST_FUNCBASE import getmetcolname


# get all winners and losers (to save RAM for loading pricematrices)
def getallwinnerloser_shell(winnerloserpoolsdir, global_params, alltrialexistdates):
    # load price matrices into RAM
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    # download npdf data
    targetvars = (winnerloserpoolsdir, pricematrixdf, benchpricematrixdf, global_params['benchticker'], global_params['testlen'], global_params['winnerdefined'], global_params['loserdefined'], global_params['minimumage'])
    multiprocessorshell(winnerloserpoolsdir, getwinnerloserpools_singletrial, alltrialexistdates, 'yes', targetvars, global_params['chunksize'])


# master function
def bestmetricfinder_master(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # get trialexistdates
    if len(global_params['statictrialexistdates']) != 0:
        if len(global_params['statictrialexistdates']) == global_params['num_trials']:
            alltrialexistdates = global_params['statictrialexistdates']
        else:
            print('The static trial exist dates you want to use do not equal the number of trials you want to run.  Exiting...')
            exit()
    else:
        alltrialexistdates = getrandomexistdate_multiple(global_params['num_trials'], global_params['firstdate'], global_params['latestdate'], global_params['testlen'], daterangedb_source)
        # save dates
        savetopkl('trialdatedata', testrunparent, alltrialexistdates)
    # get winners and losers for each trial
    if len(global_params['statictrialexistdates']) != 0:
        winnerloserpoolsdir = global_params['statictrialbaseloc'] / 'winnerloserpoolsdir'
    else:
        winnerloserpoolsdir = buildfolders_singlechild(testrunparent, 'winnerloserpoolsdir')
        getallwinnerloser_shell(winnerloserpoolsdir, global_params, alltrialexistdates)
    # parse stage script
    scriptparams = global_params['metricscript']['scriptparams']
    # create folder for all trialsummaries for each metricitem
    summarydfsavedir = buildfolders_singlechild(testrunparent, 'metrictrialsummarydfsdump')
    # create folder for all metricval calculations
    metricvalcruncherdump = buildfolders_singlechild(testrunparent, 'metricvalcruncherdump')
    # for each metricfunc in paramscript, run metricfunc evaluator
    allmetricreports = []
    for metricitem in scriptparams:
        # get metcolname
        metcolname = getmetcolname(metricitem)
        metricitemdump = buildfolders_singlechild(metricvalcruncherdump, f'{metcolname}_dump')
        allsummariesdf = metricfuncoverlaptester(metricitemdump, summarydfsavedir, metricitem, metcolname, alltrialexistdates, winnerloserpoolsdir, global_params['savemode'], global_params['chunksize'])
        # report metricfunc performance
        if len(allsummariesdf) < global_params['num_trials']:
            reportdict = {'metricname': metcolname, 'overlapfound': 'yes'}
        else:
            reportdict = {'metricname': metcolname, 'overlapfound': 'no'}
        # append report
        allmetricreports.append(reportdict)
    # construct final metricreportdf
    finalreportdf = pd.DataFrame(data=allmetricreports)
    finalreportdf.to_csv(index=False, path_or_buf=testrunparent / "finalmetricreport.csv")
    print(finalreportdf)
