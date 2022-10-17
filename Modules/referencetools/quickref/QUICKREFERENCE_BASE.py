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
import math
#   THIRD PARTY IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from FINALBAREMINCRUNCHER import baremin_cruncher, oldbaremin_cruncher, baremax_cruncher
from growthcalcbot import period_growth_portfolio, period_growth_portfolio_fulldf
from filelocations import readpkl, savetopkl, buildfolders_parent_cresult_cdump, buildfolders_singlechild
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES, daterangedb_source
from genericfunctionbot import removedupes
from filelocations import create_nonexistent_folder
from STRATTEST_FUNCBASE import allpctchanges, alldiffs, getmetcolname
from STRATTEST_SINGLE_BASE_CRUNCHER_ALLMETRICVALS import allmetricval_cruncher
from statresearchbot import stat_profiler


# GET RANKING OF PORTFOLIOS
def finalcomparisondfranks(portkeydf, metricpanel_params, thisrunparent, beg_date, end_date, comparetype):
    listofportnames = portkeydf['portname'].to_list()
    metrics_to_run = metricpanel_params[0]['method_specific_params']['fnlbatches'][0]['batch']
    finaldfdata = []
    for metricitem in metrics_to_run:
        metricname = metricitem['metricname']
        metcolname = getmetcolname(metricitem)
        finaldfrow = {'metric': metcolname}
        for portname in listofportnames:
            # PULL OF PORTFOLIO STAT SUMMARY
            summaryloc = thisrunparent / comparetype / 'resultfiles'
            summaryfn = f'{portname}_statsummdf_beg{beg_date}_end{end_date}'
            portdf = readpkl(summaryfn, summaryloc)
            metricaverage = portdf[portdf['metricname'] == metricname]['stat_mean'].item()
            finaldfrow.update({portname: metricaverage})
        finaldfdata.append(finaldfrow)

    finaldf = pd.DataFrame(data=finaldfdata)
    finaldf_transposed = finaldf.transpose()
    newcolnames = finaldf_transposed.iloc[0]
    finaldf_transposed.reset_index(inplace=True)
    finaldf_transposed.rename(columns=newcolnames, inplace=True)
    finaldf_transposed.rename(columns={'index': 'portfolio'}, inplace=True)
    finaldf_transposed = finaldf_transposed.iloc[1:]
    finaldf_transposed.reset_index(drop=True, inplace=True)
    # RANK DATA
    sumcols = []
    for metricitem in metrics_to_run:

        # DEFINE RANK PARAMS
        metricweight = metricitem['metricweight']
        rankdirection = metricitem['rankascending']
        metricname = metricitem['metricname']
        metcolname = getmetcolname(metricitem)

        # RANK METRIC DATA COLUMN
        rankcolname = f'RANK_{metcolname} (w={metricweight})'
        subjectcolname = metcolname
        finaldf_transposed[rankcolname] = finaldf_transposed[subjectcolname].rank(ascending=rankdirection)

        # GET EACH RANKCOLUMN'S WEIGHTED RANK VALUE
        wrankcolname = f'w_{rankcolname}'
        finaldf_transposed[wrankcolname] = (finaldf_transposed[rankcolname] * metricweight)

        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wrankcolname)

    finaldf_transposed['WEIGHTED LAYER RANK'] = finaldf_transposed[sumcols].sum(axis=1, min_count=len(sumcols))

    finalrankcolname = f'FINAL {comparetype} LAYER RANK as of {end_date}'
    finaldf_transposed[finalrankcolname] = finaldf_transposed['WEIGHTED LAYER RANK'].rank(ascending=1)

    # RE-SORT AND RE-INDEX
    finaldf_transposed.sort_values(ascending=True, by=[finalrankcolname], inplace=True)
    finaldf_transposed.reset_index(drop=True, inplace=True)

    # SAVE RESULTS
    finaldfname = f'{comparetype}_comparisondf'
    finaldf_transposed.to_csv(index=False, path_or_buf=thisrunparent / f"{finaldfname}.csv")
    savetopkl(finaldfname, thisrunparent, finaldf_transposed)
    return finaldf_transposed


