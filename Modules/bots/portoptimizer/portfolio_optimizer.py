"""
Title: Portfolio Optimizer
Date Started: May 20, 2020
Version: 1.02
Vers Start Date: June 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Calculates the marginal increase in growth rate against marginal increase in volatility for an additional stock added to a portfolio.

Version Notes:
1.01: Multiprocessor version.
1.02: Optimize Code.
"""

# IMPORT TOOLS
#   Standard library imports
import time
import datetime as dt
from itertools import permutations
import pickle as pkl
import os
from functools import partial
from multiprocessing import Pool
#   Third party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#   Local application imports
from filetests import count_file
from computersettings import computerobject
from filelocations import savetopkl, create_nonexistent_folder, readpkl, buildfolders_parent_cresult_cdump
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source
from timeperiodbot import youngeststockipodate
from BACKTEST_GATHERMETHOD_FILTERANDLAYER_FUNCBASE import cleanchanges
from BACKTEST_GATHERMETHOD_LAYERCAKE_FUNCBASE_RAW import dailyvolscore_single, unifatshell_single
from FINALBAREMINCRUNCHER import oldbaremin_cruncher


def quickaxes1(axe, prices, displaycols):

    graphlines = []
    graphlinenames = []
    for item in displaycols:
        graphlinename = '{}'.format(item)
        graphline, = axe.plot(prices[item], label=graphlinename)
        graphlines.append(graphline)
        graphlinenames.append(graphlinename)
    axe.legend(graphlines, graphlinenames)


# FOR A GIVEN SUBPORTFOLIO, RETURN SUMMARY OF GROWTH AND VOLATILITY VALUES
def growthvolsummarizer(summary, sliced, portslice, volmeth):

    # NORMALIZE EACH PRICE CURVE AND CALCULATE GROWTH OF PORTFOLIO
    growthdf = sliced.copy()
    firstp = growthdf.loc[0, portslice]
    growthdf[portslice] = (growthdf[portslice] - firstp) / firstp
    growthdf['portprices'] = growthdf[portslice].mean(axis=1)
    growth = growthdf.iloc[-1]['portprices']
    summary.update({'portgrowth': growth})

    # CALCULATE VOLATILITY
    volatdf = sliced.copy()
    if volmeth == 'old':
        volatdf[portslice] = volatdf[portslice].pct_change(periods=1, fill_method='ffill')
        volatdf['portdailychanges'] = volatdf[portslice].mean(axis=1)
        all_changes = volatdf['portdailychanges'].tolist()
        updated_changes = cleanchanges(all_changes)
        portvolatility = dailyvolscore_single(updated_changes)
    else:
        # get port prices
        firstp = volatdf.loc[0, portslice]
        volatdf[portslice] = (volatdf[portslice] - firstp) / firstp
        volatdf['portprices'] = volatdf[portslice].mean(axis=1)
        # get oldbareminraw prices
        allprices = volatdf['portprices'].tolist()
        oldbareminrawpricelist = oldbaremin_cruncher(allprices)
        volatdf['oldbareminraw'] = np.array(oldbareminrawpricelist)
        # calc unifat volatility score
        unifatscore_oldbareminrawstraight_mean = unifatshell_single(volatdf, 'straight', 'oldbareminraw', 'mean')
        unifatscore_oldbareminrawstraight_median = unifatshell_single(volatdf, 'straight', 'oldbareminraw', 'median')
        unifatscore_oldbareminrawstraight_std = unifatshell_single(volatdf, 'straight', 'oldbareminraw', 'std')
        unifatscore_oldbareminrawstraight_mad = unifatshell_single(volatdf, 'straight', 'oldbareminraw', 'mad')
        unifatscore_rawoldbareminraw_mean = unifatshell_single(volatdf, 'oldbareminraw', 'portprices', 'mean')
        unifatscore_rawoldbareminraw_median = unifatshell_single(volatdf, 'oldbareminraw', 'portprices', 'median')
        unifatscore_rawoldbareminraw_std = unifatshell_single(volatdf, 'oldbareminraw', 'portprices', 'std')
        unifatscore_rawoldbareminraw_mad = unifatshell_single(volatdf, 'oldbareminraw', 'portprices', 'mad')
        oldbareminrawstraightvolscore = np.mean([unifatscore_oldbareminrawstraight_mean, unifatscore_oldbareminrawstraight_median]) + np.mean([unifatscore_oldbareminrawstraight_std, unifatscore_oldbareminrawstraight_mad])
        rawoldbareminrawvolscore = np.mean([unifatscore_rawoldbareminraw_mean, unifatscore_rawoldbareminraw_median]) + np.mean([unifatscore_rawoldbareminraw_std, unifatscore_rawoldbareminraw_mad])
        portvolatility = np.mean([oldbareminrawstraightvolscore, rawoldbareminrawvolscore])
    summary.update({'portvolatility': portvolatility})
    return summary


