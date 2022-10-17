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
from growthcalcbot import getportfoliopricesdf, getportfoliopricecol, getnormpricesdf, getportgrowthrate
from filelocations import readpkl, savetopkl, buildfolders_singlechild
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES, daterangedb_source
from genericfunctionbot import removedupes
from HADYOUHAD_BASE_CRUNCHER_ALLMETRICVALS import allmetrics_single, rankmetricsdf


# GET PERFORMANCE PROFILE FOR ALL STOCKS IN PORT LIBRARY
def stockrankerdf(allportstocks, startcapital, thisrunparent, beg_date, end_date, portname):
    # CONSTRUCT GROWTH DF SHELL
    masterdf = pd.DataFrame(data={
        'STOCK': allportstocks,
        'Start Date': beg_date,
        'End Date': end_date,
        'Starting Capital ($)': startcapital
        })

    nonbenchstocks = [item for item in allportstocks if item not in ['^DJI', '^INX', '^IXIC']]
    benchstocks = [item for item in allportstocks if item in ['^DJI', '^INX', '^IXIC']]

    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    if len(nonbenchstocks) != 0:
        pricematrixdf = readpkl('allpricematrix_common', PRICES)
        all_cols = ['date'] + nonbenchstocks
        nonbenchsliced = pricematrixdf[all_cols].copy()
    if len(benchstocks) != 0:
        pricematrixdf = readpkl('allpricematrix_bench', PRICES)
        all_cols = ['date'] + benchstocks
        benchsliced = pricematrixdf[all_cols].copy()

    # JOIN SLICED DFS IF TWO EXIST
    if len(nonbenchstocks) != 0 and len(benchstocks) != 0:
        sliced = benchsliced.join(nonbenchsliced.set_index('date'), how="left", on="date")
    elif len(nonbenchstocks) != 0:
        sliced = nonbenchsliced
    elif len(benchstocks) != 0:
        sliced = benchsliced

    # SLICE OUT DATE RANGE REQUESTED
    sliced = sliced.loc[(sliced['date'] >= beg_date) & (sliced['date'] <= end_date)].copy()

    # RESET INDEX
    sliced.reset_index(drop=True, inplace=True)

    # NORMALIZE EACH PRICE CURVE
    firstp = sliced.loc[0, allportstocks]
    sliced[allportstocks] = (sliced[allportstocks] - firstp) / firstp
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
    masterdf['Gain/Loss Rate (%)'] = masterdf['Gain/Loss Rate (%)'] * 100
    # sort reset and save
    masterdf.sort_values(ascending=False, by=['Gain/Loss Rate (%)'], inplace=True)
    masterdf.reset_index(drop=True, inplace=True)
    masterdfname = f'{portname}_allstockcomparisondf'
    masterdf.to_csv(index=False, path_or_buf=thisrunparent / f"{masterdfname}.csv")
    savetopkl(masterdfname, thisrunparent, masterdf)


