"""
Title: FILTER AND LAYER - WINRATE RANKER SUBMETHOD
Date Started: May 24, 2020
Version: 2.00
Version Start: July 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Rank stocks according to how well their average win_len growthrates rank against all other stocks, for every win_len available for each stock.

VERSION NOTES
1.01: Optimize by using map and numpy arrays.
1.02: Remove exceess age data, simplify labels.
1.03: Update for lookback options.
1.04: Split functions into mean and median and std and mad respectively.
1.05: Use oldbareminraw graph instead of bareminraw graph.
1.06: Add smooth and squeeze versions.
2.00: Removed smooth and squeeze versions.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
from functools import partial
from multiprocessing import Pool
import datetime as dt
from pathlib import Path
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
from scipy import stats
#   LOCAL APPLICATION IMPORTS
from Modules.price_history import grabsinglehistory
from Modules.price_history_fillgaps import fill_gaps2
from file_functions import savetopkl
from Modules.file_tests import checknum
from Modules.price_calib_cruncher import baremin_cruncher, baremax_cruncher
from newbacktest.ingredients_funclib.STRATTEST_FUNCBASE import priceslicer
from Modules.ranking_calib import mmcalibrated, mmcalibrated_nan
from file_functions import join_str
from file_hierarchy import DirPaths, FileNames
from machinesettings import _machine

# BELUGA TO BELUGA 2.0 CORRECTIONS
daterangedb_source = Path(join_str([DirPaths().date_results, f'{FileNames().fn_daterangedb}.pkl']))
computerobject = _machine
oldbaremin_cruncher = baremin_cruncher


def winrate_cruncher(array, stat_type):
    if stat_type == 'mean':
        answer = np.mean(array)
    elif stat_type == 'median':
        answer = np.median(array)
    elif stat_type == 'avg':
        answer = np.mean([np.mean(array), np.median(array)])
    elif stat_type == 'std':
        answer = np.std(array)
    elif stat_type == 'mad':
        answer = stats.median_abs_deviation(array)
    elif stat_type == 'dev':
        answer = np.mean([np.std(array), stats.median_abs_deviation(array)])
    return answer


def winrate_summary_single(winratemetricitem, destfolder, beg_date, end_date, metcolname, stock):
    # GET PRICES
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(drop=True, inplace=True)
    # SLICE IF LOOK_BACK SETTING EXISTS
    look_backval = winratemetricitem['look_back']
    if look_backval != 0:
        prices = priceslicer(prices, look_backval)
    # SET SOURCECOL
    if winratemetricitem['sourcetype'] == 'rawprice':
        sourcecolname = stock
    elif winratemetricitem['sourcetype'] == 'oldbareminraw':
        prices['oldbareminraw'] = np.array(oldbaremin_cruncher(prices[stock].tolist()))
        sourcecolname = 'oldbareminraw'
    elif winratemetricitem['sourcetype'] == 'baremaxraw':
        prices['baremaxraw'] = np.array(baremax_cruncher(prices[stock].tolist()))
        sourcecolname = 'baremaxraw'
    elif winratemetricitem['sourcetype'] == 'trueline':
        prices['oldbareminraw'] = np.array(oldbaremin_cruncher(prices[stock].tolist()))
        prices['baremaxraw'] = np.array(baremax_cruncher(prices[stock].tolist()))
        prices['trueline'] = ((prices['baremaxraw'] - prices['oldbareminraw']) / 2) + prices['oldbareminraw']
        sourcecolname = 'trueline'
    elif winratemetricitem['sourcetype'] == 'straight':
        age = len(prices) - 1
        price_start = prices.iloc[0][stock]
        price_end = prices.iloc[-1][stock]
        slope = (price_end - price_start) / age
        prices['straight'] = [(slope * x) + price_start for x in range(age + 1)]
        sourcecolname = 'straight'
    # GET WIN VALUES
    resultcolname = f'winrate_{winratemetricitem["sourcetype"]}_{winratemetricitem["stat_type"]}'
    if winratemetricitem['winlen_ceiling'] != '':
        prices[resultcolname] = prices[sourcecolname].index.map(lambda x: winrate_cruncher(prices[sourcecolname].pct_change(periods=x, fill_method='ffill').dropna().to_numpy(), winratemetricitem['stat_type']) if winratemetricitem['winlen_ceiling'] > x > 0 else None)
    else:
        prices[resultcolname] = prices[sourcecolname].index.map(lambda x: winrate_cruncher(prices[sourcecolname].pct_change(periods=x, fill_method='ffill').dropna().to_numpy(), winratemetricitem['stat_type']) if x > 0 else None)
    # CLEAN UP DF
    winratedf = prices[[resultcolname]].copy()
    winratedf.rename(columns={resultcolname: stock}, inplace=True)
    winratedf = winratedf.loc[1:]
    winratedf.reset_index(drop=True, inplace=True)
    # SAVE TO FILE
    filename = f"{stock}_{resultcolname}_winratesummary"
    savetopkl(filename, destfolder, winratedf)


# DOWNLOAD ALL
def winrateranker(metcolname, winratemetricitem, ranksfolder, resultfolder, beg_date, end_date, tickerlist, rankmeth, rankregime, savemode):

    # RUN MULTIPROCESSOR
    fn = partial(winrate_summary_single, winratemetricitem, resultfolder, beg_date, end_date, metcolname)
    pool = Pool(processes=computerobject.use_cores)
    pool.map(fn, tickerlist, 1)
    pool.close()
    pool.join()

    # WAIT FOR ALL FILES TO DOWNLOAD
    correct = len(tickerlist)
    downloadfinish = checknum(resultfolder, correct, '')
    while downloadfinish is False:
        downloadfinish = checknum(resultfolder, correct, '')

    # CREATE MASTER DATAFRAME
    # find earliest and latest date available
    with open(daterangedb_source, "rb") as targetfile:
        daterangedb = pkl.load(targetfile)
    latestdate = end_date
    if beg_date != '':
        firstdate = beg_date
    else:
        firstdate_dateobj = daterangedb['first_date'].apply(lambda x: dt.date.fromisoformat(x))
        firstdates = firstdate_dateobj.tolist()
        firstdate = str(np.min(firstdates))
    # calculate number of days from first to last
    maxspan = (dt.date.fromisoformat(latestdate) - dt.date.fromisoformat(firstdate)).days
    # create list of all possible spans
    allspans_list = [item + 1 for item in range(maxspan)]
    masterdf = pd.DataFrame(data={'winlen': allspans_list})

    # GET RANKS
    # append each dataframe from folder to masterdf
    for child in resultfolder.iterdir():
        with open(child, "rb") as targetfile:
            prepdf = pkl.load(targetfile)
        masterdf = masterdf.join(prepdf, how="left")
    # save unconverted masterfile
    #rawfilename = 'unconvertedwinratevalues'
    #masterdf.to_csv(index=False, path_or_buf=ranksfolder / f"{rawfilename}.csv")
    # replace winrate values with rank values
    if winratemetricitem['rankmeth'] == 'standard':
        masterdf[tickerlist] = masterdf[tickerlist].rank(ascending=winratemetricitem['rawvalrankdirection'], axis=1)
    elif winratemetricitem['rankmeth'] == 'minmax':
        masterdf[tickerlist] = np.apply_along_axis(mmcalibrated, 1, masterdf[tickerlist].to_numpy(), *(winratemetricitem['rawvalrankdirection'], winratemetricitem['rankregime']))
    elif winratemetricitem['rankmeth'] == 'minmax_nan':
        masterdf[tickerlist] = np.apply_along_axis(mmcalibrated_nan, 1, masterdf[tickerlist].to_numpy(), *(winratemetricitem['rawvalrankdirection'], winratemetricitem['rankregime']))
    #masterdf.to_csv(index=False, path_or_buf=ranksfolder / "CONVERTED.csv")
    # get average ranking for each column
    final_results = masterdf[tickerlist].mean(axis=0)
    finaldf = pd.DataFrame(data=final_results)
    # add index column
    finaldf.reset_index(inplace=True)
    # rename column headers
    finaldf.rename(columns={'index': 'stock', 0: metcolname}, inplace=True)
    # re-sort and re-index
    finaldf.reset_index(drop=True, inplace=True)

    # ARCHIVE TO FILE
    filename = f"{metcolname}_ranks_as_of_{end_date}"
    if savemode == 'pkl':
        savetopkl(filename, ranksfolder, finaldf)
    elif savemode == 'csv':
        finaldf.to_csv(index=False, path_or_buf=ranksfolder / f"{filename}.csv")
    return finaldf