# GET PRICEMATRIX OF GIVEN STOCKS AND DATE RANGE
def getbaseportpricedf(portfolio, beg_date, end_date):
    # SET PRICEMATRIX PARAMS
    pricematrix = 'allpricematrix_common'
    pricematrixfolder = PRICES
    pricematrixdf = readpkl(pricematrix, pricematrixfolder)
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    all_cols = ['date'] + portfolio
    sliced = pricematrixdf[all_cols].copy()
    # SLICE OUT DATE RANGE REQUESTED
    sliced = sliced.loc[(sliced['date'] >= beg_date) & (sliced['date'] <= end_date)]
    # RESET INDEX
    sliced.reset_index(drop=True, inplace=True)
    return sliced


# RETURNS SORTED DATAFRAME OF STOCKS AND HOW ITS ADDITION TO THE PORTFOLIO CHANGES OVERALL GROWTH AND VOLATILITY OF THE PORTFOLIO GIVEN A PORTFOLIO AND DATE RANGE
def portfolio_optimizer(plot, beg_date, end_date, portfolio, volmeth):
    all_summaries = []
    for portendindex in range(len(portfolio)):
        portslice = portfolio[:portendindex+1]
        stockadded = portslice[-1]
        summary = {'portsize': len(portslice), 'stockadded': stockadded}
        sliced = getbaseportpricedf(portslice, beg_date, end_date)
        summary = growthvolsummarizer(summary, sliced, portslice, volmeth)
        all_summaries.append(summary)
    summarydf = pd.DataFrame(data=all_summaries)
    # CALCULATE CHANGE IN GROWTH AND VOLATILITY
    summarydf[['d_growth', 'd_volat']] = summarydf[['portgrowth', 'portvolatility']].diff()
    summarydf['dgro - dvol'] = summarydf['d_growth'] - summarydf['d_volat']
    # GRAPH
    if plot == 'yes':
        ax1 = plt.subplot(1, 2, 1)
        displaycols = ['portgrowth', 'd_growth', 'dgro - dvol']
        quickaxes1(ax1, summarydf, displaycols)
        ax2 = plt.subplot(1, 2, 2, sharex=ax1)
        displaycols2 = ['d_volat', 'portvolatility']
        quickaxes1(ax2, summarydf, displaycols2)
        plt.xlabel('Port size')
        plt.show()
    # DROP NAN ROW
    summarydf.dropna(how='any', inplace=True, subset=['dgro - dvol'])
    # SORT BY QUALITY METRIC
    summarydf.sort_values(ascending=False, by=['dgro - dvol'], inplace=True)
    return summarydf


# FOR EACH PERMUTATION OF A GIVEN PORTFOLIO
def permute_subprocess(dumpfolder, plot, beg_date, end_date, volmeth, enum_permute):

    # CONVERT PERMUTE TO LIST
    trialno = enum_permute[0]
    sampleport = list(enum_permute[1])

    # GET SAMPLE DATAFRAME
    summarydf = portfolio_optimizer(plot, beg_date, end_date, sampleport, volmeth)

    # RANK
    rankcolname = f'addrank_trial_{trialno}'
    summarydf[rankcolname] = summarydf['dgro - dvol'].rank(ascending=0)
    summarydf.reset_index(drop=True, inplace=True)

    # MAKE RANK DF
    prepdf = summarydf[['stockadded', rankcolname]].copy()

    # SAVE TO DUMP
    # SEARCH SUBDIR WITH LESS THAN 5000 FILES
    i = 0
    subdirname = 'permutedump_' + str(i)
    subloc = dumpfolder / subdirname
    num_files = count_file(subloc)
    while num_files >= 5000:
        i += 1
        subdirname = 'permutedump_' + str(i)
        subloc = dumpfolder / subdirname
        num_files = count_file(subloc)

    filename = f'{trialno}_permutedf'
    savetopkl(filename, subloc, prepdf)