# CREATE AND SAVE PORTINDEX TO BLACKBOX
def createportfoliokey(thisrunparent, portfolio_dict, benchportfolio):
    portfoliokeydata = []
    count = 0
    for portname, portfolio in portfolio_dict.items():
        portname = portname
        if portname == '':
            portname = f'port_{count}'
        portfoliokeydata.append({'portname': portname, 'contents': portfolio})
    portkeydf = pd.DataFrame(data=portfoliokeydata)
    portindexname = 'portfoliokey'
    portkeydf.to_csv(index=False, path_or_buf=thisrunparent / F"{portindexname}.csv")
    savetopkl(portindexname, thisrunparent, portkeydf)
    return portkeydf


# RETRIEVES METRICPANEL OF GIVEN PORTFOLIO AND STAT SUMMARY OF EACH METRIC
def getmetricpanelandrangesummary(metricpanelresults, metricpaneldump, beg_date, end_date, metricpanel_params, portname, portfolio):

    # GET METRICPANELDF OF FULL EXTANT POOL
    # collect metrics to run
    metrics_to_run = metricpanel_params[0]['method_specific_params']['fnlbatches'][0]['batch']
    layercakemetrics = [item for item in metrics_to_run if item['metricname'] != 'age']
    # create dump folders
    batchname = portname
    allmetricdataparent, allmetricdataresults, allmetricdatadump = buildfolders_parent_cresult_cdump(metricpaneldump, batchname)
    # get metricdata
    allmetricsdf = allmetricval_cruncher(allmetricdataresults, allmetricdatadump, layercakemetrics, beg_date, end_date, portfolio)

    # REMOVE RANKCOLS
    allmetcolnames = [getmetcolname(metricitem) for metricitem in metrics_to_run]
    keepcols = ['stock', 'age'] + allmetcolnames
    allmetricsdf = allmetricsdf[keepcols]

    # REPLACE METRIC COL WITH PCTRANK COL
    pctrankmetricnames = ['marketbeater', 'winrateranker_mean', 'winrateranker_median', 'winvolranker_std', 'winvolranker_mad']
    pctrankmetricitems = [metricitem for metricitem in metrics_to_run if metricitem['metricname'] in pctrankmetricnames]
    for metricitem in pctrankmetricitems:
        rankdirection = metricitem['rankascending']
        metcolname = getmetcolname(metricitem)
        allmetricsdf[metcolname] = allmetricsdf[metcolname].rank(ascending=rankdirection, pct=True)

    # SAVE METRICDF TO FILE
    formatallmetfn = f'{batchname}_allmetricsdf_beg{beg_date}_end{end_date}'
    savetopkl(formatallmetfn, metricpanelresults, allmetricsdf)
    allmetricsdf.to_csv(index=False, path_or_buf=metricpanelresults / f"{formatallmetfn}.csv")

    # GET RANGES FOR EACH METRIC COLUMN
    rangesummdata = []
    for metricitem in metrics_to_run:
        metricname = metricitem['metricname']
        metcolname = getmetcolname(metricitem)
        metcolseries = allmetricsdf[metcolname].to_numpy()
        statsumm = stat_profiler(metcolseries)
        summdict = {'metricname': metricname}
        summdict.update(statsumm)
        rangesummdata.append(summdict)

    # CREATE DF OF SUMMARY
    mktbeatstatsummdf = pd.DataFrame(data=rangesummdata)

    # SAVE DF TO FILE
    mktbeatsummfn = f'{batchname}_statsummdf_beg{beg_date}_end{end_date}'
    savetopkl(mktbeatsummfn, metricpanelresults, mktbeatstatsummdf)
    mktbeatstatsummdf.to_csv(index=False, path_or_buf=metricpanelresults / f"{mktbeatsummfn}.csv")
    return mktbeatstatsummdf


