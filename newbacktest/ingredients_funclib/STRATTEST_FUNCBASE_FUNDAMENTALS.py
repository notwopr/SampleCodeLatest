"""
Title: Layercake - Function Database - Fundamentals Functions
Date Started: Mar 3, 2021
Version: 1.00
Version Start Date: Mar 3, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Functions to be run on fundamentals data, not price data.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from Modules.price_history import grabsinglehistory_fundies
from Modules.price_history_fillgaps import fill_gaps2


# check if slope is positive
def fundypositiveslope_single(prices, stock, datatype):
    # get startdate
    beg_date = prices['date'].iloc[0]
    # get end date
    end_date = prices['date'].iloc[-1]
    # get fundydf
    if datatype == 'marketcap':
        dftype = 'marketcap'
    else:
        dftype = 'fundies'
    fundydf = grabsinglehistory_fundies(stock, dftype)
    fundydf = fill_gaps2(fundydf, beg_date, end_date)
    fundydf.reset_index(drop=True, inplace=True)
    # check that df is not empty (does not need to be exact range because fundamentals are not daily but quarterly/annually)
    if len(fundydf) != 0:
        firstdatapoint = fundydf.iloc[0][f'{datatype}_{stock}']
        lastdatapoint = fundydf.iloc[-1][f'{datatype}_{stock}']
        positiveslope = lastdatapoint - firstdatapoint
    else:
        positiveslope = None
    return positiveslope


# CURRENT MARKETCAP
def currmarketcap_single(prices, stock):
    currdate = prices['date'].iloc[-1]
    marketcapdf = grabsinglehistory_fundies(stock, 'marketcap')
    marketcapdf = fill_gaps2(marketcapdf, '', currdate)
    marketcapdf.reset_index(drop=True, inplace=True)
    if len(marketcapdf) != 0:
        currmarketcap = marketcapdf[f'marketcap_{stock}'].iloc[-1]
    else:
        currmarketcap = None
    return currmarketcap
