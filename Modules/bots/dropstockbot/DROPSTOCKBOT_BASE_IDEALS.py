"""
Title: DROP STOCK BOT BASE - MINGAIN
Date Started: Dec 9, 2020
Version: 1.00
Version Start: Dec 9, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Tells you whether to drop a stock based on the current day of the investing period you are in. Uses findings from pulloutbot data.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from growthcalcbot import removeleadingzeroprices


# get list of ideal stocks
def getidealslist_single(pricematrixdf, existpool, existdate, end_date, benchgain, ideal_profile):
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    all_cols = ['date'] + existpool
    pricedf = pricematrixdf[all_cols].copy()
    # SLICE OUT DATE RANGE REQUESTED
    pricedf = pricedf.loc[(pricedf['date'] >= existdate) & (pricedf['date'] <= end_date)].copy()
    # RESET INDEX
    pricedf.reset_index(drop=True, inplace=True)
    # remove leading zeroes from raw prices
    pricedf = removeleadingzeroprices(pricedf, existpool)
    # REMOVE EVERY ROW EXCEPT FIRST AND LAST
    pricedf = pricedf.iloc[[0, -1], :]
    pricedf.reset_index(drop=True, inplace=True)
    # CALCULATE GAIN OVER THE TIME PERIOD
    pricedf[existpool] = pricedf[existpool].pct_change(periods=1, fill_method='ffill')
    currpool = existpool
    # FILTER OUT STOCKS THAT DONT MEET IDEAL PROFILE
    if 'mktbeater' in ideal_profile.keys():
        objtestlist = (pricedf.iloc[[-1], 1:] > benchgain).loc[1]
        filterednames = objtestlist[objtestlist==True].index.tolist()
        pricedf = pricedf[['date']+filterednames]
        currpool = filterednames
    if 'min_gain' in ideal_profile.keys():
        objtestlist = (pricedf.iloc[[-1], 1:] > ideal_profile['min_gain']).loc[1]
        filterednames = objtestlist[objtestlist==True].index.tolist()
        pricedf = pricedf[['date']+filterednames]
        currpool = filterednames
    if 'min_margin' in ideal_profile.keys():
        # GET MARGINAL GAINS
        pricedf[currpool] = pricedf[currpool] - benchgain
        objtestlist = (pricedf.iloc[[-1], 1:] > ideal_profile['min_margin']).loc[1]
        filterednames = objtestlist[objtestlist==True].index.tolist()
        pricedf = pricedf[['date']+filterednames]
        currpool = filterednames
    # isolate list of stock names
    idealstocks = currpool
    return idealstocks