# GET METRICPANEL FOR EACH PORTFOLIO IN LISTOFPORTFOLIOS
def getmetricpanel_all(portkeydf, thisrunparent, batchname, metricpanel_params, beg_date, end_date):
    for count in range(len(portkeydf)):
        portname = portkeydf.loc[count]['portname'].item()
        portfolio = portkeydf.loc[count]['contents'].item()
        # BUILD METRICPANEL DUMP FOLDERS
        mp_parent, mp_results, mp_dump = buildfolders_parent_cresult_cdump(thisrunparent, batchname)
        # FOR EACH PORTFOLIO GET METRICPANEL AND STAT SUMMARY
        getmetricpanelandrangesummary(mp_results, mp_dump, beg_date, end_date, metricpanel_params, portname, portfolio)


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
def constructgrowthdf(daterangedb, portkeydf, startcapital, thisrunparent, beg_date, end_date):
    # build dump folder for portdata
    portdatadump = buildfolders_singlechild(thisrunparent, 'portdatadump')
    # CONSTRUCT GROWTH DF SHELL
    growthdf = pd.DataFrame(['Start Date', 'End Date', 'Starting Capital ($)', 'Ending Capital ($)', 'Difference ($)', 'Gain/Loss Rate (%)'], columns=['CATEGORY'])
    # FOR EACH PORTFOLIO IN LIST OF PORTFOLIOS, GET GROWTH DF DATA
    for count in range(len(portkeydf)):
        portname = portkeydf.loc[count]['PORTFOLIO NAME']
        portfolio = portkeydf.loc[count]['CONTENTS']
        # CHECK TO SEE IF EVERY MEMBER EXISTED AT BEGDATE
        portstatus = ''
        for stock in portfolio:
            if stock not in ['^DJI', '^IXIC', '^INX']:
                ipodate = daterangedb[daterangedb['stock'] == stock]['first_date'].item()
                if dt.date.fromisoformat(ipodate) > dt.date.fromisoformat(beg_date):
                    portstatus = 'notavailable'
            else:
                portstatus == 'bench'
                break
        if portstatus == 'notavailable':
            growthdf[portname] = np.array([dt.date.fromisoformat(beg_date), dt.date.fromisoformat(end_date), startcapital, np.nan, np.nan, np.nan])
        else:
            # PULL PRICEMATRIX
            if portname == 'bench' or portname == 'nasdaq' or portname == 'dow' or portname == 'snp':
                pricematrixdf = readpkl('allpricematrix_bench', PRICES)
            else:
                pricematrixdf = readpkl('allpricematrix_common', PRICES)
            package = [portfolio, [beg_date, end_date]]
            sliced, portgrowth = period_growth_portfolio_fulldf('mean', 'no', 1.5, '', '', pricematrixdf, package)
            # archive portfoliodata
            portdfname = f'portdata_{portname}'
            sliced.to_csv(index=False, path_or_buf=portdatadump / f"{portdfname}.csv")
            # add growth data to final growthdf
            endcapital = round(startcapital * (1 + portgrowth), 2)
            difference = round(endcapital - startcapital, 2)
            rate = round(portgrowth * 100, 2)
            growthdf[portname] = np.array([dt.date.fromisoformat(beg_date), dt.date.fromisoformat(end_date), startcapital, endcapital, difference, rate])
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


