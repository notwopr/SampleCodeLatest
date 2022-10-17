"""
Title: MAXDD BASE
Date Started: Nov 10, 2020
Version: 1
Version Start: Nov 10, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Calculate the likelihood that portfolio will exceed its maxdrawdown during the testperiod.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
import datetime as dt
import pickle as pkl
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from filelocations import buildfolders_singlechild, savetopkl, readpkl, buildfolders_regime_testrun
from tickerportalbot import tickerportal2
from timeperiodbot import getrandomexistdate_multiple
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source
from statresearchbot import stat_profiler
from computersettings import computerobject
from filetests import checknum
from FINALBAREMINCRUNCHER import oldbaremin_cruncher
from STRATTEST_FUNCBASE_MMBM import allpctdrops_single


# GETS A STOCK'S MAXDD SUMMARY
def histmaxdd(savedir, test_beg, test_end, stock):
    # get all prices
    fullprices = grabsinglehistory(stock)
    # get historical maxdd
    histprices = fullprices.copy()
    histprices = fill_gaps2(histprices, '', test_beg)
    histpricelist = histprices[stock].tolist()
    bminrawhistpricelist = oldbaremin_cruncher(histpricelist)
    histprices['oldbareminraw'] = np.array(bminrawhistpricelist)
    histmaxdd = allpctdrops_single(histprices, stock, 'oldbareminraw', stock, 'max')
    # get current maxdd
    currprices = fullprices.copy()
    currprices = fill_gaps2(currprices, '', test_end)
    currpricelist = currprices[stock].tolist()
    bminrawcurrpricelist = oldbaremin_cruncher(currpricelist)
    currprices['oldbareminraw'] = np.array(bminrawcurrpricelist)
    currmaxdd = allpctdrops_single(currprices, stock, 'oldbareminraw', stock, 'max')
    # save summary
    stocksumm = {'stock': stock, 'histmaxdd': histmaxdd, 'currmaxdd': currmaxdd}
    savetopkl(f'stockmaxddsummary_{stock}', savedir, stocksumm)


# SINGLE TRIAL: PROPORTION OF STOCKS WHERE SUBSEQUENT PERIOD ALTERED MAXDD
def getmaxddchangepct(trialsumm, trialparent, trialresultparent, exist_date, startpool, testlen, benchticker):
    # get test period dates
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    # build subfolders for trial
    trialdumpfolder = buildfolders_singlechild(trialparent, 'dumpfiles')
    # run maxddsummary multiprocessor
    fn = partial(histmaxdd, trialdumpfolder, test_beg, test_end)
    pool = Pool(processes=computerobject.use_cores)
    pool.map(fn, startpool, 1)
    pool.close()
    pool.join()
    # wait for all files to download
    correct = len(startpool)
    downloadfinish = checknum(trialdumpfolder, correct, '')
    while downloadfinish is False:
        downloadfinish = checknum(trialdumpfolder, correct, '')
    # construct maxddsummdf
    table_results = []
    for child in trialdumpfolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    maxddsummdf = pd.DataFrame(data=table_results)
    # create column tallying where currmaxdd > histmaxdd
    maxddsummdf['maxddchanged'] = maxddsummdf['histmaxdd'] > maxddsummdf['currmaxdd']
    # calculate proportion where histmaxdd was changed
    maxddchangepct = maxddsummdf['maxddchanged'].mean()
    # calculate bench performance
    benchprices = grabsinglehistory(benchticker)
    benchprices = fill_gaps2(benchprices, test_beg, test_end)
    benchprices.reset_index(inplace=True, drop=True)
    benchperf = (benchprices.iat[-1, 1] / benchprices.iat[0, 1]) - 1
    # update summary
    trialsumm.update({'test_beg': test_beg, 'test_end': test_end, 'maxddchangepct': maxddchangepct, 'benchticker': benchticker, 'benchperf': benchperf})
    # save results of trial
    maxddsummdf.to_csv(index=False, path_or_buf=trialparent / f"maxddsummarydf_{exist_date}.csv")
    savetopkl(f'trialsumm_{exist_date}', trialresultparent, trialsumm)


# MASTER FUNCTION: ASSEMBLES PROPORTIONS OF ALL TRIALS
def prop_maxddadjusted_multitrial(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # build stage folders
    trialdumpparent = buildfolders_singlechild(testrunparent, 'trialdumpparent')
    trialresultparent = buildfolders_singlechild(testrunparent, 'trialresultparent')
    # get trialexistdates
    if len(global_params['statictrialexistdates']) != 0:
        if len(global_params['statictrialexistdates']) == global_params['num_trials']:
            alltrialexistdates = global_params['statictrialexistdates']
        else:
            print('The static trial exist dates you want to use do not equal the number of trials you want to run.  Exiting...')
            exit()
    else:
        alltrialexistdates = getrandomexistdate_multiple(global_params['num_trials'], global_params['firstdate'], global_params['latestdate'], global_params['testlen'], daterangedb_source)
    # for each trialdate get proportion of pool that histmaxdd was adjusted
    for trial in enumerate(alltrialexistdates):
        trialno = trial[0]
        existdate = trial[1]
        # build folders for trial
        trialparent = buildfolders_singlechild(trialdumpparent, f'trialno{trialno}_edate{existdate}')
        # get startpool
        if global_params['basepool'] == 'yes':
            trialfolder = f'\\trialno{trialno}_edate{existdate}'
            trialpath = trialfolder + global_params['subtrialfolderpath']
            fullbasepoolpath = global_params['testrunparentpath'] + trialpath
            basepoolfilename = global_params['basepoolfntemplate'] + existdate
            basepooldf = readpkl(basepoolfilename, Path(fullbasepoolpath))
            startpool = basepooldf['stock'].tolist()
        else:
            startpool = tickerportal2(existdate, 'common')
        # construct trial summary
        trialsumm = {'trialno': trialno, 'existdate': existdate, 'testlen': global_params['testlen']}
        # get maxdd change pct
        getmaxddchangepct(trialsumm, trialparent, trialresultparent, existdate, startpool, global_params['testlen'], global_params['benchticker'])
    # CREATE MASTERDF
    alltrialresults = []
    for child in trialresultparent.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        alltrialresults.append(unpickled_raw)
    masterdf = pd.DataFrame(data=alltrialresults)
    # ARCHIVE MASTERDF
    mdfn = f"alltrialsummaries_{global_params['metricsetname']}"
    masterdf.to_csv(index=False, path_or_buf=testrunparent / f"{mdfn}.csv")
    # get stat summary
    statcols = [
        'maxddchangepct'
    ]
    allstatdicts = []
    for statcol in statcols:
        datarr = masterdf[statcol].dropna().to_numpy()
        if len(datarr) >= 2:
            statdict = stat_profiler(datarr)
        else:
            statdict = {
                'stat_min': None,
                'stat_q1': None,
                'stat_mean': None,
                'stat_med': None,
                'stat_q3': None,
                'stat_max': None,
                'stat_std': None,
                'stat_sharpe': None
            }
        statdict.update({'category': statcol})
        allstatdicts.append(statdict)
    # CREATE STATDF
    statdf = pd.DataFrame(data=allstatdicts)
    # save results
    statsfn = f"maxddchange_multitrial_summary_{global_params['metricsetname']}"
    statdf.to_csv(index=False, path_or_buf=testrunparent / f"{statsfn}.csv")
    return statdf
