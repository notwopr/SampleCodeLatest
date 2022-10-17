"""
Title: Quick Reference - Portfolio volatility
Date Started: Nov 10, 2021
Version: 1
Version Start: Nov 10, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Calculates the volatility of a given portfolio against a given benchmark for a given date range.

VERSIONS:
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from Modules.price_calib import add_calibratedprices
from file_functions import readpkl
from file_hierarchy import PRICES


# return individual + port price curves + baremaxraw of port prices
def get_portpricecurve(portfolio, beg_date, end_date):
    if len(portfolio) == 1 and portfolio[0] in ["^DJI", "^INX", "^IXIC"]:
        matrixname = "allpricematrix_bench"
    else:
        matrixname = "allpricematrix_common"
    # OPEN PRICE MATRIX
    pricedf = readpkl(matrixname, PRICES)
    # SLICE out other stocks
    pricedf = pricedf[['date'] + portfolio]
    # CHECK TO MAKE SURE NO NANs otherwise quit program
    if pricedf.isnull().values.any() is True:
        print('NANs found, indicating missing prices, suggesting that not all stocks have price data for all dates in the date range.  Revise date range such that all stocks in portfolio have prices for every day spanning the entire range.  It is possible that some stocks have holes in their data, where prices are missing where there should not.  Program exiting.')
        exit()
    # SLICE out other stocks and uncommon dates
    #pricedf = pricedf[portfolio].dropna(how="any")
    # SLICE OUT DATE RANGE REQUESTED
    pricedf = pricedf[(pricedf['date'] <= end_date) & (pricedf['date'] >= beg_date)]
    # reset index
    pricedf.reset_index(inplace=True, drop=True)
    # normalize
    firstp = pricedf.loc[0, portfolio]
    pricedf[portfolio] = pricedf[portfolio] / firstp
    # get portprice column by averaging the normprice cols together
    pricedf['portprices'] = pricedf[portfolio].mean(axis=1)
    # get baremax price for portpricecol
    pricedf = add_calibratedprices(pricedf, ['baremaxraw'], 'portprices')
    return pricedf