def permute_cruncher(num_perms, dumpfolder, plot, beg_date, end_date, volmeth, enum_allperms):

    fn = partial(permute_subprocess, dumpfolder, plot, beg_date, end_date, volmeth)
    pool = Pool(processes=computerobject.use_cores)
    pool.map(fn, enum_allperms, 2)
    pool.close()
    pool.join()


# RETURNS RANKED LIST OF STOCKS IN GIVEN PORTFOLIO THAT BEST INCREASE PORTFOLIO GROWTH WHILE DECREASING VOLATILITY PERMUTATION VERSION
def portfolio_optimizer_allpermutations(plot, dumpfolder, resultfolder, beg_date, end_date, volmeth, portfolio):

    # IF NO BEGDATE SET, SET IT AS youngest STOCK (NONINDEX) IPO DATE
    if beg_date == '':
        beg_date = youngeststockipodate(portfolio, daterangedb_source)

    # CREATE MASTER DATAFRAME OBJECT
    masterdf = pd.DataFrame(data={'stockadded': portfolio})

    # GET ALL PERMUTATIONS OF PORTFOLIO
    allperms = list(permutations(portfolio))
    num_perms = len(allperms)

    # CREATE DIRECTORY TREE
    num_subdirs = int(np.ceil(num_perms / 5000))
    for i in range(num_subdirs):
        subdirname = 'permutedump_' + str(i)
        subloc = dumpfolder / subdirname
        create_nonexistent_folder(subloc)

    enum_allperms = enumerate(allperms)
    permute_cruncher(num_perms, dumpfolder, plot, beg_date, end_date, volmeth, enum_allperms)

    # ASSEMBLE DATA
    allrankcols = []
    for root, dirs, files in os.walk(dumpfolder, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            with open(filepath, "rb") as targetfile:
                prepdf = pkl.load(targetfile)

            # KEEP TRACK OF RANKCOLS
            rankcolname = prepdf.columns[-1]
            allrankcols.append(rankcolname)

            # APPEND RANK DF TO MASTER DF
            masterdf = masterdf.join(prepdf.set_index('stockadded'), how="left", on="stockadded")

    # GET AVERAGE RANKING
    masterdf['AVG RANK'] = masterdf[allrankcols].mean(axis=1, skipna=True)

    # GET FINAL RANKING
    masterdf['FINAL RANK'] = masterdf['AVG RANK'].rank(ascending=1)

    # SORT BY FINAL RANK
    masterdf.sort_values(ascending=True, by=['FINAL RANK'], inplace=True)
    masterdf.reset_index(drop=True, inplace=True)

    finaldf = masterdf[['stockadded', 'AVG RANK', 'FINAL RANK']].copy()

    # ARCHIVE TO FILE
    filename = f"portfolio_optimizer_ranks_{beg_date}_to_{end_date}"
    savetopkl(filename, resultfolder, finaldf)
    finaldf.to_csv(index=False, path_or_buf=resultfolder / f"{filename}.csv")

    # REPORT FINDINGS
    print(finaldf)

    return finaldf


# TAKES BASE PORTFOLIO, replaces worst with one from candidates, repeat
def candidate_challenger(plot, testrunparent, baseportfolio, candidatelist, beg_date, end_date, volmeth):
    currentpool = baseportfolio
    testnumber = 1
    for nextstock in candidatelist:
        # BUILD FOLDERS
        cctestrun_parent, cctestrun_results, cctestrun_dump = buildfolders_parent_cresult_cdump(testrunparent, f'cctestrun_{testnumber}')
        rankdf = portfolio_optimizer_allpermutations(plot, cctestrun_dump, cctestrun_results, beg_date, end_date, volmeth, currentpool)
        # GET LAST PLACE STOCK
        lastplace = rankdf.iloc[-1]['stockadded']
        # REMOVE FROM LIST
        currentpool.remove(lastplace)
        # ADD NEXT CANDIDATE
        currentpool.append(nextstock)
        # ADD TESTNUMBER
        testnumber += 1
