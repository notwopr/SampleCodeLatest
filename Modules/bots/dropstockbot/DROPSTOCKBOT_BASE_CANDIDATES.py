"""
Title: DROP STOCK BOT BASE - CANDIDATES
Date Started: Dec 10, 2020
Version: 1.10
Version Start: Aug 15, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Tells you whether to drop a stock based on the current day of the investing period you are in. Uses findings from pulloutbot data.
Versions:
1.1: modified order of operations to reduce memory usage.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from growthcalcbot import removeleadingzeroprices


# get list of candidate stocks who fit required candidate profile conditions set
def getcandidateslist_single(pricematrixdf, benchpricematrixdf, existpool, existdate, interim_date, benchgain_curr, candidate_profile):
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    all_cols = ['date'] + existpool
    pricematrixdf = pricematrixdf[all_cols]
    # SLICE OUT DATE RANGE REQUESTED
    pricematrixdf = pricematrixdf.loc[(pricematrixdf['date'] >= existdate) & (pricematrixdf['date'] <= interim_date)]
    # RESET INDEX
    pricematrixdf.reset_index(drop=True, inplace=True)
    # remove leading zeroes from raw prices
    pricematrixdf = removeleadingzeroprices(pricematrixdf, existpool)
    # REMOVE EVERY ROW EXCEPT FIRST AND LAST
    pricedf = pricematrixdf.copy()
    pricedf = pricedf.iloc[[0, -1], :]
    pricedf.reset_index(drop=True, inplace=True)
    # CALCULATE GAIN OVER THE TIME PERIOD
    pricedf[existpool] = pricedf[existpool].pct_change(periods=1, fill_method='ffill')
    currpool = existpool
    # FILTER OUT STOCKS THAT DONT MEET GROWTH_CURR CANDIDATE PROFILE
    if 'growth_curr' in candidate_profile.keys():
        objtestlist = ((pricedf.iloc[[-1], 1:] < candidate_profile['growth_curr']+candidate_profile['growth_err']) & (pricedf.iloc[[-1], 1:] > candidate_profile['growth_curr']-candidate_profile['growth_err'])).loc[1]
        filterednames = objtestlist[objtestlist==True].index.tolist()
        pricedf = pricedf[['date']+filterednames]
        currpool = filterednames
    # FILTER OUT STOCKS THAT DONT MEET MARGIN_CURR CANDIDATE PROFILE
    if 'margin_curr' in candidate_profile.keys():
        # GET MARGINAL GAINS
        pricedf[currpool] = pricedf[currpool] - benchgain_curr
        objtestlist = ((pricedf.iloc[[-1], 1:] < candidate_profile['margin_curr']+candidate_profile['margin_err']) & (pricedf.iloc[[-1], 1:] > candidate_profile['margin_curr']-candidate_profile['margin_err'])).loc[1]
        filterednames = objtestlist[objtestlist==True].index.tolist()
        pricedf = pricedf[['date']+filterednames]
        currpool = filterednames
    # FILTER OUT STOCKS THAT DONT MEET BEATPCT CANDIDATE PROFILE
    if 'beatpct_curr' in candidate_profile.keys():
        # JOIN BENCH PRICES
        all_bcols = ['date', candidate_profile['benchticker']]
        benchpricematrixdf = benchpricematrixdf[all_bcols]
        pricematrixdf = pricematrixdf.join(benchpricematrixdf.set_index('date'), how="left", on="date")
        # remove leading zeroes from raw prices
        alltickers = currpool + [candidate_profile['benchticker']]
        pricematrixdf = removeleadingzeroprices(pricematrixdf, alltickers)
        # remove filtered stocks
        all_cols = ['date'] + currpool + [candidate_profile['benchticker']]
        pricematrixdf = pricematrixdf[all_cols]
        # NORMALIZE EACH PRICE CURVE
        alltickers = currpool + [candidate_profile['benchticker']]
        firstp = pricematrixdf.loc[0, alltickers]
        pricematrixdf[alltickers] = (pricematrixdf[alltickers] - firstp) / firstp
        # convert normprices to boolean whether it beat or did not beat market
        pricematrixdf[currpool] = pricematrixdf[currpool].apply(lambda x: x > pricematrixdf[candidate_profile['benchticker']])
        # remove first row, remove benchmark and date cols
        pricematrixdf = pricematrixdf.iloc[1:][currpool]
        # calculate beatpcts
        beatpcts = pricematrixdf[currpool].mean(axis=0)
        # filter out those not in qualification range
        objtestlist = beatpcts[(beatpcts > candidate_profile['beatpct_curr']-candidate_profile['beatpct_err']) & (beatpcts < candidate_profile['beatpct_curr']+candidate_profile['beatpct_err'])]
        filterednames = objtestlist.index.tolist()
        currpool = filterednames
    # isolate list of stock names
    candidatestocks = currpool
    return candidatestocks
