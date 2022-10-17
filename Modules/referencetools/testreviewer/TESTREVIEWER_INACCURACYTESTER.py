"""
Title: Best Weight Finder - Test Reviewer
Date Started: Jan 23, 2020
Version: 4.0
Version Start: Feb 24, 2020
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
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from FINALBAREMINCRUNCHER import baremin_cruncher
from BACKTEST_GATHERMETHOD_LAYERCAKE import asdrbareminraw_single, mmbmsmooth_single, allrawvolatiles_single


def quickref(beg_date, end_date, stock):

    # GET PRICES
    prices = grabsinglehistory(stock)

    # CUSTOM SPAN DATES AND CORRECT ZEROS
    prices = fill_gaps2(prices, beg_date, end_date)

    return prices


def quickref1(stock, beg_date, end_date, viewmod):

    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)

    # GET AGE
    lastd = prices.iat[-1, 0]
    firstd = prices.iat[0, 0]
    age = (lastd - firstd).days

    allprices = prices[stock].tolist()
    minprice = np.min(allprices)
    maxprice = np.max(allprices)
    pricecolname = '{}_minmax_calibration'.format(stock)
    smoothcolname = '{}_smooth'.format(stock)
    if minprice != maxprice:
        prices[pricecolname] = (prices[stock] - minprice) / (maxprice - minprice)
    else:
        prices[pricecolname] = 0

    if viewmod == 'baremin':
        # GET LIST OF PRICES
        pricelist = prices[pricecolname].tolist()
        newpricelist = baremin_cruncher(pricelist)
        prices['{}_baremin'.format(stock)] = np.array(newpricelist)
        prices[smoothcolname] = abs(prices[pricecolname] - prices['{}_baremin'.format(stock)])
    else:
        # GET POLYNOMIAL PRICE HISTORY
        x_vals = list(range(age + 1))
        x = np.array(x_vals)
        y = np.array(prices[pricecolname])
        z = np.polyfit(x, y, 3)
        p = np.poly1d(z)
        prices['index'] = prices[pricecolname].index
        prices['{}_polyn'.format(stock)] = p(prices['index'])

        # ABSOLUTE DEVIATION
        prices[smoothcolname] = abs(prices[pricecolname] - prices['{}_polyn'.format(stock)])

    return prices


def quickref2(beg_date, end_date, stock):

    # GET PRICES
    prices = grabsinglehistory(stock)

    # CUSTOM SPAN DATES AND CORRECT ZEROS
    prices = fill_gaps2(prices, beg_date, end_date)

    # BAREMINRAW METRICS
    allprices = prices[stock].tolist()
    newpricelist = baremin_cruncher(allprices)
    prices['bareminrawprices'] = np.array(newpricelist)

    # MINMAX METRICS
    minprice = np.min(allprices)
    maxprice = np.max(allprices)
    if minprice != maxprice:
        prices['minmaxprices'] = (prices[stock] - minprice) / (maxprice - minprice)
        rawlist = prices['minmaxprices'].tolist()
        pricedatalist = baremin_cruncher(rawlist)
        prices['mmbmprices'] = np.array(pricedatalist)

    return prices


def inaccuracytester(method, min_age, rankingtotal, rankcolname, viewmod, reviewtype, sortascend, dataloc):

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

    tallylist = []
    rankinglist = list(range(rankingtotal+1))[1:]
    for rank in rankinglist:
        firstticker = stocklist[rank-1]
        secondticker = stocklist[rank]

        if dataloc == 'incsv':
            # SET COLNAMES
            volatilescorecol = 'volatilescore'
            smoothscorecol = 'smoothscore'
            dailygrowthcol = 'asdrscore'

            # CALCULATE SMOOTHNESS AND BAREMIN OVERALL GROWTH
            volatilescore1 = rfile[rfile['stock'] == firstticker][volatilescorecol].iat[0]
            volatilescore2 = rfile[rfile['stock'] == secondticker][volatilescorecol].iat[0]
            truedailygrowth1 = rfile[rfile['stock'] == firstticker][dailygrowthcol].iat[0]
            truedailygrowth2 = rfile[rfile['stock'] == secondticker][dailygrowthcol].iat[0]
            smoothscore1 = rfile[rfile['stock'] == firstticker][smoothscorecol].iat[0]
            smoothscore2 = rfile[rfile['stock'] == secondticker][smoothscorecol].iat[0]
        else:
            # CALCULATE SHARPE METRICS
            firsttickerdf = quickref2('', method.end_date, firstticker)
            secondtickerdf = quickref2('', method.end_date, secondticker)
            firsttickerage = len(firsttickerdf)-1
            secondtickerage = len(secondtickerdf)-1

            asdev1, asdevmed1 = allrawvolatiles_single(firstticker, firsttickerdf, firsttickerage)
            volatilescore1 = np.mean([asdev1, asdevmed1])
            asdev2, asdevmed2 = allrawvolatiles_single(secondticker, secondtickerdf, secondtickerage)
            volatilescore2 = np.mean([asdev2, asdevmed2])
            asdr1, asdrmed1 = asdrbareminraw_single(firsttickerdf, firsttickerage)
            truedailygrowth1 = np.mean([asdr1, asdrmed1])
            asdr2, asdrmed2 = asdrbareminraw_single(secondtickerdf, secondtickerage)
            truedailygrowth2 = np.mean([asdr2, asdrmed2])
            mmbmsmoothscore1, mmbmsmoothscoremed1 = mmbmsmooth_single(firsttickerdf)
            smoothscore1 = np.mean([mmbmsmoothscore1, mmbmsmoothscoremed1])
            mmbmsmoothscore2, mmbmsmoothscoremed2 = mmbmsmooth_single(secondtickerdf)
            smoothscore2 = np.mean([mmbmsmoothscore2, mmbmsmoothscoremed2])
        if volatilescore1 != 0 and volatilescore2 != 0:
            growthnumer1 = truedailygrowth1 * (1 - smoothscore1)
            growthnumer2 = truedailygrowth2 * (1 - smoothscore2)
            sharpe1 = growthnumer1 / volatilescore1
            sharpe2 = growthnumer2 / volatilescore2

            if reviewtype == 'manual':
                # RETRIEVE PLOT GRAPHS FOR EACH PAIR
                firsttickerdf2 = quickref1(firstticker, '', method.end_date, viewmod)
                secondtickerdf2 = quickref1(secondticker, '', method.end_date, viewmod)

                if viewmod == 'baremin':
                    trajectoryline = '{}_baremin'
                else:
                    trajectoryline = '{}_polyn'

                priceline = '{}_minmax_calibration'
                deviationline = '{}_smooth'

                plt.subplot(2, 2, 1)
                plt.plot(firsttickerdf2[[priceline.format(firstticker), trajectoryline.format(firstticker)]])
                plt.title('{} Rank {}: {} TrueDailyGrowth: {}'.format(rankcolname, rank, firstticker, truedailygrowth1))

                plt.subplot(2, 2, 2)
                plt.plot(secondtickerdf2[[priceline.format(secondticker), trajectoryline.format(secondticker)]])
                plt.title('{} Rank {}: {} TrueDailyGrowth: {}'.format(rankcolname, rank+1, secondticker, truedailygrowth2))

                ax1 = plt.subplot(2, 2, 3)
                plt.plot(firsttickerdf2[[deviationline.format(firstticker)]])
                plt.title('Rank {}: {} Smooth Score: {} Sharpe: {}'.format(rank, firstticker, smoothscore1, sharpe1))

                plt.subplot(2, 2, 4, sharey=ax1)
                plt.plot(secondtickerdf2[[deviationline.format(secondticker)]])
                plt.title('Rank {}: {} Smooth Score: {} Sharpe: {}'.format(rank+1, secondticker, smoothscore2, sharpe2))
                plt.show()

                # ASK WHICH YOU LIKE BETTER:
                choice = easygui.ynbox('Was {} better than {}? If it is too close to call, choose YES'.format(firstticker, secondticker))

                if choice is False:
                    methodtally += 1
            else:
                if sharpe2 > sharpe1 and growthnumer2 > growthnumer1 and volatilescore2 < volatilescore1:
                    tallylist.append(1)
                elif sharpe2 > sharpe1 and growthnumer2 > growthnumer1:
                    tallylist.append(1)
                elif sharpe2 > sharpe1 and volatilescore2 < volatilescore1:
                    tallylist.append(1)
                elif volatilescore2 < volatilescore1 and truedailygrowth2 > truedailygrowth1:
                    tallylist.append(1)
                else:
                    tallylist.append(0)

    all_method_tallies.update({method.methodname: methodtally})

    # PRESENT RESULTS
    print('{} RANKINGS HAVE BEEN COMPARED'.format(len(tallylist)))
    print('{} OF METHOD {} WERE RANKED INCORRECTLY'.format(all_method_tallies[method.methodname], rankcolname))
    finalinaccscore = np.mean(tallylist) * 100
    print('({} % inaccuracy rate)'.format(finalinaccscore))

    return finalinaccscore


def inaccpackage(testsample, min_age, rankingtotal, viewmod, reviewtype, sortascend, dataloc):

    # GET RANK COLUMNS
    rfile = testsample.rankingfile()
    allcols = list(rfile.columns)
    rankcols = []
    for item in allcols:
        if item.find('RANK') != -1:
            rankcols.append(item)

    # GET INACCSCORE FOR EACH RANKCOL
    inaccdfdata = []
    for rankcol in rankcols:
        rankcolinacc = inaccuracytester(testsample, min_age, rankingtotal, rankcol, viewmod, reviewtype, sortascend, dataloc)
        print(rankcolinacc)
        inaccdfdata.append({'rankcol': rankcol, 'inaccuracyrate (%)': rankcolinacc})

    # CREATE DF OF RESULTS
    inaccdf = pd.DataFrame(data=inaccdfdata)
    # SORT AND RESET
    inaccdf.sort_values(ascending=True, by=['inaccuracyrate (%)'], inplace=True)
    inaccdf.reset_index(drop=True, inplace=True)

    print(inaccdf)
