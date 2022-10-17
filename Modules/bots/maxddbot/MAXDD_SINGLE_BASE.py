"""
Title: MAXDD SINGLE BASE
Date Started: Nov 11, 2020
Version: 1
Version Start: Nov 11, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Calculate the likelihood that a stock will exceed its maxdrawdown during the testperiod.

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
from filelocations import buildfolders_singlechild, savetopkl, buildfolders_regime_testrun
from timeperiodbot import getrandomexistdate_multiple
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source
from computersettings import computerobject
from filetests import checknum
from FINALBAREMINCRUNCHER import oldbaremin_cruncher
from STRATTEST_FUNCBASE_MMBM import allpctdrops_single
from correlationresearch import twolistcorr


# GETS A STOCK'S MAXDD SUMMARY FOR SINGLE DATE
def getmaxdds(trialsumm, test_beg, test_end, stock):
    # get all prices
    fullprices = grabsinglehistory(stock)
    # get historical maxdd
    histprices = fullprices.copy()
    histprices = fill_gaps2(histprices, '', test_beg)
    histpricelist = histprices[stock].tolist()
    bminrawhistpricelist = oldbaremin_cruncher(histpricelist)
    histprices['oldbareminraw'] = np.array(bminrawhistpricelist)
    histmaxdd = allpctdrops_single(histprices, stock, 'oldbareminraw', 'max')
    # get current maxdd
    currprices = fullprices.copy()
    currprices = fill_gaps2(currprices, '', test_end)
    currpricelist = currprices[stock].tolist()
    bminrawcurrpricelist = oldbaremin_cruncher(currpricelist)
    currprices['oldbareminraw'] = np.array(bminrawcurrpricelist)
    currmaxdd = allpctdrops_single(currprices, stock, 'oldbareminraw', 'max')
    # update summary
    trialsumm.update({'histmaxdd': histmaxdd, 'currmaxdd': currmaxdd})
    return trialsumm


# GET MAXDD STATS FOR SINGLE EXISTDATE
def getmaxddstats_singledate(dumpfolder, stock, testlen, benchticker, trialpackage):
    trialno = trialpackage[0]
    exist_date = trialpackage[1]
    # get test period dates
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    # create summary dict
    trialsumm = {
        'trialno': trialno,
        'existdate': exist_date,
        'testlen': testlen,
        'test_beg': test_beg,
        'test_end': test_end,
        'stock': stock
        }
    trialsumm = getmaxdds(trialsumm, test_beg, test_end, stock)
    # calculate bench performance
    benchprices = grabsinglehistory(benchticker)
    benchprices = fill_gaps2(benchprices, test_beg, test_end)
    benchprices.reset_index(inplace=True, drop=True)
    benchperf = (benchprices.iat[-1, 1] / benchprices.iat[0, 1]) - 1
    # update summary
    trialsumm.update({'benchticker': benchticker, 'benchperf': benchperf})
    # save results of trial
    savetopkl(f'trialsumm_{exist_date}', dumpfolder, trialsumm)


# MASTER FUNCTION: ASSEMBLES PROPORTIONS OF ALL TRIALS
def prop_maxddadjusted_multitrial_singlestock(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # build stage folders
    trialdumpparent = buildfolders_singlechild(testrunparent, 'trialdumpparent')
    # get trialexistdates
    if len(global_params['statictrialexistdates']) != 0:
        if len(global_params['statictrialexistdates']) == global_params['num_trials']:
            alltrialexistdates = global_params['statictrialexistdates']
        else:
            print('The static trial exist dates you want to use do not equal the number of trials you want to run.  Exiting...')
            exit()
    else:
        # get stock's firstdate
        with open(daterangedb_source, "rb") as targetfile:
            daterangedb = pkl.load(targetfile)
        latestdate = daterangedb[daterangedb['stock'] == global_params['stock']]['last_date'].item()
        firstdate = daterangedb[daterangedb['stock'] == global_params['stock']]['first_date'].item()
        # if benchmark used is younger than stock examined, use benchmark's firstdate instead
        benchprices = grabsinglehistory(global_params['benchticker'])
        benchprices = fill_gaps2(benchprices, '', '')
        benchfirstdate = benchprices.iat[0, 0]
        if dt.date.fromisoformat(firstdate) < benchfirstdate:
            firstdate = benchfirstdate
        alltrialexistdates = getrandomexistdate_multiple(global_params['num_trials'], firstdate, latestdate, global_params['testlen'], daterangedb_source)

    # for each trialdate get histmaxdd and currmaxdd
    fn = partial(getmaxddstats_singledate, trialdumpparent, global_params['stock'], global_params['testlen'], global_params['benchticker'])
    pool = Pool(processes=computerobject.use_cores)
    pool.map(fn, enumerate(alltrialexistdates), 1)
    pool.close()
    pool.join()
    # wait for all files to download
    correct = len(alltrialexistdates)
    downloadfinish = checknum(trialdumpparent, correct, '')
    while downloadfinish is False:
        downloadfinish = checknum(trialdumpparent, correct, '')
    # construct maxddsummdf
    table_results = []
    for child in trialdumpparent.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    maxddsummdf = pd.DataFrame(data=table_results)
    # add maxdd change column
    maxddsummdf['maxddchanged'] = maxddsummdf['histmaxdd'] > maxddsummdf['currmaxdd']
    # add binary version of change col
    maxddsummdf['maxddchanged_binary'] = 1 * maxddsummdf['maxddchanged']
    # calculate proportion where histmaxdd was changed
    maxddchangepct = maxddsummdf['maxddchanged'].mean()
    # ARCHIVE MASTERDF
    mdfn = f"alltrialsummaries_{global_params['metricsetname']}_{global_params['stock']}"
    maxddsummdf.to_csv(index=False, path_or_buf=testrunparent / f"{mdfn}.csv")
    # report changepct stats
    allchangeresults = maxddsummdf['maxddchanged'].tolist()
    num_changed = len([item for item in allchangeresults if item is True])
    num_unchanged = len([item for item in allchangeresults if item is False])
    corrlist1 = maxddsummdf['maxddchanged_binary'].tolist()
    corrlist2 = maxddsummdf['benchperf'].tolist()
    corrfig = twolistcorr(corrlist1, corrlist2, global_params['corrmethod'])
    print(f'Out of {global_params["num_trials"]} trials run on {global_params["stock"]}, the historical max drawdown was exceeded during the {global_params["testlen"]}-day period following a trial\'s existdate in {num_changed} of those trials. In the remaining {num_unchanged} trials, the maxdrawdown remained the same.')
    print(f'This represents a maxdrawdown change probability of {maxddchangepct*100} %.  This means that on any given day, {global_params["stock"]} would have a {maxddchangepct*100} % chance of seeing its max drawdown exceeded in the {global_params["testlen"]}-days following.')
    print(f'The degree to which {global_params["stock"]}\'s maxdrawdown was exceeded depended on how the benchmark {global_params["benchticker"]} performed is {corrfig}.')
