"""
Title: CONSISTENCY BOT BASE
Date Started: Dec 6, 2020
Version: 1.00
Version Start: Dec 6, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  To calculate probability if a stock experiences gain X in one period, what is the probability that it'll experience the same gain in the next period.
for each trial date
find all existing stocks
find all stocks that meet requirements
pick a stock at random
determine whether its next period growth passes or fails and record

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import random
import datetime as dt
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_singlechild, readpkl, buildfolders_regime_testrun, savetopkl
from tickerportalbot import tickerportal3
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source, PRICES
from timeperiodbot import getrandomexistdate
from statresearchbot import stat_profiler
from growthcalcbot import removeleadingzeroprices
from genericfunctionbot import multiprocessorshell
from CONSISTENCY_BASE_ALLMETRICVALS import allmetricval_cruncher, filterallmetrics


# filterqualifiers further
def filterqualifiers(verbose, scriptparams, beg_date, end_date, pool, rankmeth, rankregime):
    # get df of all metric values
    allmetricsdf = allmetricval_cruncher(scriptparams, beg_date, end_date, pool, rankmeth, rankregime)
    if verbose == 'verbose':
        print(allmetricsdf[['stock', 'unifatscore_rawtrue_mean']])
    # filter df
    finaldf = filterallmetrics(allmetricsdf, scriptparams, beg_date, end_date, rankmeth, rankregime)
    if verbose == 'verbose':
        print(finaldf[['stock', 'unifatscore_rawtrue_mean']])
    resultpool = finaldf['stock'].tolist()
    return resultpool


# get list of qualifiers from single exist date
def getqualifierlist(verbose, pricematrixdf, gainthreshold, gain_err, existpool, beg_date, end_date, mode):
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    all_cols = ['date'] + existpool
    pricedf = pricematrixdf[all_cols].copy()
    # SLICE OUT DATE RANGE REQUESTED
    pricedf = pricedf.loc[(pricedf['date'] >= beg_date) & (pricedf['date'] <= end_date)].copy()
    # RESET INDEX
    pricedf.reset_index(drop=True, inplace=True)
    # remove leading zeroes from raw prices
    pricedf = removeleadingzeroprices(pricedf, existpool)
    # REMOVE EVERY ROW EXCEPT FIRST AND LAST
    pricedf = pricedf.iloc[[0, -1], :]
    pricedf.reset_index(drop=True, inplace=True)
    # CALCULATE GAIN OVER THE TIME PERIOD
    pricedf[existpool] = pricedf[existpool].pct_change(periods=1, fill_method='ffill')
    # FILTER OUT COLUMNS THAT DONT MEET GAIN THRESHOLD
    if gain_err == "":
        if mode == 'split':
            qualifiersobj_bottom = pricedf[(pricedf.iloc[[-1], 1:] <= gainthreshold)].loc[1].dropna()
            qualifiersobj_top = pricedf[(pricedf.iloc[[-1], 1:] > gainthreshold)].loc[1].dropna()
            finaltuple = (qualifiersobj_bottom.to_dict(), qualifiersobj_top.to_dict())
        else:
            qualifiersobj = pricedf[(pricedf.iloc[[-1], 1:] > gainthreshold)].loc[1].dropna()
            finaltuple = qualifiersobj.to_dict()
    else:
        lowerbound = gainthreshold - gain_err
        upperbound = gainthreshold + gain_err
        if mode == 'split':
            qualifiersobj_bottom = pricedf[(pricedf.iloc[[-1], 1:] <= lowerbound)].loc[1].dropna()
            qualifiersobj_midbottom = pricedf[(pricedf.iloc[[-1], 1:] > lowerbound) & (pricedf.iloc[[-1], 1:] <= gainthreshold)].loc[1].dropna()
            qualifiersobj_midtop = pricedf[(pricedf.iloc[[-1], 1:] > gainthreshold) & (pricedf.iloc[[-1], 1:] <= upperbound)].loc[1].dropna()
            qualifiersobj_top = pricedf[(pricedf.iloc[[-1], 1:] > upperbound)].loc[1].dropna()
            finaltuple = (qualifiersobj_bottom.to_dict(), qualifiersobj_midbottom.to_dict(), qualifiersobj_midtop.to_dict(), qualifiersobj_top.to_dict())
        else:
            qualifiersobj = pricedf[(pricedf.iloc[[-1], 1:] > lowerbound) & (pricedf.iloc[[-1], 1:] < upperbound)].loc[1].dropna()
            finaltuple = qualifiersobj.to_dict()
    if verbose == 'verbose':
        print(finaltuple)
    return finaltuple


# single trial master
def singletrial_master(verbose, filterqualifiers_prev, filter_daterange, scriptparams, latestdate, firstdate, len_total, savedir, pricematrixdf, gain_prev, err_prev, gain_next, err_next, len_prev, len_next, mode, trialno):
    # do not continue unless there are qualifiers found
    qualifiers_prev = []
    while len(qualifiers_prev) == 0:
        qualifiers_prev_dict = {}
        while len(qualifiers_prev_dict) == 0:
            # get randomdate
            existdate = getrandomexistdate(latestdate, firstdate, len_total, daterangedb_source)
            # get existing stocks
            existpool = tickerportal3(existdate, 'common', 2)
            # get prev end date
            prev_end = str(dt.date.fromisoformat(existdate) + dt.timedelta(days=len_prev))
            # get all qualifiers
            qualifiers_prev_dict = getqualifierlist(verbose, pricematrixdf, gain_prev, err_prev, existpool, existdate, prev_end, '')
        qualifiers_prev = list(qualifiers_prev_dict.keys())
        # filter qualifiers_prev list
        if filterqualifiers_prev == 'yes':
            if filter_daterange == 'beforeprev':
                beg_date = ''
                end_date = existdate
            elif filter_daterange == 'prevplus':
                beg_date = ''
                end_date = prev_end
            elif filter_daterange == 'prev':
                beg_date = existdate
                end_date = prev_end
            qualifiers_prev = filterqualifiers(verbose, scriptparams, beg_date, end_date, qualifiers_prev, 'standard', '1isbest')
    # get next period dates
    next_end = str(dt.date.fromisoformat(prev_end) + dt.timedelta(days=len_next))
    # calculate gain in nextperiod
    qualifiers_next_dict = getqualifierlist(verbose, pricematrixdf, gain_next, err_next, qualifiers_prev, prev_end, next_end, mode)
    # calc proportion of prevstocks in nextstocks
    num_qualifiers_prev = len(qualifiers_prev)
    summary = {
        'trialno': trialno,
        'prev_beg': existdate,
        'prev_end': prev_end,
        'next_end': next_end,
        'len_prev': len_prev,
        'len_next': len_next,
        'qualifiers_prev': num_qualifiers_prev
        }
    if mode == 'split':
        if err_next == "":
            for tranch in enumerate(['bottom', 'top']):
                qualifiers_list = list(qualifiers_next_dict[tranch[0]].keys())
                num_qualifiers_next = len(qualifiers_list)
                consistscore = num_qualifiers_next / num_qualifiers_prev
                summary.update({
                    f'qualifiers_{tranch[1]}': num_qualifiers_next,
                    f'consistscore_{tranch[1]}': consistscore
                })
        else:
            for tranch in enumerate(['bottom', 'midbottom', 'midtop', 'top']):
                qualifiers_list = list(qualifiers_next_dict[tranch[0]].keys())
                num_qualifiers_next = len(qualifiers_list)
                consistscore = num_qualifiers_next / num_qualifiers_prev
                summary.update({
                    f'qualifiers_{tranch[1]}': num_qualifiers_next,
                    f'consistscore_{tranch[1]}': consistscore
                })
    else:
        qualifiers_next = list(qualifiers_next_dict.keys())
        num_qualifiers_next = len(qualifiers_next)
        num_qualifiers_prev = len(qualifiers_prev)
        # proportion of qualifying stocks that made next period qualifications
        consistscore = num_qualifiers_next / num_qualifiers_prev
        summary.update({
            'qualifiers_prev': num_qualifiers_prev,
            'qualifiers_next': num_qualifiers_next,
            'consistscore': consistscore
        })
    # save summary
    savetopkl(f'trialsummary_trialno{trialno}', savedir, summary)


# main consistency function
def consistencybotmaster(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    trialresults = buildfolders_singlechild(testrunparent, 'trialresults')
    # get trial iterables
    trialiters = np.arange(0, global_params['num_trials'], 1)
    # load pricematrix
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    # run trials
    targetvars = (global_params['verbose'], global_params['filterqualifiers_prev'], global_params['filter_daterange'], global_params['prev_filters'], global_params['latestdate'], global_params['firstdate'], global_params['len_prev'] + global_params['len_next'], trialresults, pricematrixdf, global_params['gain_prev'], global_params['err_prev'], global_params['gain_next'], global_params['err_next'], global_params['len_prev'], global_params['len_next'], global_params['mode'])
    multiprocessorshell(trialresults, singletrial_master, trialiters, 'no', targetvars)
    # assemble results
    allsummaries = []
    for child in trialresults.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        allsummaries.append(unpickled_raw)
    alltrialsdf = pd.DataFrame(data=allsummaries)
    alltrialsdf.to_csv(index=False, path_or_buf=testrunparent / "alltrialsummaries.csv")
    # get stats
    if global_params['mode'] == 'split':
        if global_params['err_next'] == "":
            for tranch in ['bottom', 'top']:
                statdict = stat_profiler(alltrialsdf[f'consistscore_{tranch}'].dropna())
                consiststatdf = pd.DataFrame(data=[statdict])
                consiststatdf.to_csv(index=False, path_or_buf=testrunparent / f"consistpctstats_{tranch}.csv")
                print(tranch, statdict)
        else:
            for tranch in ['bottom', 'midbottom', 'midtop', 'top']:
                statdict = stat_profiler(alltrialsdf[f'consistscore_{tranch}'].dropna())
                consiststatdf = pd.DataFrame(data=[statdict])
                consiststatdf.to_csv(index=False, path_or_buf=testrunparent / f"consistpctstats_{tranch}.csv")
                print(tranch, statdict)
    else:
        statdict = stat_profiler(alltrialsdf['consistscore'].dropna())
        consiststatdf = pd.DataFrame(data=[statdict])
        consiststatdf.to_csv(index=False, path_or_buf=testrunparent / "consistpctstats.csv")
        print(statdict)
