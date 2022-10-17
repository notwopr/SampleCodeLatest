"""
Title: PRICE PROJECTOR - BASE
Date Started: Oct 27, 2020
Version: 1.0
Version Start: Oct 27, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Returns pricedf with projected price col.

VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
import datetime as dt
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize, Bounds, brute
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from computersettings import computerobject
from filetests import checknum
from filelocations import savetopkl, buildfolders_regime_testrun
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher


def avg_geometricrate(arr, x, avgtype):
    arr = ((arr+1) ** (1 / x)) - 1
    if avgtype == 'mean':
        answer = np.mean(arr)
    elif avgtype == 'median':
        answer = np.median(arr)
    elif avgtype == 'composite':
        answer = np.mean([np.mean(arr), np.median(arr)])
    return answer


# get projected daily percentage change
def getprices(stock, beg_date, end_date, focuscol):
    # get prices
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(drop=True, inplace=True)
    # create focuscol
    if focuscol == 'oldbareminraw' or focuscol == 'baremaxraw' or focuscol == 'trueline':
        allprices = prices[stock].tolist()
        oldbareminrawpricelist = oldbaremin_cruncher(allprices)
        prices['oldbareminraw'] = np.array(oldbareminrawpricelist)
        if focuscol == 'baremaxraw' or focuscol == 'trueline':
            baremaxrawpricelist = baremax_cruncher(allprices)
            prices['baremaxraw'] = np.array(baremaxrawpricelist)
            if focuscol == 'trueline':
                prices['trueline'] = ((prices['baremaxraw'] - prices['oldbareminraw']) / 2) + prices['oldbareminraw']
    return prices


# get projected daily percentage change given price history
def projected_dpc(prices, focuscol, avgtype, projtype):
    # GET WIN VALUES
    if projtype == '1day':
        geometricrates = prices[focuscol].pct_change(periods=1, fill_method='ffill').dropna().to_numpy()
    elif projtype == 'slopescore':
        age = len(prices) - 1
        firstp = prices.iloc[0][focuscol].item()
        lastp = prices.iloc[-1][focuscol].item()
        geometricrates = [((lastp/firstp) ** (1 / age)) - 1]
    elif type(projtype) == tuple:
        geometricrates = (prices[focuscol].index.map(lambda x: avg_geometricrate(prices[focuscol].pct_change(periods=x, fill_method='ffill').dropna().to_numpy(), x, avgtype) if projtype[1] > x > projtype[0] else None)).dropna().to_numpy()
    elif projtype == 'full':
        geometricrates = (prices[focuscol].index.map(lambda x: avg_geometricrate(prices[focuscol].pct_change(periods=x, fill_method='ffill').dropna().to_numpy(), x, avgtype) if x > 0 else None)).dropna().to_numpy()
    if avgtype == 'mean':
        projdpc = np.mean(geometricrates)
    elif avgtype == 'median':
        projdpc = np.median(geometricrates)
    elif avgtype == 'composite':
        projdpc = np.mean([np.mean(geometricrates), np.median(geometricrates)])
    return projdpc


# price slicer
def priceslicer(prices, beg_date, end_date):
    # slice prices to date range requested
    if beg_date == '' and end_date == '':
        prices = prices
    else:
        if end_date != '':
            prices = prices[prices['date'] <= end_date]
        if beg_date != '':
            prices = prices[prices['date'] >= beg_date]
        prices.reset_index(drop=True, inplace=True)
    return prices


# get projected pricecol given price history and projdpc
def projpricecol(prices, focuscol, projdpc, projdpc_colname):
    firstp = prices.loc[0][focuscol].item()
    prices[projdpc_colname] = prices.index.map(lambda x: firstp * (1 + projdpc) ** x)
    return prices


# gives projdpc inaccuracy score based on (1) proportion projprices exceed oldbareminraw (2) proportion projprices != oldbareminraw
def projdpc_inaccuracyscore(dumpfolder, subjectdf, projdpc):
    pricedf = subjectdf.copy()
    # get projprices
    pricedf = projpricecol(pricedf, projdpc)
    '''
    # remove firstrow
    pricedf = pricedf.iloc[1:]
    pricedf.reset_index(drop=True, inplace=True)
    # calc proportion of projected prices that exceed oldbareminraw prices
    ltprojpct = (pricedf['oldbareminraw'] < pricedf['projprices']).mean()
    # calc proportion of projected prices that do not equal oldbareminraw prices
    dneprojpct = (pricedf['oldbareminraw'] != pricedf['projprices']).mean()
    # return qualityscore
    score = np.mean([ltprojpct, dneprojpct])
    print(f'For projdpc {projdpc}: exceedscore:{ltprojpct} | unequalscore: {dneprojpct}')
    '''
    #score = (abs(pricedf['oldbareminraw'] - pricedf['projprices']) / pricedf['oldbareminraw']).mean()
    score = (abs(pricedf['oldbareminraw'] - pricedf['projprices'])).mean()
    # save score
    summary = {'projdpc': projdpc, 'inaccuracyscore': score}
    savetopkl(f'projdpcinaccscore_{projdpc}', dumpfolder, summary)
    return score


# optimizer to find best projectdpc
def bestprojdpc(rootdir, global_params, stock):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    pricedf = getfulloldbareminrawprices(stock)
    # for each sample projdpc
    iterarr = np.arange(global_params['lbound'], global_params['ubound'], global_params['step'])

    # run multiprocessor
    fn = partial(projdpc_inaccuracyscore, testrunparent, pricedf)
    pool = Pool(processes=computerobject.use_cores)
    pool.map(fn, iterarr, 1)
    pool.close()
    pool.join()

    # wait for all files to download
    correct = len(iterarr)
    downloadfinish = checknum(testrunparent, correct, '')
    while downloadfinish is False:
        downloadfinish = checknum(testrunparent, correct, '')
    # construct resultdf
    table_results = []
    for child in testrunparent.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    resultdf = pd.DataFrame(data=table_results)
    # sort by score
    resultdf.sort_values(ascending=True, by=['inaccuracyscore'], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    print(resultdf)
    bestprojdpc = resultdf.loc[0]['projdpc'].item()
    print(f'Best projdpc is {bestprojdpc}')
    return bestprojdpc


# find date that is closest to the bottom right corner of graph
def getelbowdate(stock, beg_date, end_date, focuscol):
    prices = getprices(stock, beg_date, end_date, focuscol)
    br_x = len(prices) - 1
    br_y = prices[stock].min().item()
    y_range = prices[stock].max().item() - br_y
    prices['dist_to_br'] = prices.index.map(lambda x: ((((br_x - x) / br_x) ** 2) + (((prices.loc[x][focuscol].item() - br_y) / y_range) ** 2)) ** (1/2))
    # sort
    prices.sort_values(ascending=True, by=['dist_to_br'], inplace=True)
    prices.reset_index(drop=True, inplace=True)
    # return elbowdate
    elbowdate = prices.loc[0]['date'].date()
    return elbowdate


# highlight elbowdate in graph
def highlight_elbow(prices, stock, beg_date, end_date, focuscol):
    elbowdate = getelbowdate(stock, beg_date, end_date, focuscol)
    prices['elbow'] = prices.index.map(lambda x: prices.loc[x][focuscol].item() if prices.loc[x]['date'].date() == elbowdate else 0)
    return prices


# add dist_to_br col to pricedf
def getdist_to_br(prices, focuscol):
    br_x = len(prices) - 1
    br_y = prices[focuscol].min().item()
    y_range = prices[focuscol].max().item() - br_y
    prices['dist_to_br'] = prices.index.map(lambda x: ((((br_x - x) / br_x) ** 2) + (((prices.loc[x][focuscol].item() - br_y) / y_range) ** 2)) ** (1/2))
    return prices


# get elbow projdpc
def getprojdpc_elbow(stock, beg_date, end_date, focuscol, avgtype, projtype):
    # get elbow date
    elbowdate = getelbowdate(stock, beg_date, end_date, focuscol)
    print(f'elbow date for {beg_date} to {end_date}: {elbowdate}')
    # get prices up to elbow date
    prices = getprices(stock, beg_date, str(elbowdate), focuscol)
    print(prices)
    # get projdpc from those sliced prices
    projdpc_elbow = projected_dpc(prices, focuscol, avgtype, projtype)
    return projdpc_elbow


# get standard projdpc
def getprojdpc_standard(stock, beg_date, end_date, focuscol, avgtype, projtype):
    # get full prices within date range requested
    prices = getprices(stock, beg_date, end_date, focuscol)
    projdpc_standard = projected_dpc(prices, focuscol, avgtype, projtype)
    return projdpc_standard
