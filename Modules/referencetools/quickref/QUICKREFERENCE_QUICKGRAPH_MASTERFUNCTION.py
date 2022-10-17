"""
Title: Quick Reference - QUICKGRAPH - MASTERSCRIPT FUNCTION
Date Started: July 11, 2020
Version: 1.00
Version Start: July 11, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Master function to run the quickgraph program.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import easygui
#   LOCAL APPLICATION IMPORTS
from QUICKREFERENCE_BASE import quickgraph_portfolio, graphdf_single
from timeperiodbot import oldeststockipodate, youngeststockipodate
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2


def graphsidebyside(stock, beg_date, end_date, leftgraph, rightgraph):

    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    allprices = prices[stock].tolist()
    oldbareminrawpricelist = oldbaremin_cruncher(allprices)
    prices['oldbareminraw'] = np.array(oldbareminrawpricelist)
    baremaxrawpricelist = baremax_cruncher(allprices)
    prices['baremaxraw'] = np.array(baremaxrawpricelist)
    prices['trueline'] = ((prices['baremaxraw'] - prices['oldbareminraw']) / 2) + prices['oldbareminraw']
    prices['squeezeline'] = (prices['baremaxraw'] - prices['oldbareminraw']) / prices['oldbareminraw']
    prices['rawtrue'] = abs(prices[stock] - prices['trueline']) / prices['trueline']
    prices['smoothline'] = (prices[stock] - prices['oldbareminraw']) / prices['oldbareminraw']
    age = len(prices) - 1
    # get all straight and kneelines
    for focuscol in ['baremaxraw', 'oldbareminraw', stock, 'trueline']:
        price_start = prices.iloc[0][focuscol]
        price_end = prices.iloc[-1][focuscol]
        slope = (price_end - price_start) / age
        if focuscol == stock:
            focuscolname = 'raw'
        else:
            focuscolname = focuscol
        prices[f'{focuscolname}_straightline'] = [(slope * x) + price_start for x in range(age + 1)]
        prices[f'{focuscolname}_kneeline'] = (prices[focuscol] - prices[f'{focuscolname}_straightline']) / prices[f'{focuscolname}_straightline']
    # get all dpcs
    for focuscol in ['baremaxraw', 'oldbareminraw', stock, 'trueline']:
        if focuscol == stock:
            focuscolname = 'raw'
        else:
            focuscolname = focuscol
        prices[f'{focuscolname}_dpc'] = prices[focuscol].pct_change(periods=1, fill_method='ffill')
    modleftgraph = []
    for item in leftgraph:
        # modify graphlist
        if item == 'raw':
            #leftgraph[leftgraph.index(item)] = stock
            modleftgraph.append(stock)
        else:
            modleftgraph.append(item)
    ax1 = plt.subplot(1, 2, 1)
    plt.plot(prices[modleftgraph])
    plt.subplot(1, 2, 2, sharex=ax1)
    plt.plot(prices[rightgraph])
    plt.title(f'{stock}: left graph: {modleftgraph}: right graph: {rightgraph}')
    plt.show()


# OUTPUTS GRAPH OF GIVEN LIST OF TICKERS AND PARAMS
def quickgraphlist(beg_date, beg_date_type, graphlist, daterangedb_source, pricecalibration, end_date, graph_portfolio_line, sidebysidecustom, leftgraph, rightgraph):
    # SET BEGDATE
    if beg_date_type == 'youngest':
        beg_date = youngeststockipodate(graphlist, daterangedb_source)
    elif beg_date_type == 'oldest':
        beg_date = oldeststockipodate(graphlist, daterangedb_source)
    elif beg_date_type == 'fixed':
        beg_date = beg_date

    # GRAPH
    if sidebysidecustom == 'yes':
        graphsidebyside(graphlist[0], beg_date, end_date, leftgraph, rightgraph)
    else:
        quickgraph_portfolio(pricecalibration, graphlist, beg_date, end_date, graph_portfolio_line)


# RETURNS GRAPH OUTPUTS IN SEQUENCE OR ALL AT ONCE
def runquickgraph(sidebysidecustom, leftgraph, rightgraph, sequence, beg_date, beg_date_type, fullstocklist, benchmark, beg_stock_index, end_stock_index, daterangedb_source, pricecalibration, end_date, graph_portfolio_line):

    graphlist = fullstocklist[beg_stock_index:end_stock_index] + [benchmark]
    if sequence.startswith('yes') is False:
        if sequence == 'nowithoutbench':
            graphlist = fullstocklist[beg_stock_index:end_stock_index]
        quickgraphlist(beg_date, beg_date_type, graphlist, daterangedb_source, pricecalibration, end_date, graph_portfolio_line, sidebysidecustom, leftgraph, rightgraph)

    else:
        for stock in graphlist[:-1]:
            if sequence == 'yeswithbench':
                substocklist = [stock, benchmark]
            else:
                substocklist = [stock]
            quickgraphlist(beg_date, beg_date_type, substocklist, daterangedb_source, pricecalibration, end_date, graph_portfolio_line, sidebysidecustom, leftgraph, rightgraph)


# MANUALLY COMPARE GRAPHS OF A GIVEN LIST TWO AT A TIME; AND RETURNS SCORE OF ORDER ACCURACY
def rankreview_sidebysidegraph(stocklist, pricecalibration, beg_date, beg_date_type, end_date, daterangedb_source):

    tallylist = []
    for rank in range(len(stocklist)-1):
        stock1 = stocklist[rank]
        stock2 = stocklist[rank+1]
        # SET BEGDATE
        if beg_date_type == 'youngest':
            beg_date = youngeststockipodate([stock1, stock2], daterangedb_source)
        elif beg_date_type == 'oldest':
            beg_date = oldeststockipodate([stock1, stock2], daterangedb_source)
        elif beg_date_type == 'fixed':
            beg_date = beg_date
        elif beg_date_type == 'full':
            beg_date = ''

        # RETRIEVE PLOT GRAPHS FOR EACH PAIR
        prices1, graphcols1 = graphdf_single(pricecalibration, stock1, beg_date, end_date)
        prices2, graphcols2 = graphdf_single(pricecalibration, stock2, beg_date, end_date)

        plt.subplot(1, 2, 1)
        plt.plot(prices1[graphcols1])
        plt.title(f'Stock: {stock1} Rank: {rank}')

        plt.subplot(1, 2, 2)
        plt.plot(prices2[graphcols2])
        plt.title(f'Stock: {stock2} Rank: {rank+1}')
        plt.show()

        # ASK WHICH YOU LIKE BETTER:
        choice = easygui.ynbox(f'Was {stock1} better than {stock2}? If it is too close to call, choose YES')

        if choice is False:
            tallylist.append(1)
        else:
            tallylist.append(0)

    # PRESENT RESULTS
    print(f'{len(tallylist)} comparisons have been made.')
    print(f'{np.sum(tallylist)} were ranked incorrectly according to manual review. ({np.mean(tallylist) * 100} % inaccuracy rate)')