# RETURNS STATS IF YOU HAD CHOSEN ONE PORTFOLIO OVER ANOTHER
def hadyouhadinvested(metric_compare, graphit, verbose, startcapital, beg_date, end_date, portkeydf, thisrunparent, metricpanel_params, pricecalibration):

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
    growthdf = constructgrowthdf(daterangedb, portkeydf, startcapital, thisrunparent, beg_date, end_date)

    # GET RANKING OF ALL STOCKS IN THE PORT LIBRARY
    allportstocks = []
    allportlists = portkeydf['CONTENTS'].tolist()
    for portlist in allportlists:
        allportstocks.extend(portlist)
    allportstocks = removedupes(allportstocks)
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
                ipodate = daterangedb[daterangedb['stock'] == stock]['first_date'].item()
                if dt.date.fromisoformat(ipodate) > dt.date.fromisoformat(beg_date):
                    portstatus = 'notavailable'
            else:
                portstatus == 'bench'
                break
        # IF EVERY STOCK IN PORT AVAILABLE, MAKE RANKING
        if portstatus != 'notavailable':
            stockrankerdf(portcontents, startcapital, eachportperfdf_dump, beg_date, end_date, portname)

    if metric_compare == 'yes':
        # FOR EACH PORTFOLIO GET LIFETIME METRICPANEL AND STAT SUMMARY
        getmetricpanel_all(portkeydf, thisrunparent, 'lifetimemetricpaneldata', metricpanel_params, '', end_date)
        # FOR EACH PORTFOLIO GET TEST PERIOD METRICPANEL AND STAT SUMMARY
        getmetricpanel_all(portkeydf, thisrunparent, 'testperiodmetricpaneldata', metricpanel_params, beg_date, end_date)

        # DRAFT LIFETIME FINAL COMPARISON DF
        lt_finalcompranks = finalcomparisondfranks(portkeydf, metricpanel_params, thisrunparent, beg_date, end_date, 'lifetimemetricpaneldata')
        tp_finalcompranks = finalcomparisondfranks(portkeydf, metricpanel_params, thisrunparent, beg_date, end_date, 'testperiodmetricpaneldata')

    # GRAPH IT
    if graphit == 'yes':
        # GRAPH JUST PORTOFOLIO LINES IN ONE GRAPH
        fig1 = plt.figure()
        axe1 = fig1.add_subplot(111)
        portlines = []
        portlinenames = []
        listofportfolios = portkeydf['CONTENTS'].tolist()
        for portfolio in listofportfolios:

            sliced, stockcols, portcols = getgraphdata(pricecalibration, portfolio, beg_date, end_date)
            quickaxes_portfolios(axe1, sliced, portcols, portfolio, portlines, portlinenames)

        axe1.legend(portlines, portlinenames)
        plt.title('{} to {} {}'.format(beg_date, end_date, pricecalibration))
        plt.show()

        # GRAPH ALL STOCKS AND PORTFOLIOS TOGETHER
        # GET COORDINATES FOR SUBPLOT MATRIX
        num_ports = len(listofportfolios)
        num_rows = int(math.sqrt(num_ports))
        num_cols = math.ceil(num_ports / num_rows)
        strcoord = int(str(num_rows) + str(num_cols))

        # PLOT EACH SUBPLOT
        fig2 = plt.figure()
        count = 1

        # FOR EACH PORTFOLIO, CREATE AXES
        for portfolio in listofportfolios:
            subplotcoord = int(str(strcoord) + str(count))
            axe2 = fig2.add_subplot(subplotcoord)
            sliced, stockcols, portcols = getgraphdata(pricecalibration, portfolio, beg_date, end_date)
            quickaxes(axe2, sliced, stockcols, portcols)
            count += 1

        # DISPLAY GRAPH
        plt.title('{} to {} {}'.format(beg_date, end_date, pricecalibration))
        plt.show()

    # REPORT RESULTS
    if verbose == 'verbose':
        print(growthdf)
        if metric_compare == 'yes':
            print('\n')
            print(lt_finalcompranks)
            print('\n')
            print(tp_finalcompranks)


def createbaremin(sliced, portfolio, nonbenchstocks):
    # CHECK IF PORTCOLS NEEDED
    if len(nonbenchstocks) != 0:
        convertcols = portfolio + ['portprices']
    else:
        convertcols = portfolio
    # CREATE BAREMIN VERSIONS OF SAME
    bareminstock = []
    for item in convertcols:
        rawlist = sliced[item].tolist()
        pricedatalist = baremin_cruncher(rawlist)
        baremincolname = f'baremin {item}'
        sliced[baremincolname] = np.array(pricedatalist)
        if item in portfolio:
            bareminstock.append(baremincolname)
    # CATEGORIZE COLS
    portbaremin = ['baremin portprices']
    portraw = ['portprices']
    return portbaremin, portraw, bareminstock, sliced


def createoldbaremin(sliced, portfolio, nonbenchstocks):
    # CHECK IF PORTCOLS NEEDED
    if len(nonbenchstocks) != 0:
        convertcols = portfolio + ['portprices']
    else:
        convertcols = portfolio
    # CREATE OLDBAREMIN VERSIONS OF SAME
    oldbareminstock = []
    for item in convertcols:
        rawlist = sliced[item].tolist()
        pricedatalist = oldbaremin_cruncher(rawlist)
        oldbaremincolname = f'oldbaremin {item}'
        sliced[oldbaremincolname] = np.array(pricedatalist)
        if item in portfolio:
            oldbareminstock.append(oldbaremincolname)
    # CATEGORIZE COLS
    portoldbaremin = ['oldbaremin portprices']
    portraw = ['portprices']
    return portoldbaremin, portraw, oldbareminstock, sliced


