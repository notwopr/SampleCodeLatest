"""
Title: Strattest - General Function Database
Date Started: Dec 20, 2020
Version: 2
Version Start Date: Dec 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: General functions relied upon by Strattester.

Version Notes:
1.01: Added 2018 screener metrics.
1.02: Remove lookback versions from library because duplicative.
2: Remove deprecated functions from old layer and filter backtester.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS


# chop off end of price history given new end date
def priceslicer_shortenend(prices, newend):
    prices = prices[prices['date'] <= newend].copy()
    prices.reset_index(drop=True, inplace=True)
    return prices


# shorten beginning of price history given numdays from last day
def priceslicer(prices, timelimiter):
    lastd = prices.iat[-1, 0]
    firstd = lastd - dt.timedelta(days=timelimiter)
    slicedf = prices[prices['date'] >= firstd].copy()
    slicedf.reset_index(drop=True, inplace=True)
    return slicedf


# GET METCOLNAME
def getmetcolname(metricitem):
    metricname = metricitem['metricname']
    look_backval = metricitem['look_back']
    if look_backval != 0:
        metcolname = f'{metricname}_LB{look_backval}'
    else:
        metcolname = f'{metricname}'
    return metcolname


def cleanchanges(all_changes):
    updated_changes = []
    # REMOVE NANS AND INFS
    for item in all_changes:
        if np.isinf(item) or np.isnan(item):
            updated_changes.append(0)
        else:
            updated_changes.append(item)
    # REMOVE FIRST ENTRY (FIRST ROW)
    updated_changes = updated_changes[1:]
    return updated_changes


def alldiffs(prices, changecol, period):
    changeratedata = prices[changecol].diff(periods=period)
    # CLEAN CHANGES
    all_changes = changeratedata.tolist()
    updated_changes = cleanchanges(all_changes)
    return updated_changes


def allpctchanges_old(prices, changecol, period):
    changeratedata = prices[changecol].pct_change(periods=period, fill_method='ffill')
    # CLEAN CHANGES
    all_changes = changeratedata.tolist()
    updated_changes = cleanchanges(all_changes)
    return updated_changes


# negative changes from A to B uses price of B as denominator, while positive changes use price of A
def newpctchange(prices, changecol, x):
    if (prices[changecol].loc[x] - prices[changecol].loc[x-1]) > 0:
        if prices[changecol].loc[x-1] != 0:
            ans = (prices[changecol].loc[x] - prices[changecol].loc[x-1]) / prices[changecol].loc[x-1]
        else:
            ans = np.inf
    else:
        if prices[changecol].loc[x] != 0:
            ans = (prices[changecol].loc[x] - prices[changecol].loc[x-1]) / prices[changecol].loc[x]
        else:
            ans = np.inf
    return ans


def allpctchanges(prices, changecol, period):
    changeratedata = prices.index.map(lambda x: newpctchange(prices, changecol, x) if x > prices.index[0] else None)
    # CLEAN CHANGES
    all_changes = changeratedata.tolist()
    try:
        updated_changes = cleanchanges(all_changes)
    except TypeError:
        print(changecol)
        print(prices)
    return updated_changes


# returns daily margindpcs
def alldpcmargins(prices, stock, benchmatrixchangesdf, benchticker):
    # join benchmarkdf to pricedf
    # CALCULATE DAILY PRICE CHANGES
    prices[f'dpc_{stock}'] = prices[stock].pct_change(periods=1, fill_method='ffill')
    # ATTACH BENCHMARKDF TO STOCKDF
    prices = prices.join(benchmatrixchangesdf.set_index('date'), how="left", on="date")
    # create margindpccol
    changeratedata = prices[f'dpc_{stock}'] - prices[f'dpc_{benchticker}']
    # CLEAN CHANGES
    all_changes = changeratedata.tolist()
    updated_changes = cleanchanges(all_changes)
    return updated_changes
