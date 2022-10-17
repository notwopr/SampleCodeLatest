"""
Title: Quick Reference
Date Started: Feb 26, 2019
Version: 1.3
Version Start: July 27, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Quickly pull up print out of various functions.

VERSIONS:
1.2:  Add growthrates by X period.  use geometric formula.
1.3: Clean up hadyouhadinvested bot with updated code.
Quick Graph.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
import datetime as dt
#   THIRD PARTY IMPORTS
import numpy as np
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from growthcalcbot import getportfoliopricesdf, getnormpricesdf, getportgrowthrate
from filelocations import readpkl
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES, daterangedb_source
from QUICKREF_GETPRICE_BASE import getsingleprice


# GET PERFORMANCE PROFILE FOR ALL STOCKS IN PORT LIBRARY
def stockrankerdf(allportstocks, startcapital, beg_date, end_date):
    # CONSTRUCT GROWTH DF SHELL
    masterdf = pd.DataFrame(data={
        'STOCK': allportstocks,
        'Start Date': beg_date,
        'End Date': end_date,
        'Starting Capital ($)': round(startcapital / len(allportstocks), 2)
        })
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    all_cols = ['date'] + allportstocks
    sliced = pricematrixdf[all_cols].copy()
    # SLICE OUT DATE RANGE REQUESTED
    sliced = sliced.loc[(sliced['date'] >= beg_date) & (sliced['date'] <= end_date)].copy()
    # RESET INDEX
    sliced.reset_index(drop=True, inplace=True)
    # NORMALIZE EACH PRICE CURVE
    firstp = sliced.loc[0, allportstocks]
    sliced[allportstocks] = round((sliced[allportstocks] - firstp) / firstp, 2)
    # REMOVE EVERY ROW EXCEPT FIRST AND LAST
    sliced = sliced.iloc[[-1], :]
    sliced.reset_index(drop=True, inplace=True)
    finaldf_transposed = sliced.transpose()
    finaldf_transposed.reset_index(inplace=True)
    finaldf_transposed.rename(columns={'index': 'STOCK', 0: 'Gain/Loss Rate (%)'}, inplace=True)
    finaldf_transposed = finaldf_transposed.iloc[1:]
    finaldf_transposed.reset_index(drop=True, inplace=True)
    masterdf = masterdf.join(finaldf_transposed.set_index('STOCK'), how="left", on="STOCK")
    masterdf['Ending Capital ($)'] = (masterdf['Starting Capital ($)'] * (1 + masterdf['Gain/Loss Rate (%)'])).apply(lambda x: round(x, 2))
    masterdf['Difference ($)'] = (masterdf['Ending Capital ($)'] - masterdf['Starting Capital ($)']).apply(lambda x: round(x, 2))
    masterdf['Gain/Loss Rate (%)'] = (masterdf['Gain/Loss Rate (%)'] * 100).apply(lambda x: round(x, 2))
    # sort reset and save
    masterdf.sort_values(ascending=False, by=['Gain/Loss Rate (%)'], inplace=True)
    masterdf.reset_index(drop=True, inplace=True)
    return masterdf


# RETURNS BENCH rate over time period
def getrawbenchrate(beg_date, end_date, benchmark):
    # calculate benchmark growth rate
    beg_price = getsingleprice(benchmark, beg_date)
    end_price = getsingleprice(benchmark, end_date)
    rawbenchrate = (end_price / beg_price) - 1
    return rawbenchrate


# RETURNS STATS IF YOU HAD CHOSEN ONE PORTFOLIO OVER ANOTHER
def hadyouhadinvested(startcapital, beg_date, end_date, portfolio, benchmark):

    # LOAD DATARANGE DB
    with open(daterangedb_source, "rb") as targetfile:
        daterangedb = pkl.load(targetfile)

    # IF NO END DATE GIVEN, SUPPLY LAST AVAILABLE DATE
    if end_date == '':
        # FIND LATEST DATE AVAILABLE
        lastdate_dateobj = daterangedb['last_date'].apply(lambda x: dt.date.fromisoformat(x))
        lastdates = lastdate_dateobj.tolist()
        end_date = str(np.max(lastdates))

    # GET PERFORMANCE PROFILE FOR EACH PORTFOLIO
    # CHECK TO SEE IF EVERY MEMBER EXISTED AT BEGDATE AND DATA AVAILABLE
    for stock in portfolio:
        if stock not in daterangedb['stock'].tolist():
            print(f'{stock} did not exist at the chosen beg_date.  Cannot calculate portfolio performance.  In order for this script to calculate portfolio performance, every stock in the chosen portfolio must have existed during the time period chosen. Exiting...')
            exit()
        else:
            ipodate = daterangedb[daterangedb['stock'] == stock]['first_date'].item()
            if dt.date.fromisoformat(ipodate) > dt.date.fromisoformat(beg_date):
                print(f'{stock} did not exist at the chosen beg_date.  Cannot calculate portfolio performance.  In order for this script to calculate portfolio performance, every stock in the chosen portfolio must have existed during the time period chosen. Exiting...')
                exit()
    # PULL PRICEMATRIX
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    # prep and archive price summaries
    pricesummdf = getportfoliopricesdf(pricematrixdf, portfolio, beg_date, end_date)
    # get normalized prices
    normdf = getnormpricesdf(pricesummdf, portfolio)
    # IF EVERY STOCK IN PORT AVAILABLE, MAKE RANKING
    individstockperfdf = stockrankerdf(portfolio, startcapital, beg_date, end_date)
    print(individstockperfdf)
    print('\n')
    # calc port growth
    portgrowth = getportgrowthrate(normdf, portfolio, 'mean', 'no', 'no', 'no', 1.5)
    # add growth data to final growthdf
    endcapital = round(startcapital * (1 + portgrowth), 2)
    difference = round(endcapital - startcapital, 2)
    rate = round(portgrowth * 100, 2)
    # calculate benchmark growth rate
    rawbenchrate = getrawbenchrate(beg_date, end_date, benchmark)
    benchendcapital = round(startcapital * (1 + rawbenchrate), 2)
    benchdifference = round(benchendcapital - startcapital, 2)
    benchrate = round(rawbenchrate * 100, 2)
    margrate = round(rate - benchrate, 2)
    portdifference = endcapital - benchendcapital
    # REPORT
    print(f'Had you invested in the above portfolio from {beg_date} to {end_date}, your portfolio\'s value would have grown {rate} % from ${startcapital:,} to ${endcapital:,}.  You would have earned ${difference:,}.')
    print(f'In contrast, in that same time period, had you put your money in {benchmark} instead, your portfolio\'s value would have grown {benchrate} % from ${startcapital:,} to ${benchendcapital:,}.  You would have earned ${benchdifference:,}.')
    print(f'Your portfolio therefore experienced a marginal rate over {benchmark} of {round(margrate, 2)} %, a difference of ${round(portdifference, 2):,}.')
    print('\n')
    return endcapital