def createbaremax(sliced, portfolio, nonbenchstocks):
    # CHECK IF PORTCOLS NEEDED
    if len(nonbenchstocks) != 0:
        convertcols = portfolio + ['portprices']
    else:
        convertcols = portfolio
    # CREATE BAREMAX VERSIONS OF SAME
    convertcols = portfolio + ['portprices']
    bmaxstock = []
    for item in convertcols:
        rawlist = sliced[item].tolist()
        bmaxlist = baremax_cruncher(rawlist)
        baremaxcolname = 'baremax {}'.format(item)
        sliced[baremaxcolname] = np.array(bmaxlist)
        if item in portfolio:
            bmaxstock.append(baremaxcolname)
    # CATEGORIZE COLS
    portbaremax = ['baremax portprices']
    portraw = ['portprices']
    return portbaremax, portraw, bmaxstock, sliced


def createsqueezefactor(sliced, portfolio):
    # CREATE BAREMIN VERSIONS OF SAME
    convertcols = portfolio + ['portprices']
    squeezestock = []
    for item in convertcols:
        rawlist = sliced[item].tolist()
        bminlist = oldbaremin_cruncher(rawlist)
        bmaxlist = baremax_cruncher(rawlist)
        baremincolname = 'baremin {}'.format(item)
        sliced[baremincolname] = np.array(bminlist)
        baremaxcolname = 'baremax {}'.format(item)
        sliced[baremaxcolname] = np.array(bmaxlist)
        if item in portfolio:
            squeezestock.append(baremincolname)
            squeezestock.append(baremaxcolname)

    # CATEGORIZE COLS
    portbaremin = ['baremin portprices']
    portbaremax = ['baremax portprices']
    portraw = ['portprices']

    return portbaremin, portbaremax, portraw, squeezestock, sliced


# QUICK GRAPHS A STOCK IN VARIOUS CALIBRATIONS
def quickaxes_portfolios(ax1, sliced, portcols, portfolio, portlines, portlinenames):

    for item in portcols:
        portlinename = '{} -- {}'.format(portfolio, item)
        if len(portcols) == 2:
            if item == 'portprices':
                portline, = ax1.plot(sliced[item], alpha=0.5, label=portlinename)
            else:
                portline, = ax1.plot(sliced[item], linewidth=3.0, label=portlinename)
        else:
            portline, = ax1.plot(sliced[item], label=portlinename)
        portlines.append(portline)
        portlinenames.append(portlinename)


# QUICK GRAPHS A STOCK IN VARIOUS CALIBRATIONS
def quickaxes(ax1, sliced, stockcols, portcols, graph_portfolio_line):

    stocklines = []
    stocklinenames = []
    alphaval = 1
    if graph_portfolio_line == 'yes':
        for item in portcols:
            ax1.plot(sliced[item], linewidth=4.0)
        alphaval = 0.5
    for item in stockcols:
        stocklinename = '{}'.format(item)
        stockline, = ax1.plot(sliced[item], alpha=alphaval, label=stocklinename)
        stocklines.append(stockline)
        stocklinenames.append(stocklinename)
    ax1.legend(stocklines, stocklinenames)


def quickaxes1(axe, prices, displaycols):

    graphlines = []
    graphlinenames = []
    for item in displaycols:
        graphlinename = '{}'.format(item)
        graphline, = axe.plot(prices[item], label=graphlinename)
        graphlines.append(graphline)
        graphlinenames.append(graphlinename)
    axe.legend(graphlines, graphlinenames)


