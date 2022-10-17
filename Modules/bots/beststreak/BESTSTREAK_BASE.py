"""
Title: Best Streak Base Script
Date Started: September 26, 2020
Version: 1.0
Version Start: September 26, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Functions calculate mkt beat streak stats.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import math
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from Modules.tickerportalbot import tickerportal3
from file_hierarchy import PRICES, daterangedb_source, tickerlistcommon_source
from file_functions import savetopkl, readpkl, buildfolders_singlechild
from Modules.list_functions import intersectlists
from Modules.multiprocessing import multiprocessorshell
from Modules.ranking_calib import mmcalibrated


# same as mktbeatpooldf but asks for pricematrix to optimize RAM
def mktbeatpooldf_multiprocessor(portfolio, benchticker, beg_date, end_date, pricematrixdf):

    # SLICE OUT DATE RANGE REQUESTED
    pricematrixdf = pricematrixdf.loc[(pricematrixdf['date'] >= beg_date) & (pricematrixdf['date'] <= end_date)].copy()
    # RESET INDEX
    pricematrixdf.reset_index(drop=True, inplace=True)
    # NORMALIZE EACH PRICE CURVE
    alltickers = portfolio + [benchticker]
    firstp = pricematrixdf.loc[0, alltickers]
    pricematrixdf[alltickers] = (pricematrixdf[alltickers] - firstp) / firstp
    return pricematrixdf


# for given period, returns df of stocks and their performance against benchmark
def period_cruncher(latestdate, allexistingstocks, benchticker, period_dump, pricematrixdf, period):
    # get performance df
    perfdf = mktbeatpooldf_multiprocessor(allexistingstocks, benchticker, period[1][0], period[1][1], pricematrixdf)
    # remove all rows except last
    perfdf = perfdf.iloc[[-1], :]
    perfdf.reset_index(drop=True, inplace=True)
    # get benchperf
    benchperf = perfdf[benchticker].item()
    # remove bench entry
    perfdf = perfdf[['date']+allexistingstocks]
    # REFORMAT IN STOCKNAME-GROWTH COLUMN FORMAT
    margcolname = f'Period {period[0]}: {period[1][0]} TO {period[1][1]}'
    perfdf = perfdf.transpose()
    perfdf = perfdf.iloc[1:]
    perfdf.reset_index(inplace=True)
    perfdf.rename(columns={'index': 'stock', 0: margcolname}, inplace=True)
    perfdf[margcolname] = perfdf[margcolname] - benchperf
    # SAVE perfdf
    savetopkl(f'perfdf_period{period[0]}', period_dump, perfdf)


# for given time period and benchmark, and periodlen, return rank of stocks by how well it did against benchmark
def beststreak_cruncher(verbose, verbosefile, beg_date, end_date, benchticker, periodlen, avg_type, dev_type, avgmarginweight, devmarginweight, num_mktbeatweight, savedir, rankmeth, rankregime, custompool, chunksize):

    # GET LIST OF ALL STOCKS EXISTING FOR THAT PERIOD
    allexistingstocks = tickerportal3(beg_date, 'common', 2)
    if custompool != []:
        allexistingstocks = intersectlists(custompool, allexistingstocks)
    # GET ALL TEST PERIODS IN THE DATE RANGE
    daterange = (dt.date.fromisoformat(end_date) - dt.date.fromisoformat(beg_date)).days
    totalchunks = math.ceil(daterange / periodlen)
    all_periods = [[str(dt.date.fromisoformat(beg_date) + dt.timedelta(days=periodlen*(chunknum-1))), str(dt.date.fromisoformat(beg_date) + dt.timedelta(days=periodlen*(chunknum)))] for chunknum in range(1, totalchunks+1)]

    # STORE LAST AVAILABLE DATE
    with open(daterangedb_source, "rb") as targetfile:
        daterangedb = pkl.load(targetfile)
    lastdate_dateobj = daterangedb['last_date'].apply(lambda x: dt.date.fromisoformat(x))
    lastdates = lastdate_dateobj.tolist()
    latestdate = str(np.max(lastdates))

    # REMOVE PERIOD WHERE THE LAST DATE IS GREATER THAN LAST AVAILABLE DATE
    all_periods = [item for item in all_periods if dt.date.fromisoformat(item[1]) <= dt.date.fromisoformat(latestdate)]

    # CREATE MASTERTALLY DF
    mastertallydf = pd.DataFrame(data={'stock': allexistingstocks})

    # create period_dump
    period_dump = buildfolders_singlechild(savedir, 'period_dump')
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    all_cols = ['date'] + allexistingstocks
    pricematrixdf = pricematrixdf[all_cols]
    # PULL BENCH PRICES
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    all_bcols = ['date', benchticker]
    benchpricematrixdf = benchpricematrixdf[all_bcols]
    # JOIN
    benchpricematrixdf = benchpricematrixdf.join(pricematrixdf.set_index('date'), how="left", on="date")

    allperiodcols = [f'Period {period[0]}: {period[1][0]} TO {period[1][1]}' for period in enumerate(all_periods)]
    # for each period RUN MULTIPROCESSOR
    targetvars = (latestdate, allexistingstocks, benchticker, period_dump, benchpricematrixdf)
    multiprocessorshell(period_dump, period_cruncher, all_periods, 'yes', targetvars, chunksize)
    # join perfdfs to mastertallydfs
    for child in period_dump.iterdir():
        with open(child, "rb") as targetfile:
            perfdf = pkl.load(targetfile)
        mastertallydf = mastertallydf.join(perfdf.set_index('stock'), how="left", on="stock")

    # reorder columns
    mastertallydf = mastertallydf[['stock'] + allperiodcols]
    # calculate number periods beat market
    mastertallydf['num_mktbeats'] = mastertallydf[allperiodcols].applymap(lambda x: 1 if x > 0 else 0).sum(axis=1)

    # calculate avg margin
    if avg_type == 'mean':
        mastertallydf[f'{avg_type}_margin'] = mastertallydf[allperiodcols].mean(axis=1)
    elif avg_type == 'median':
        mastertallydf[f'{avg_type}_margin'] = mastertallydf[allperiodcols].median(axis=1)
    elif avg_type == 'avg':
        mastertallydf['mean_margin'] = mastertallydf[allperiodcols].mean(axis=1)
        mastertallydf['median_margin'] = mastertallydf[allperiodcols].median(axis=1)
        mastertallydf[f'{avg_type}_margin'] = mastertallydf[['mean_margin', 'median_margin']].mean(axis=1)

    # calculate margin deviation
    if dev_type == 'std':
        mastertallydf[f'{dev_type}_margin'] = mastertallydf[allperiodcols].std(axis=1)
    elif dev_type == 'mad':
        mastertallydf[f'{dev_type}_margin'] = mastertallydf[allperiodcols].mad(axis=1)
    elif dev_type == 'dev':
        mastertallydf['std_margin'] = mastertallydf[allperiodcols].std(axis=1)
        mastertallydf['mad_margin'] = mastertallydf[allperiodcols].mad(axis=1)
        mastertallydf[f'{dev_type}_margin'] = mastertallydf[['std_margin', 'mad_margin']].mean(axis=1)

    # rank
    sumcols = []
    trimcols = ['stock']
    weight_total = 0
    for metricname in [f'{avg_type}_margin', f'{dev_type}_margin', 'num_mktbeats']:
        # set metricweights
        if metricname == f'{avg_type}_margin':
            metricweight = avgmarginweight
        elif metricname == f'{dev_type}_margin':
            metricweight = devmarginweight
        elif metricname == 'num_mktbeats':
            metricweight = num_mktbeatweight
        # RANK METRIC DATA COLUMN
        rankcolname = f'RANK_{metricname} (w={metricweight})'
        # SET METRIC COLUMN RANK DIRECTION
        if metricname == f'{dev_type}_margin':
            rankdirection = 1
        else:
            rankdirection = 0
        if rankmeth == 'minmax':
            mastertallydf[rankcolname] = mmcalibrated(mastertallydf[metricname].to_numpy(), rankdirection, rankregime)
        elif rankmeth == 'standard':
            mastertallydf[rankcolname] = mastertallydf[metricname].rank(ascending=rankdirection)
        # GET EACH RANKCOLUMN'S WEIGHTED RANK VALUE
        wrankcolname = f'w_{rankcolname}'
        mastertallydf[wrankcolname] = (mastertallydf[rankcolname] * metricweight)
        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wrankcolname)
        # ADD WEIGHT TO WEIGHT TOTAL
        weight_total += metricweight
        # KEEP TRACK OF COLNAMES FOR TRIMMED VERSION OF FINAL DF
        trimcols = trimcols + [metricname, rankcolname, wrankcolname]

    # sum weighted rankcols
    masterwrankcolname = f'MASTER WEIGHTED RANK {weight_total}'
    mastertallydf[masterwrankcolname] = mastertallydf[sumcols].sum(axis=1, min_count=len(sumcols))
    # rank overall weighted rankcol
    if rankmeth == 'minmax':
        if rankregime == '1isbest':
            finalrankascend = 0
        elif rankregime == '0isbest':
            finalrankascend = 1
    elif rankmeth == 'standard':
        finalrankascend = 1
    finalrankcolname = f'MASTER FINAL RANK as of {end_date}'
    mastertallydf[finalrankcolname] = mastertallydf[masterwrankcolname].rank(ascending=finalrankascend)
    trimcols = trimcols + [masterwrankcolname, finalrankcolname]

    # RE-SORT AND RE-INDEX
    mastertallydf.sort_values(ascending=True, by=[finalrankcolname], inplace=True)
    mastertallydf.reset_index(drop=True, inplace=True)

    # save
    savefilename = f'beststreaks_{beg_date}_to_{end_date}'
    savetopkl(savefilename, savedir, mastertallydf)
    # trim out periods cols for final df
    if verbosefile == 'no':
        mastertallydf = mastertallydf[trimcols]
    mastertallydf.to_csv(index=False, path_or_buf=savedir / f"{savefilename}.csv")

    # report results
    if verbose == 'verbose':
        print(f'All of the following stocks existed from {beg_date} to {end_date}:')
        print(f'{allexistingstocks}')
        print(f'From {beg_date} to {end_date}, there were {len(all_periods)} {periodlen}-day periods.')
        print(f'This is how many periods each stock beat {benchticker}:')
        print(mastertallydf[['stock', 'num_mktbeats']])
        print(f'Stocks were ranked by weighing the following two factors equally: (1) the number of periods it beat {benchticker} and (2) the {avg_type} amount by which the stock beat/lost against {benchticker}.  The following ranking resulted:')
        print(mastertallydf[['stock',  'rank_num_mktbeats', f'rank_{avg_type}_margin', 'avgrank', 'finalrank']])
    return mastertallydf
