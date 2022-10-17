"""
Title: PULLOUT BOT MASTER
Date Started: Dec 4, 2020
Version: 4.00
Version Start: Jan 15, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  To tell you when and if you should exit a position in a stock based on the likelihood it will end up beating the market by the end of the testperiod.

Pullout percentage represents the proportion of stocks in a pool that are beating a given benchmark.  Overall pullout percentage is the proportion of days out of the total in a test period that a stock beats a given benchmark in normalized price growth. If the test period is one year, we normalize the price graphs for that period, the overall pullout percentage are the number of days where a given stock\'s normalized price graph is above the benchmarks

By day pull out percentage represents the proportion of stocks in a pool that on a given day in a test period, the proportion of stocks within a given pool whose normalized price graph on that day is above that of the benchmark.

For each trial, all existing stocks were pulled and separated between winners and losers. The winners were those stocks whose overall gain over the test period exceeded the given benchmark; losers fell short.

"Portbeatpct" is the proportion of stocks in a winner or losergroup that currently has its normalized price graph above the benchmark.  This is different from pulloutpct.  If you look at bydaycharts, portbeatpct gives you what proportion of winners/losers on a given day has their normalized price graph above the benchmark on that day.  Pulloutpct on that same day gives you the cumulative proportion of days up to that day that a stock was above the benchmark's normalized price graph and then averages all stocks within a winner/loser group for that day to give you the value for that day.
Versions:
2: PRevious version had pulloutpct daybyday just be the mean of stocks that beat the market for that day when for a more accurate figure it should be each stock's overall pulloutpct up to that day and then averaged.
3: Separate creation of normpricedf from remainder in two separate multiprocessing stages to save memory.
4: consolidate functions to reduce memory usage.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
#   THIRD PARTY IMPORTS
import numpy as np
import pandas as pd
from scipy import stats
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_singlechild, readpkl, buildfolders_regime_testrun, savetopkl
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, PRICES
from timeperiodbot import getrandomexistdate_multiple
from statresearchbot import stat_profiler
from genericfunctionbot import multiprocessorshell
from PULLOUT_BASE_GETWINNERSLOSERS import normpricedf_singletrial


# clean normpricedf
def cleandf(mode, normpricesdf, startpool, trialno, exist_date, testlen):
    # remove first row, remove benchmark and date cols
    normpricesdf = normpricesdf.iloc[1:][startpool]
    # add day column
    normpricesdf['testday'] = normpricesdf.index
    # reorder columns
    normpricesdf = normpricesdf[['testday']+startpool]
    # reset index
    normpricesdf.reset_index(inplace=True, drop=True)
    return normpricesdf


# convert boolean pricedf into byday pulloutpct
def booleantobydaydf(booleanpricedf, pool):
    booleanpricedf[pool] = booleanpricedf[pool].apply(lambda x: x.expanding(1).mean())
    return booleanpricedf


def getbydayandtrialstats(pricedf, mode, startpool, benchticker, trialno, exist_date, testlen, winnerpool, loserpool, trialsummary, masterbydaydf):
    if mode == 'margins':
        # convert normprices to margindata
        pricedf[startpool] = pricedf[startpool].apply(lambda x: x - pricedf[benchticker])
    elif mode == 'pulloutpct' or mode == 'portbeatpct':
        # convert normprices to boolean whether it beat or did not beat market
        pricedf[startpool] = pricedf[startpool].apply(lambda x: x > pricedf[benchticker])
    elif mode == 'posdpcpct':
        # convert dpcpricedf to boolean whether it is or isn't positive
        pricedf[startpool] = pricedf[startpool].apply(lambda x: x > 0)
    # clean df
    pricedf = cleandf(mode, pricedf, startpool, trialno, exist_date, testlen)
    # convert boolean df to bydaypulloutpct values or bydayposdpcpct values
    if mode == 'pulloutpct' or mode == 'posdpcpct':
        pricedf = booleantobydaydf(pricedf, startpool)
    # calc stats
    for key, val in {'winners': winnerpool, 'losers': loserpool}.items():
        # copy pooltype df
        subpool = val
        subpooldf = pricedf[['testday']+subpool].copy()
        # get per stock stat values
        if mode == 'portbeatpct':
            perstockstatvalues = subpooldf[subpool].mean(axis=0)
        else:
            perstockstatvalues = subpooldf.iloc[-1][subpool]
        # get subpoolstats and bydaysubpoolstats
        allcols = []
        for stat_type in ['mean', 'median', 'min', 'max', 'std', 'mad']:
            if stat_type == 'mean':
                overallsubpoolstat = perstockstatvalues.mean()
                subpooldf[f'byday{stat_type}_{mode}_{key}'] = subpooldf[subpool].mean(axis=1)
            elif stat_type == 'median':
                overallsubpoolstat = perstockstatvalues.median()
                subpooldf[f'byday{stat_type}_{mode}_{key}'] = subpooldf[subpool].median(axis=1)
            elif stat_type == 'min':
                overallsubpoolstat = perstockstatvalues.min()
                subpooldf[f'byday{stat_type}_{mode}_{key}'] = subpooldf[subpool].min(axis=1)
            elif stat_type == 'max':
                overallsubpoolstat = perstockstatvalues.max()
                subpooldf[f'byday{stat_type}_{mode}_{key}'] = subpooldf[subpool].max(axis=1)
            elif stat_type == 'std':
                overallsubpoolstat = perstockstatvalues.std()
                subpooldf[f'byday{stat_type}_{mode}_{key}'] = subpooldf[subpool].std(axis=1)
            elif stat_type == 'mad':
                overallsubpoolstat = stats.median_abs_deviation(perstockstatvalues, nan_policy='omit')
                # overallsubpoolstat = perstockstatvalues.mad() until they fix the bug for this...
                subpooldf[f'byday{stat_type}_{mode}_{key}'] = subpooldf[subpool].apply(lambda x: stats.median_abs_deviation(x, nan_policy='omit'), axis=1)
                # subpooldf[f'byday{stat_type}_{mode}_{key}'] = subpooldf[subpool].mad(axis=1) until they fix the bug for this...
            trialsummary.update({f'{stat_type}_{mode}_{key}': overallsubpoolstat})
            allcols.append(f'byday{stat_type}_{mode}_{key}')
        # byday stats: for each day get the subpool stat value
        subpooldf = subpooldf[['testday'] + allcols].copy()
        masterbydaydf = masterbydaydf.join(subpooldf.set_index('testday'), how="left", on="testday")
    return masterbydaydf, trialsummary


# single pulloutbot trial
def pulloutbot_singletrial(npdfs, overallstats, bydaydfs, benchticker, testlen, trial):
    trialno = trial[0]
    exist_date = trial[1]
    # open npdf data file
    npdfdict = readpkl(f'npdfdatadict_trial{trialno}', npdfs)
    # create master stat objects
    trialsummary = {'trialno': trialno, 'testlen': testlen, 'benchticker': benchticker, 'test_beg': npdfdict['test_beg'], 'test_end': npdfdict['test_end']}
    masterbydaydf = pd.DataFrame(data={'testday': np.arange(1, testlen+1)})
    for mode in ['portbeatpct', 'pulloutpct', 'posdpcpct', 'gains', 'margins']:
        # make modifiable copy of sourcedf
        if mode == 'posdpcpct':
            pricedf = npdfdict['dpcpricedf']
        else:
            pricedf = npdfdict['normpricesdf']
        masterbydaydf, trialsummary = getbydayandtrialstats(pricedf.copy(), mode, npdfdict['startpool'], benchticker, trialno, exist_date, testlen, npdfdict['winnerpool'], npdfdict['loserpool'], trialsummary, masterbydaydf)
    # save stats
    savetopkl(f'bydaystats_trial{trialno}', bydaydfs, masterbydaydf)
    savetopkl(f'overallstats_trial{trialno}', overallstats, trialsummary)


# download npdf shell (to save RAM for loading pricematrices)
def downloadnpdfallshell(npdfs, global_params, alltrialexistdates):
    # load price matrices into RAM
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    # download npdf data
    targetvars = (npdfs, pricematrixdf, benchpricematrixdf, global_params['benchticker'], global_params['testlen'], global_params['winnerdefined'], global_params['loserdefined'])
    multiprocessorshell(npdfs, normpricedf_singletrial, alltrialexistdates, 'yes', targetvars)


# main pulloutbot function
def pulloutbotmaster(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    overallstats = buildfolders_singlechild(testrunparent, 'overallstats')
    bydaydfs = buildfolders_singlechild(testrunparent, 'bydaydfs')
    npdfs = buildfolders_singlechild(testrunparent, 'npdfs')
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
    # get pricedf and winner/loser trialdata
    downloadnpdfallshell(npdfs, global_params, alltrialexistdates)
    # run get byday and overall stats
    targetvars = (npdfs, overallstats, bydaydfs, global_params['benchticker'], global_params['testlen'])
    multiprocessorshell(bydaydfs, pulloutbot_singletrial, alltrialexistdates, 'yes', targetvars)
    # construct mastertrialdf
    table_results = []
    for child in overallstats.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    overallstatsdf = pd.DataFrame(data=table_results)
    # save df
    overallstatsdf.to_csv(index=False, path_or_buf=testrunparent / "overallstats_alltrialsummaries.csv")
    # get overallpullout pct stats
    masteroverallstatdata = []
    for mode in ['portbeatpct', 'pulloutpct', 'posdpcpct', 'gains', 'margins']:
        for group in ['winners', 'losers']:
            for stat_type in ['mean', 'median', 'min', 'max', 'std', 'mad']:
                statdict = {'category': f'{stat_type}_{mode}_{group}'}
                statdict.update(stat_profiler(overallstatsdf[f'{stat_type}_{mode}_{group}'].dropna().to_numpy()))
                masteroverallstatdata.append(statdict)
    # save final df
    masteroverallstats = pd.DataFrame(data=masteroverallstatdata)
    masteroverallstats.to_csv(index=False, path_or_buf=testrunparent / "masteroverallstats.csv")
    # get byday pullout pct stats
    masterdflist = []
    for child in bydaydfs.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        masterdflist.append(unpickled_raw)
    bydaydfscombined = pd.concat(masterdflist, ignore_index=True)
    meanstats = bydaydfscombined.groupby('testday').mean()
    medianstats = bydaydfscombined.groupby('testday').median()
    stdstats = bydaydfscombined.groupby('testday').std()
    madstats = bydaydfscombined.groupby('testday').mad()
    minstats = bydaydfscombined.groupby('testday').min()
    maxstats = bydaydfscombined.groupby('testday').max()
    allstats = {
        'mean': meanstats,
        'median': medianstats,
        'std': stdstats,
        'mad': madstats,
        'min': minstats,
        'max': maxstats
        }
    # create masterbydaydf
    masterbydaydf = pd.DataFrame(data={'testday': np.arange(1, global_params['testlen']+1)})
    for key, statdf in allstats.items():
        # rename cols
        statdf = pd.DataFrame(statdf.reset_index())
        for mode in ['portbeatpct', 'pulloutpct', 'posdpcpct', 'gains', 'margins']:
            for group in ['winners', 'losers']:
                for stat_type in ['mean', 'median', 'min', 'max', 'std', 'mad']:
                    statdf.rename(columns={f'byday{stat_type}_{mode}_{group}': f'byday{stat_type}_{mode}_{group}_{key}'}, inplace=True)
        masterbydaydf = masterbydaydf.join(statdf.set_index('testday'), how="left", on="testday")
    masterbydaydf.to_csv(index=False, path_or_buf=testrunparent / "masterbydaystats.csv")
    # save byday dfs
    for mode in ['portbeatpct', 'pulloutpct', 'posdpcpct', 'gains', 'margins']:
        for group in ['winners', 'losers']:
            for key in ['mean', 'median', 'min', 'max', 'std', 'mad']:
                savecols = []
                for stat_type in ['mean', 'median', 'min', 'max', 'std', 'mad']:
                    savecols.append(f'byday{stat_type}_{mode}_{group}_{key}')
                # save final df
                savedf = masterbydaydf[['testday']+savecols].copy()
                savedf.to_csv(index=False, path_or_buf=testrunparent / f"masterbydaystats_{mode}_{group}_({key}ofalltrials).csv")
    # create custom dfs
    for mode in ['pulloutpct', 'posdpcpct', 'gains', 'margins']:
        for charttype in ['bounded', 'stability']:
            # set by day types and statcoltypes
            if charttype == 'stability':
                bydaytypes = ['bydaymedian', 'bydaymad']
            elif charttype == 'bounded':
                bydaytypes = ['bydaymedian']
            # pull source cols
            maincols = []
            for bydaytype in bydaytypes:
                for group in ['winners', 'losers']:
                    if charttype == 'stability':
                        if bydaytype == 'bydaymedian':
                            statcol = 'mad'
                        elif bydaytype == 'bydaymad':
                            statcol = 'median'
                        maincols.append(f'{bydaytype}_{mode}_{group}_{statcol}')
                    elif charttype == 'bounded':
                        for statcol in ['mad', 'median']:
                            maincols.append(f'{bydaytype}_{mode}_{group}_{statcol}')
            # establish basedf
            customdf = masterbydaydf[['testday']+maincols].copy()
            # if charttype is bounded, add outlier cols
            if charttype == 'bounded':
                for group in ['winners', 'losers']:
                    # get 1.5*MAD val column
                    customdf[f'1.5*mad {group}'] = customdf[f'bydaymedian_{mode}_{group}_mad'] * 1.5
                    # get mainval +/- 1.5*madval
                    customdf[f'{group}-(1.5*MAD)'] = customdf[f'bydaymedian_{mode}_{group}_median'] - customdf[f'1.5*mad {group}']
                    customdf[f'{group}+(1.5*MAD)'] = customdf[f'bydaymedian_{mode}_{group}_median'] + customdf[f'1.5*mad {group}']
            # save df
            customdf.to_csv(index=False, path_or_buf=testrunparent / f"{charttype}df_{mode}.csv")