# RETURN DF OF GRAPH DATA FOR SINGLE STOCK
def graphdf_single(pricecalibration, stock, beg_date, end_date):

    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(inplace=True, drop=True)
    # CALIBRATE PRICES
    if pricecalibration == 'norm':
        firstp = prices.loc[0, stock]
        calibcol = f'norm {stock}'
        prices[calibcol] = (prices[stock] - firstp) / firstp
        graphcols = [calibcol]
    elif pricecalibration == 'minmax':
        minprices = prices[stock].min(axis=0)
        maxprices = prices[stock].max(axis=0)
        calibcol = f'minmax {stock}'
        prices[calibcol] = (prices[stock] - minprices) / (maxprices - minprices)
        graphcols = [calibcol]
    elif pricecalibration == 'bareminraw' or pricecalibration == 'oldbareminraw' or pricecalibration == 'squeezefactor':
        rawlist = prices[stock].tolist()
        if pricecalibration == 'bareminraw':
            pricedatalist = baremin_cruncher(rawlist)
            calibcol = f'baremin {stock}'
            prices[calibcol] = np.array(pricedatalist)
            graphcols = [stock, calibcol]
        elif pricecalibration == 'oldbareminraw' or pricecalibration == 'squeezefactor':
            pricedatalist = oldbaremin_cruncher(rawlist)
            calibcol = f'oldbaremin {stock}'
            prices[calibcol] = np.array(pricedatalist)
            graphcols = [stock, calibcol]
            if pricecalibration == 'squeezefactor':
                bmaxlist = baremax_cruncher(rawlist)
                calibcol2 = 'baremax {}'.format(stock)
                prices[calibcol2] = np.array(bmaxlist)
                graphcols = [stock, calibcol, calibcol2]
    else:
        graphcols = [stock]
    return prices, graphcols


# QUICK GRAPHS A STOCK IN VARIOUS CALIBRATIONS
def getgraphdata(pricecalibration, portfolio, beg_date, end_date):

    nonbenchstocks = [item for item in portfolio if item not in ['^DJI', '^INX', '^IXIC']]
    benchstocks = [item for item in portfolio if item in ['^DJI', '^INX', '^IXIC']]

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

    # BACKFILL PRICES FOR GRAPHING PURPOSES (GRAPH WOULDN'T APPEAR IF PRICES ARE NAN FOR DATE REQUESTED)
    sliced = sliced.fillna(method='bfill')

    # SLICE OUT DATE RANGE REQUESTED
    sliced = sliced.loc[(sliced['date'] >= beg_date) & (sliced['date'] <= end_date)].copy()

    # RESET INDEX
    sliced.reset_index(drop=True, inplace=True)

    # CALIBRATE PRICES
    if pricecalibration == 'raw' or pricecalibration == 'bareminraw' or pricecalibration == 'baremaxraw' or pricecalibration == 'rawsqueezefactor' or pricecalibration == 'oldbareminraw':

        # NORMALIZE EACH PRICE CURVE AND CREATE PORTFOLIO CURVE
        firstp = sliced.loc[0, portfolio]
        sliced[portfolio] = (sliced[portfolio] - firstp) / firstp

    elif pricecalibration == 'minmax' or pricecalibration == 'minmaxbaremin' or pricecalibration == 'squeezefactor':

        # MINMAX CALIBRATE EACH PRICE CURVE AND CREATE PORTFOLIO CURVE
        minprices = sliced[portfolio].min(axis=0)
        maxprices = sliced[portfolio].max(axis=0)
        sliced[portfolio] = (sliced[portfolio] - minprices) / (maxprices - minprices)

    # CREATE PORTFOLIO PRICES
    sliced['portprices'] = sliced[nonbenchstocks].mean(axis=1)

    # PREP GRAPHCOLS
    if pricecalibration == 'bareminraw':
        portbaremin, portraw, bareminstock, sliced = createbaremin(sliced, portfolio, nonbenchstocks)
    elif pricecalibration == 'oldbareminraw':
        portbaremin, portraw, bareminstock, sliced = createoldbaremin(sliced, portfolio, nonbenchstocks)
    elif pricecalibration == 'baremaxraw':
        portbaremax, portraw, baremaxstock, sliced = createbaremax(sliced, portfolio, nonbenchstocks)
    elif pricecalibration == 'minmaxbaremin':
        portbaremin, portraw, bareminstock, sliced = createbaremin(sliced, portfolio, nonbenchstocks)
    elif pricecalibration == 'squeezefactor' or pricecalibration == 'rawsqueezefactor' or pricecalibration == 'rawsqueezefactorsingle':
        portbaremin, portbaremax, portraw, squeezestock, sliced = createsqueezefactor(sliced, portfolio)

    # ASSIGN GRAPHCOLS
    if pricecalibration == 'bareminraw' or pricecalibration == 'oldbareminraw' or pricecalibration == 'minmaxbaremin':
        stockcols = portfolio + bareminstock
        portcols = portraw + portbaremin
    elif pricecalibration == 'baremaxraw':
        stockcols = portfolio + baremaxstock
        portcols = portraw + portbaremax
    elif pricecalibration == 'squeezefactor' or pricecalibration == 'rawsqueezefactor' or pricecalibration == 'rawsqueezefactorsingle':
        stockcols = portfolio + squeezestock
        portcols = portraw + portbaremin + portbaremax
    else:
        stockcols = portfolio
        portcols = ['portprices']

    return sliced, stockcols, portcols


