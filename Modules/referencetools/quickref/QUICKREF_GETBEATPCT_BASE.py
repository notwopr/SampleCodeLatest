"""
Title: GET BEATPCT BOT BASE
Date Started: Dec 12, 2020
Version: 1.00
Version Start: Dec 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given list of stocks and a benchmark and investment period, return the list with their beatpct against the benchmark. Beatpct is the proportion of days the stock's normalized graph exceeded the benchmark's.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from filelocations import readpkl
from UPDATEPRICEDATA_FILELOCATIONS import PRICES

from growthcalcbot import removeleadingzeroprices


# CREATES DF OF BENCH AND PORTFOLIO NORMALIZED PRICES
def getnormprices(pricematrixdf, benchpricematrixdf, portfolio, benchticker, beg_date, end_date):
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    all_cols = ['date'] + portfolio
    nonbenchsliced = pricematrixdf[all_cols].copy()
    # PULL BENCH PRICES
    all_bcols = ['date', benchticker]
    benchsliced = benchpricematrixdf[all_bcols].copy()
    # JOIN
    benchsliced = benchsliced.join(nonbenchsliced.set_index('date'), how="left", on="date")
    # SLICE OUT DATE RANGE REQUESTED
    benchsliced = benchsliced.loc[(benchsliced['date'] >= beg_date) & (benchsliced['date'] <= end_date)].copy()
    # RESET INDEX
    benchsliced.reset_index(drop=True, inplace=True)
    # remove leading zeroes from raw prices
    alltickers = portfolio + [benchticker]
    benchsliced = removeleadingzeroprices(benchsliced, alltickers)
    # NORMALIZE EACH PRICE CURVE
    firstp = benchsliced.loc[0, alltickers]
    benchsliced[alltickers] = (benchsliced[alltickers] - firstp) / firstp
    return benchsliced


# clean normpricedf
def cleandf(normpricesdf, startpool):
    # remove first row, remove benchmark and date cols
    normpricesdf = normpricesdf.iloc[1:][startpool]
    # add day column
    normpricesdf['testday'] = normpricesdf.index
    # reorder columns
    normpricesdf = normpricesdf[['testday']+startpool]
    # reset index
    normpricesdf.reset_index(inplace=True, drop=True)
    return normpricesdf


# download all npdf data
def getbeatpct(global_params):
    # load price matrices into RAM
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    # get df of normalized bench and pool prices
    normpricesdf = getnormprices(pricematrixdf, benchpricematrixdf, global_params['portfolio'], global_params['benchticker'], global_params['investstart'], global_params['investend'])
    if global_params['verbose'] == 'verbose':
        print(normpricesdf)
    # convert normprices to boolean whether it beat or did not beat market
    normpricesdf[global_params['portfolio']] = normpricesdf[global_params['portfolio']].apply(lambda x: x > normpricesdf[global_params['benchticker']])
    if global_params['verbose'] == 'verbose':
        print(normpricesdf)
    # clean df
    normpricesdf = cleandf(normpricesdf, global_params['portfolio'])
    if global_params['verbose'] == 'verbose':
        print(normpricesdf)
    beatpcts = normpricesdf[global_params['portfolio']].mean(axis=0)
    if global_params['verbose'] == 'verbose':
        print(beatpcts)
    # convert to df
    beatpctdf = beatpcts.to_frame()
    # reset index
    beatpctdf.reset_index(inplace=True)
    # change colname
    beatpctdf.rename(columns={'index': 'TICKER', 0: 'Current Beatpct'}, inplace=True)
    beatpctdf.reset_index(inplace=True, drop=True)
    if global_params['verbose'] == 'verbose':
        print(beatpctdf)
    # sort by beatpct
    beatpctdf.sort_values(ascending=False, by='Current Beatpct', inplace=True)
    beatpctdf.reset_index(drop=True, inplace=True)
    if global_params['verbose'] == 'verbose':
        print(beatpctdf)
    return beatpctdf
