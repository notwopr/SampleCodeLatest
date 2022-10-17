"""
Title: Library of Functions for Test Period Insights
Date Started: July 8, 2020
Version: 2.50
Version Start: Jan 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Provide a centralized location for functions related to calculating insights regarding the test period on a given pool.
Versions:
2: modify leaderboard metrics
2.5: Simplify drop functions
Growth Rate
    Meanperf
    Medianperf
    avgperf
Reliability
    Meanperf_std
    Medianperf_std
    Avgperf_std
    Meanperf_mad
    Medianperf_mad
    Avgperf_mad
Turmoil
    Prevalence of dips
    Magnitude of dips
    Maxdip is low
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
from pathlib import Path
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl
from file_hierarchy import DirPaths
from Modules.growthcalcbot import removeleadingzeroprices
# from Modules.price_calib import convertpricearr
from newbacktest.ingredients_funclib.STRATTEST_FUNCBASE_MMBM import allpctdrops_single

PRICES = Path(DirPaths().eodprices)


# # return array of all drop values
# def alldropshell(priceseries, uppercol, lowercol):
#     # assign upper and lower arrays
#     upperarr = convertpricearr(priceseries, uppercol)
#     lowerarr = convertpricearr(priceseries, lowercol)
#     pctdrops = (lowerarr - upperarr) / upperarr
#     nonzerodrops = pctdrops[pctdrops < 0]
#     return nonzerodrops
#
#
# # get pct drop samples; use raw calibration only
# def allpctdrops_single(priceseries, uppercol, lowercol, stat_type):
#     nonzerodrops = alldropshell(priceseries, uppercol, lowercol)
#     metricscore = getdropstat_single(priceseries, nonzerodrops, stat_type)
#     return metricscore


# creates df of bench and portfolio prices
def benchplusportfolioprices(portfolio, benchticker, beg_date, end_date):
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    all_cols = ['date'] + portfolio
    nonbenchsliced = pricematrixdf[all_cols].copy()
    # PULL BENCH PRICES
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    all_bcols = ['date', benchticker]
    benchsliced = benchpricematrixdf[all_bcols].copy()
    # JOIN
    sliced = benchsliced.join(nonbenchsliced.set_index('date'), how="left", on="date")
    # SLICE OUT DATE RANGE REQUESTED
    sliced = sliced.loc[(sliced['date'] >= beg_date) & (sliced['date'] <= end_date)].copy()
    # RESET INDEX
    sliced.reset_index(drop=True, inplace=True)
    return sliced


# converts benchplusportdf of rawprices to normalized prices
def normalizedf(rawpricedf, portfolio, benchticker):
    # NORMALIZE EACH PRICE CURVE
    alltickers = portfolio + [benchticker]
    # remove leading zeroes from raw prices
    normpricedf = removeleadingzeroprices(rawpricedf, alltickers)
    firstp = normpricedf.loc[0, alltickers]
    normpricedf[alltickers] = (normpricedf[alltickers] - firstp) / firstp
    return normpricedf


# converts benchplusportdf of rawprices to normalized prices
def mktbeatpooldf(portfolio, benchticker, beg_date, end_date):
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    all_cols = ['date'] + portfolio
    nonbenchsliced = pricematrixdf[all_cols].copy()
    # PULL BENCH PRICES
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    all_bcols = ['date', benchticker]
    benchsliced = benchpricematrixdf[all_bcols].copy()
    # JOIN
    sliced = benchsliced.join(nonbenchsliced.set_index('date'), how="left", on="date")
    # SLICE OUT DATE RANGE REQUESTED
    sliced = sliced.loc[(sliced['date'] >= beg_date) & (sliced['date'] <= end_date)].copy()
    # RESET INDEX
    sliced.reset_index(drop=True, inplace=True)
    # NORMALIZE EACH PRICE CURVE
    alltickers = portfolio + [benchticker]
    # remove leading zeroes from raw prices
    sliced = removeleadingzeroprices(sliced, alltickers)
    firstp = sliced.loc[0, alltickers]
    sliced[alltickers] = (sliced[alltickers] - firstp) / firstp
    return sliced


# CALCULATES PROPORTION OF A GIVEN POOL THAT BEATS THE BENCH
def mktbeatpoolpct(verbose, portfolio, benchticker, beg_date, end_date):
    sliced = mktbeatpooldf(portfolio, benchticker, beg_date, end_date)
    benchperf = sliced.iloc[-1][benchticker]
    portbeatsumm = np.mean(sliced.iloc[-1][portfolio] > benchperf)
    # REPORT RESULTS
    if verbose == 'verbose':
        print(sliced)
        print(f'Of the {len(portfolio)} stocks tested against the benchmark {benchticker}, {portbeatsumm*len(portfolio)} of them ({portbeatsumm*100} %) beat the benchmark\'s performance of {benchperf*100} % for the period of {beg_date} to {end_date}.')
    return portbeatsumm


# CALCULATES VARIETY OF STATS RE POOL TIME PERIOD AND BENCHMARK
def mktbeatpoolstats(verbose, portfolio, benchticker, beg_date, end_date):
    # get rawprice df
    rawpricesdf = benchplusportfolioprices(portfolio, benchticker, beg_date, end_date)
    # Prevalence of dips
    dropprevresults = rawpricesdf.iloc[:, 1:].apply(lambda x: allpctdrops_single(x, 'baremaxraw', 'rawprice', 'prev'))
    # magnitude of dips
    dropmagresults = rawpricesdf.iloc[:, 1:].apply(lambda x: allpctdrops_single(x, 'baremaxraw', 'rawprice', 'avg'))
    # dropscores (dip prev * dip mag)
    dropscores = dropprevresults * dropmagresults
    # max dip
    dropmaxresults = rawpricesdf.iloc[:, 1:].apply(lambda x: allpctdrops_single(x, 'baremaxraw', 'rawprice', 'min'))
    # get normalized prices of portfolio and benchmark
    normpricedf = normalizedf(rawpricesdf, portfolio, benchticker)
    # separate portfolio into mktbeaters and mktfailures
    benchperf = normpricedf.iloc[-1][benchticker]
    mktbeatpool = normpricedf[portfolio].columns[(normpricedf.iloc[-1][portfolio] > benchperf)].tolist()
    failurepool = [item for item in portfolio if item not in mktbeatpool]
    # calc sizes
    poolsize = len(portfolio)
    mktbeatsize = len(mktbeatpool)
    failsize = len(failurepool)
    mktbeatpoolpct = mktbeatsize / poolsize
    mktfailpoolpct = failsize / poolsize
    # calc length of period
    period_len = (dt.date.fromisoformat(end_date) - dt.date.fromisoformat(beg_date)).days

    # create resultdict
    resultdict = {
        'beg_date': beg_date,
        'end_date': end_date,
        'period_len': period_len,
        'mktbeatpoolpct': mktbeatpoolpct,
        'mktfailpoolpct': mktfailpoolpct,
        'poolsize': poolsize,
        'mktbeatsize': mktbeatsize,
        'fsize': failsize,
        'fullpool': portfolio,
        'mktbeatpool': mktbeatpool,
        'failurepool': failurepool
        }
    if verbose == 'verbose':
        print(f'Of the {poolsize} stocks tested against the benchmark {benchticker}, {mktbeatpoolpct*poolsize} of them ({mktbeatpoolpct*100} %) beat the benchmark\'s performance of {benchperf*100} % for the {period_len}-day period of {beg_date} to {end_date}.')
        print('The following are the stocks that beat the benchmark:')
        print(mktbeatpool)
        print('The following are the stocks that did not beat the benchmark:')
        print(failurepool)
    # add benchticker stats
    benchdipprev = dropprevresults[benchticker]
    benchdipmag = dropmagresults[benchticker]
    benchdipscore = benchdipprev * benchdipmag
    benchdipmax = dropmaxresults[benchticker]
    resultdict.update({
        'benchmarkused': benchticker,
        'benchperf': benchperf,
        'benchdipprev': benchdipprev,
        'benchdipmag': benchdipmag,
        'benchdipscore': benchdipscore,
        'benchdipmax': benchdipmax
    })
    # add portfolio data
    for pooltype in ['pool', 'mktbeat', 'mktfail']:
        if pooltype == 'pool':
            stockgroup = portfolio
        elif pooltype == 'mktbeat':
            stockgroup = mktbeatpool
        elif pooltype == 'mktfail':
            stockgroup = failurepool
        # calc growth stats
        perf_mean = normpricedf.iloc[-1][stockgroup].mean()
        perf_median = normpricedf.iloc[-1][stockgroup].median()
        perf_mean_margin = perf_mean - benchperf
        perf_median_margin = perf_median - benchperf
        # calc dip stats
        dipprev_mean = dropprevresults[stockgroup].mean()
        dipprev_median = dropprevresults[stockgroup].median()
        dipmag_mean = dropmagresults[stockgroup].mean()
        dipmag_median = dropmagresults[stockgroup].median()
        dipscore_mean = dropscores[stockgroup].mean()
        dipscore_median = dropscores[stockgroup].median()
        dipmax_mean = dropmaxresults[stockgroup].mean()
        dipmax_median = dropmaxresults[stockgroup].median()
        # append to resultdict
        resultdict.update({
            f'{pooltype}perf_mean': perf_mean,
            f'{pooltype}perf_median': perf_median,
            f'{pooltype}perf_mean_margin': perf_mean_margin,
            f'{pooltype}perf_median_margin': perf_median_margin,
            f'{pooltype}dipprev_mean': dipprev_mean,
            f'{pooltype}dipprev_median': dipprev_median,
            f'{pooltype}dipmag_mean': dipmag_mean,
            f'{pooltype}dipmag_median': dipmag_median,
            f'{pooltype}dipscore_mean': dipscore_mean,
            f'{pooltype}dipscore_median': dipscore_median,
            f'{pooltype}dipmax_mean': dipmax_mean,
            f'{pooltype}dipmax_median': dipmax_median,
            })
        # REPORT RESULTS
        if verbose == 'verbose':
            print(f'The {pooltype} had a mean performance of {perf_mean*100} % (margin over {benchticker} of {perf_mean_margin*100} %). The pool had a median performance of {perf_median*100} % (margin over {benchticker} of {perf_median_margin*100} %).')
    return resultdict


# RETURNS LIST OF STOCKS THAT BEAT THE BENCH
def mktbeatpool_list(portfolio, benchticker, beg_date, end_date):
    sliced = mktbeatpooldf(portfolio, benchticker, beg_date, end_date)
    benchperf = sliced.iloc[-1][benchticker]
    mktbeatpool = sliced[portfolio].columns[(sliced.iloc[-1][portfolio] > benchperf)].tolist()
    return mktbeatpool


# RETURNS GROWTH RATE OF GIVEN PORTFOLIO
def growthrate(portfolio, benchticker, beg_date, end_date):
    sliced = mktbeatpooldf(portfolio, benchticker, beg_date, end_date)
    portfoliogrowth = sliced.iloc[-1][portfolio].mean()
    return portfoliogrowth


# RETURNS GROWTH RATE OF PORTFOLIO, BENCHMARK AND MARGIN
def growthandmarginrate(portfolio, benchticker, beg_date, end_date):
    sliced = mktbeatpooldf(portfolio, benchticker, beg_date, end_date)
    portfoliogrowth = sliced.iloc[-1][portfolio].mean()
    benchperf = sliced.iloc[-1][benchticker]
    marginrate = portfoliogrowth - benchperf
    return portfoliogrowth, benchperf, marginrate