# QUICK GRAPHS A STOCK IN VARIOUS CALIBRATIONS
def quickgraph_portfolio(pricecalibration, portfolio, beg_date, end_date, graph_portfolio_line):

    # FIX END DATE
    if end_date == '':
        # FIND LATEST DATE AVAILABLE
        with open(daterangedb_source, "rb") as targetfile:
            daterangedb = pkl.load(targetfile)
        lastdate_dateobj = daterangedb['last_date'].apply(lambda x: dt.date.fromisoformat(x))
        lastdates = lastdate_dateobj.tolist()
        end_date = str(np.max(lastdates))

    sliced, stockcols, portcols = getgraphdata(pricecalibration, portfolio, beg_date, end_date)

    # GET VOLATILITY STATS
    volstr = 'Volatility Scores:'
    allvolcols = portfolio + ['portprices']
    for volcol in allvolcols:
        # IF VOLATILITY DATA USE ABSOLUTE PRICES, USE .PCTCHANGE
        if pricecalibration == 'rawsingle' or pricecalibration == 'rawsqueezefactorsingle':
            volarr = abs(np.array(allpctchanges(sliced, volcol, 1)))
        # IF DATA IS ALREADY IN PERCENTAGE OR RELATIVE UNITS (MINMAX CALIB E.G.) USE .DIFF
        else:
            volarr = abs(np.array(alldiffs(sliced, volcol, 1)))
        volavg = np.mean(volarr)
        voldev = np.std(volarr)
        volscore = volavg + voldev
        volstr += f'\n{volcol}: {volscore} (voldev: {voldev} + volavg: {volavg})'

    # GRAPH IT
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    quickaxes(ax1, sliced, stockcols, portcols, graph_portfolio_line)
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # place a text box in upper left in axes coords
    #ax1.text(0.15, 0.95, volstr, transform=ax1.transAxes, fontsize=8, verticalalignment='top', bbox=props)

    plt.title('{} to {} {}'.format(beg_date, end_date, pricecalibration))
    plt.show()


