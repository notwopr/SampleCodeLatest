"""
Title: TESTREVIEWER - RANKVIEWER
Date Started: Feb 25, 2020
Version: 1.0
Version Start: Feb 25, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Visually compare graphs and tally results and return scores of best method.
Remove test2 and add rankviewer.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import easygui
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from FINALBAREMINCRUNCHER import baremin_cruncher, baremax_cruncher, oldbaremin_cruncher


def quickref2(stock, beg_date, end_date, pricecalibration):

    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)

    if pricecalibration == 'raw':
        prices[pricecalibration] = prices[stock]
    if pricecalibration == 'minmax':
        allprices = prices[stock].tolist()
        minprice = np.min(allprices)
        maxprice = np.max(allprices)
        if minprice != maxprice:
            prices[pricecalibration] = (prices[stock] - minprice) / (maxprice - minprice)
        else:
            prices[pricecalibration] = 0
    if pricecalibration == 'normalized':
        firstp = prices.iat[0, 1]
        if firstp == 0:
            firstp = 1.00
        prices[pricecalibration] = prices[stock] / firstp
    if pricecalibration == 'baremin':
        pricelist = prices[stock].tolist()
        newpricelist = baremin_cruncher(pricelist)
        prices[pricecalibration] = np.array(newpricelist)
    if pricecalibration == 'baremin_minmax':
        # MIN MAX NORM
        allprices = prices[stock].tolist()
        minprice = np.min(allprices)
        maxprice = np.max(allprices)
        if minprice != maxprice:

            # GET MINMAX NORMALIZED BAREMIN PRICES
            prices['minmaxnorm_prices'] = (prices[stock] - minprice) / (maxprice - minprice)
            pricelist = prices['minmaxnorm_prices'].tolist()
            newpricelist = baremin_cruncher(pricelist)
            prices[pricecalibration] = np.array(newpricelist)
        else:
            prices[pricecalibration] = 0
    if pricecalibration == 'baremin_norm':
        firstp = prices.iat[0, 1]
        if firstp == 0:
            firstp = 1.00
        prices['norm'] = prices[stock] / firstp
        pricelist = prices['norm'].tolist()
        newpricelist = baremin_cruncher(pricelist)
        prices[pricecalibration] = np.array(newpricelist)
    return prices


def rankviewer(method, min_age, rankinglist, rankcolname, sortascend, pricecalibration):
    all_method_tallies = {}
    methodtally = 0
    rfile = method.rankingfile()

    # CHOOSE RANK COLUMN AND SORT
    rfile.sort_values(ascending=sortascend, by=[rankcolname], inplace=True)
    rfile.reset_index(drop=True, inplace=True)

    # FILTER IF MIN_AGE SET
    if min_age != '':
        filteredrfile = rfile[rfile['age'] >= min_age]
        filteredrfile.reset_index(drop=True, inplace=True)
        stocklist = filteredrfile['stock'].tolist()
    else:
        stocklist = rfile['stock'].tolist()

    for rank in rankinglist:
        firstticker = stocklist[rank-1]
        secondticker = stocklist[rank]

        # RETRIEVE GRAPHS FOR EACH PAIR
        firsttickerdf = quickref2(firstticker, '', method.end_date, pricecalibration)
        secondtickerdf = quickref2(secondticker, '', method.end_date, pricecalibration)

        priceline = pricecalibration
        plt.subplot(1, 2, 1)
        plt.plot(firsttickerdf[[priceline.format(firstticker)]])
        plt.title('{} Rank {}: {}'.format(rankcolname, rank, firstticker))

        plt.subplot(1, 2, 2)
        plt.plot(secondtickerdf[[priceline.format(secondticker)]])
        plt.title('{} Rank {}: {}'.format(rankcolname, rank+1, secondticker))
        plt.show()

        # ASK WHICH YOU LIKE BETTER:
        choice = easygui.ynbox('Was {} better than {}? If it is too close to call, choose YES'.format(firstticker, secondticker))

        if choice is False:
            methodtally += 1

    all_method_tallies.update({method.methodname: methodtally})

    # PRESENT RESULTS
    print('{} RANKINGS BY {} HAVE BEEN COMPARED'.format(rankingtotal, rankcolname))
    print('{} OF THEM WERE RANKED INCORRECTLY'.format(all_method_tallies[method.methodname]))


def squeezedfprep(stock, beg_date, end_date):
    prices = quickref2(stock, beg_date, end_date, 'minmax')
    pricelist = prices['minmax'].tolist()
    newpricelist1 = oldbaremin_cruncher(pricelist)
    prices['oldbaremin'] = np.array(newpricelist1)
    newpricelist2 = baremax_cruncher(pricelist)
    prices['baremax'] = np.array(newpricelist2)
    prices['squeeze'] = prices['baremax'] - prices['oldbaremin']

    return prices


def squeezefactor_viewer(method, rankingtotal, sortascend, rankcolname):

    rfile = method.rankingfile()

    # CHOOSE RANK COLUMN AND SORT
    rfile.sort_values(ascending=sortascend, by=[rankcolname], inplace=True)
    rfile.reset_index(drop=True, inplace=True)

    stocklist = rfile['stock'].tolist()
    rankinglist = list(range(rankingtotal+1))[1:]
    for rank in rankinglist:
        firstticker = stocklist[rank-1]
        secondticker = stocklist[rank]

        # GET SQUEEZEFACTOR VALUES
        squeezefactor1 = rfile[rfile['stock'] == firstticker]['squeezefactor'].iat[0]
        squeezefactor2 = rfile[rfile['stock'] == secondticker]['squeezefactor'].iat[0]
        squeezevol1 = rfile[rfile['stock'] == firstticker]['squeezevolatility'].iat[0]
        squeezevol2 = rfile[rfile['stock'] == secondticker]['squeezevolatility'].iat[0]

        # RETRIEVE GRAPHS FOR EACH PAIR
        firsttickerdf = squeezedfprep(firstticker, '', method.end_date)
        secondtickerdf = squeezedfprep(secondticker, '', method.end_date)

        plt.subplot(2, 2, 1)
        plt.plot(firsttickerdf[['oldbaremin', 'baremax', 'minmax']])
        plt.title('Rank {}: {}'.format(rank-1, firstticker))

        ax1 = plt.subplot(2, 2, 3)
        plt.plot(firsttickerdf['squeeze'])
        plt.title('Squeezefactor: {} Volatility: {}'.format(squeezefactor1, squeezevol1))

        plt.subplot(2, 2, 2)
        plt.plot(secondtickerdf[['oldbaremin', 'baremax', 'minmax']])
        plt.title('Rank {}: {}'.format(rank, secondticker))

        plt.subplot(2, 2, 4, sharey=ax1)
        plt.plot(secondtickerdf['squeeze'])
        plt.title('Squeezefactor: {} Volatility: {}'.format(squeezefactor2, squeezevol2))
        plt.show()