# GET PERFORMANCE PROFILE FOR EACH PORTFOLIO
def constructgrowthdf(daterangedb, portkeydf, startcapital, thisrunparent, beg_date, end_date, avgmeth, remove_outliers, verbose, plot, strength,  metricpanelscript):
    # build dump folder for portdata
    portdatadump = buildfolders_singlechild(thisrunparent, 'portdatadump')
    # CONSTRUCT GROWTH DF SHELL
    growthdf = pd.DataFrame(['Start Date', 'End Date', 'Starting Capital ($)', 'Ending Capital ($)', 'Difference ($)', 'Gain/Loss Rate (%)'], columns=['CATEGORY'])
    metricsdfdata = []
    # FOR EACH PORTFOLIO IN LIST OF PORTFOLIOS, GET GROWTH DF DATA
    for count in range(len(portkeydf)):
        portname = portkeydf.loc[count]['PORTFOLIO NAME']
        portfolio = portkeydf.loc[count]['CONTENTS']
        # CHECK TO SEE IF EVERY MEMBER EXISTED AT BEGDATE AND DATA AVAILABLE
        portstatus = ''
        for stock in portfolio:
            if stock not in ['^DJI', '^IXIC', '^INX']:
                if stock not in daterangedb['stock'].tolist():
                    portstatus = 'notavailable'
                    print(stock)
                else:
                    ipodate = daterangedb[daterangedb['stock'] == stock]['first_date'].item()
                    if dt.date.fromisoformat(ipodate) > dt.date.fromisoformat(beg_date):
                        portstatus = 'notavailable'
            else:
                portstatus == 'bench'
                break
        # if not, assign nan
        if portstatus == 'notavailable':
            growthdf[portname] = np.array([dt.date.fromisoformat(beg_date), dt.date.fromisoformat(end_date), startcapital, np.nan, np.nan, np.nan])
        else:
            # PULL PRICEMATRIX
            if portname == 'bench' or portname == 'nasdaq' or portname == 'dow' or portname == 'snp':
                pricematrixdf = readpkl('allpricematrix_bench', PRICES)
            else:
                pricematrixdf = readpkl('allpricematrix_common', PRICES)
            # prep and archive price summaries
            pricesummdf = getportfoliopricesdf(pricematrixdf, portfolio, beg_date, end_date)
            portdfname = f'portdata_{portname}'
            pricesummdf.to_csv(index=False, path_or_buf=portdatadump / f"{portdfname}.csv")
            # get normalized prices
            normdf = getnormpricesdf(pricesummdf, portfolio)
            # calc port growth
            portgrowth = getportgrowthrate(normdf, portfolio, avgmeth, remove_outliers, verbose, plot, strength)
            # add growth data to final growthdf
            endcapital = round(startcapital * (1 + portgrowth), 2)
            difference = round(endcapital - startcapital, 2)
            rate = round(portgrowth * 100, 2)
            growthdf[portname] = np.array([dt.date.fromisoformat(beg_date), dt.date.fromisoformat(end_date), startcapital, endcapital, difference, rate])

            # ADD METRICS TO GROWTHDF
            # get portprices
            portprices = getportfoliopricecol(normdf, portfolio, avgmeth)
            # parse metricpanel script
            scriptparams = metricpanelscript['scriptparams']
            # CREATE MASTER SUMMARY
            summary = {'Portfolio': portname}
            # set 'stock' column for allmetrics_single
            portprices.rename(columns={f'portfolioprices_{avgmeth}': f'{portname}'}, inplace=True)
            # get summary of all metric values
            summary = allmetrics_single(portprices, summary, scriptparams, '', '', beg_date, end_date, portname)
            # append summary to growthdf
            metricsdfdata.append(summary)

    # TRANSPOSE DATAFRAME
    growthdf = growthdf.transpose()
    newcolnames = growthdf.iloc[0]
    growthdf.reset_index(inplace=True)
    growthdf.rename(columns=newcolnames, inplace=True)
    growthdf.rename(columns={'index': 'Portfolio'}, inplace=True)
    growthdf = growthdf.iloc[1:]
    growthdf.sort_values(ascending=False, by=['Gain/Loss Rate (%)'], inplace=True)
    growthdf.reset_index(drop=True, inplace=True)
    growthdf = growthdf.join(portkeydf.set_index('PORTFOLIO NAME'), how="left", on="Portfolio")
    growthdf = growthdf[['Portfolio', 'CONTENTS', 'Start Date', 'End Date', 'Starting Capital ($)', 'Ending Capital ($)', 'Difference ($)', 'Gain/Loss Rate (%)']]
    growthdfname = 'growthcomparisondf'
    growthdf.to_csv(index=False, path_or_buf=thisrunparent / f"{growthdfname}.csv")
    savetopkl(growthdfname, thisrunparent, growthdf)

    # CONSTRUCT METRICSDF
    metricsdf = pd.DataFrame(data=metricsdfdata)
    # RANK METRICSDF
    metricsdf = rankmetricsdf(metricsdf, scriptparams)
    metricsdfname = 'metricsdf'
    metricsdf.to_csv(index=False, path_or_buf=thisrunparent / f"{metricsdfname}.csv")


# RETURNS STATS IF YOU HAD CHOSEN ONE PORTFOLIO OVER ANOTHER
def hadyouhadinvested(startcapital, beg_date, end_date, portkeydf, thisrunparent, avgmeth, remove_outliers, verbose, plot, strength, metricpanelscript):

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
    constructgrowthdf(daterangedb, portkeydf, startcapital, thisrunparent, beg_date, end_date, avgmeth, remove_outliers, verbose, plot, strength,  metricpanelscript)

    # GET RANKING OF ALL STOCKS IN THE PORT LIBRARY
    allportstocks = []
    allportlists = portkeydf['CONTENTS'].tolist()
    for portlist in allportlists:
        allportstocks.extend(portlist)
    allportstocks = removedupes(allportstocks)
    # remove stocks that have no data
    allportstocks = [item for item in allportstocks if item in daterangedb['stock'].tolist()]
    stockrankerdf(allportstocks, startcapital, thisrunparent, beg_date, end_date, 'allstocks')

    # GET GROWTH DFS FOR EACH PORTFOLIO IN LIBRARY
    eachportperfdf_dump = buildfolders_singlechild(thisrunparent, 'eachportperfdf')
    for row in portkeydf.iterrows():
        portname = row[1][0]
        portcontents = row[1][1]
        # CHECK TO SEE IF EVERY MEMBER EXISTED AT BEGDATE
        portstatus = ''
        for stock in portcontents:
            if stock not in ['^DJI', '^IXIC', '^INX']:
                allavailablestocks = daterangedb['stock'].tolist()
                if stock not in allavailablestocks:
                    portstatus = 'notavailable'
                else:
                    ipodate = daterangedb[daterangedb['stock'] == stock]['first_date'].item()
                    if dt.date.fromisoformat(ipodate) > dt.date.fromisoformat(beg_date):
                        portstatus = 'notavailable'
            else:
                portstatus == 'bench'
                break
        # IF EVERY STOCK IN PORT AVAILABLE, MAKE RANKING
        if portstatus != 'notavailable':
            stockrankerdf(portcontents, startcapital, eachportperfdf_dump, beg_date, end_date, portname)