# QUICK GRAPHS A STOCK IN VARIOUS CALIBRATIONS
def quickgraph(pricecalibration, stocklist, beg_date, end_date):

    for item in stocklist:
        prices = grabsinglehistory(item)
        prices = fill_gaps2(prices, beg_date, end_date)

        if pricecalibration == 'raw':
            prices['prices'] = prices[item]
            displaycols = ['prices']
        elif pricecalibration == 'normalized':
            firstp = prices.iat[0, 1]
            prices['prices'] = prices[item] / firstp
            displaycols = ['prices']
        elif pricecalibration == 'normbaremin':
            firstp = prices.iat[0, 1]
            prices['prices'] = prices[item] / firstp
            rawlist = prices['prices'].tolist()
            pricedatalist = baremin_cruncher(rawlist)
            prices['bareminprices'] = np.array(pricedatalist)
            displaycols = ['prices', 'bareminprices']
        elif pricecalibration == 'minmax':
            allprices = prices[item].tolist()
            minprice = np.min(allprices)
            maxprice = np.max(allprices)
            prices['prices'] = (prices[item] - minprice) / (maxprice - minprice)
            displaycols = ['prices']
        elif pricecalibration == 'bareminraw':
            prices['prices'] = prices[item]
            rawlist = prices['prices'].tolist()
            pricedatalist = baremin_cruncher(rawlist)
            prices['bareminprices'] = np.array(pricedatalist)
            displaycols = ['prices', 'bareminprices']
        elif pricecalibration == 'minmaxbaremin':
            allprices = prices[item].tolist()
            minprice = np.min(allprices)
            maxprice = np.max(allprices)
            prices['prices'] = (prices[item] - minprice) / (maxprice - minprice)
            rawlist = prices['prices'].tolist()
            pricedatalist = baremin_cruncher(rawlist)
            prices['bareminprices'] = np.array(pricedatalist)
            displaycols = ['prices', 'bareminprices']

        # GRAPH IT
        '''TO DO: FIGURE OUT HOW TO DISPLAY ALL GRAPHS IN ONE GRID'''
        prices[displaycols].plot()
        plt.title('{} - {}'.format(item, pricecalibration))
        plt.legend()
        plt.show()


def pricecalibrator(prices, stock, pricecalibration):

    pricecolname = '{} {} prices'.format(stock, pricecalibration)
    if pricecalibration == 'raw':
        prices[pricecolname] = prices[stock]
    elif pricecalibration == 'normalized':
        firstp = prices.iat[0, 1]
        prices[pricecolname] = (prices[stock] - firstp) / firstp
    elif pricecalibration == 'normbaremin':
        firstp = prices.iat[0, 1]
        prices['normprices'] = (prices[stock] - firstp) / firstp
        rawlist = prices['normprices'].tolist()
        pricedatalist = baremin_cruncher(rawlist)
        prices[pricecolname] = np.array(pricedatalist)
    elif pricecalibration == 'minmax':
        allprices = prices[stock].tolist()
        minprice = np.min(allprices)
        maxprice = np.max(allprices)
        prices[pricecolname] = (prices[stock] - minprice) / (maxprice - minprice)
    elif pricecalibration == 'bareminraw':
        rawlist = prices[stock].tolist()
        pricedatalist = baremin_cruncher(rawlist)
        prices[pricecolname] = np.array(pricedatalist)
    elif pricecalibration == 'minmaxbaremin':
        allprices = prices[stock].tolist()
        minprice = np.min(allprices)
        maxprice = np.max(allprices)
        prices['mmprices'] = (prices[stock] - minprice) / (maxprice - minprice)
        rawlist = prices['mmprices'].tolist()
        pricedatalist = baremin_cruncher(rawlist)
        prices[pricecolname] = np.array(pricedatalist)

    return prices


def comparegraphs(calibrations, portfolio, beg_date, end_date):

    num_plotcols = len(portfolio)
    num_plotrows = len(calibrations)

    # SETUP GRAPH
    fig = plt.figure()
    plt.rcParams.update({'font.size': 5})
    stockcount = 1
    for stock in portfolio:

        # GET PRICE HISTORY
        prices = grabsinglehistory(stock)
        prices = fill_gaps2(prices, beg_date, end_date)

        # COLLECT GRAPH DATA
        subplotcoldict = {}
        calibcount = 1
        for calib in calibrations:

            # GET CALIBRATED PRICING
            pricecolname = '{} {} prices'.format(stock, calib)
            prices = pricecalibrator(prices, stock, calib)

            # ADD STUFF TO GRAPH
            keyname = 'subplot{}'.format(calibcount)
            subplotcoldict.update({keyname: pricecolname})
            calibcount += 1

        # FOR EACH SUBPLOT, ADD AXES TO FIGURE
        spcount = 0
        for key in subplotcoldict:
            subplotindex = stockcount + (spcount * num_plotcols)
            axe = fig.add_subplot(num_plotrows, num_plotcols, subplotindex)
            axe.set_title(subplotcoldict[key])
            quickaxes1(axe, prices, [subplotcoldict[key]])
            spcount += 1

        stockcount += 1

    plt.show()
