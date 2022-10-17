"""
Title: TESTREVIEWER - RANK METHOD BASE
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
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from FINALBAREMINCRUNCHER import baremin_cruncher
from BACKTEST_GATHERMETHOD_LAYERCAKE import allrawvolatiles_single, asdrbareminraw_single, mmbmsmooth_single


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


def comparetworanks(method, col1, col2, targetinacclen, reviewamount, viewmod, reviewtype, dataloc):

    col1inacclist = []
    col2inacclist = []
    rfile = method.rankingfile()

    # GET STOCKS WHERE THE RANKINGS BETWEEN THE TWO METHODS DIFFER GREATEST
    scratchdf = rfile.copy()
    scratchdf['rankdiff'] = abs(scratchdf[col1] - scratchdf[col2])
    scratchdf.sort_values(ascending=False, by=['rankdiff'], inplace=True)
    scratchdf.reset_index(drop=True, inplace=True)

    # GET LIST OF STOCKS TO LOOK OVER
    fullreviewlist = scratchdf.loc[(np.isnan(scratchdf['rankdiff']) == False) & (scratchdf['rankdiff'] != 0), 'stock'].tolist()

    print('Number of stocks with ranking discrepancy: {}'.format(len(fullreviewlist)))

    if len(fullreviewlist) != 0:
        # FOCUSING ON EACH RANK METHOD ONE AT A TIME...
        for focuscol in [col1, col2]:
            print('Focusing on column {} now...'.format(focuscol))
            if focuscol == col1:
                nonfocuscol = col2
                inacclist = col1inacclist
            elif focuscol == col2:
                nonfocuscol = col1
                inacclist = col2inacclist

            # COMPARE THE FOCUS STOCK WITH ANOTHER AND RECORD ACCURACY UNTIL INACCURATE LIST REACHES TARGET LENGTH
            count = 0
            inacclistlen = len(inacclist)
            while inacclistlen < targetinacclen:
                print('Stock no. {} being reviewed now...'.format(count))
                stock1 = fullreviewlist[count]
                print('name of stock being reviewed now: {}'.format(stock1))
                # GET RANKS OF FOCUS STOCK
                focuscolrank = scratchdf[scratchdf['stock'] == stock1][focuscol].iloc[0]
                nonfocuscolrank = scratchdf[scratchdf['stock'] == stock1][nonfocuscol].iloc[0]

                # FIND LIST OF STOCKS THAT WERE RANKED HIGHER THAN IT UNDER NONFOCUSCOL, BUT WORSE THAN IT IN THE FOCUSCOL
                comparedf = rfile.copy()
                betterbutworsedf = comparedf[(comparedf[nonfocuscol] < nonfocuscolrank) & (comparedf[focuscol] >= focuscolrank)].copy()
                print('Number of stocks better but worse than the focused stock: {}'.format(len(betterbutworsedf)))

                if len(betterbutworsedf) >= reviewamount:

                    tallylist = []

                    # SORT DF BY GREATEST DEVIATION INDEX
                    betterbutworsedf['focuscoldiff'] = abs(betterbutworsedf[focuscol] - focuscolrank)
                    betterbutworsedf['nonfocuscoldiff'] = abs(betterbutworsedf[nonfocuscol] - nonfocuscolrank)
                    betterbutworsedf['mostdiffindex'] = betterbutworsedf[['focuscoldiff', 'nonfocuscoldiff']].mean(axis=1)
                    betterbutworsedf.sort_values(ascending=False, by=['mostdiffindex'], inplace=True)
                    betterbutworsedf.reset_index(drop=True, inplace=True)
                    betterbutworselist = betterbutworsedf['stock'].tolist()

                    print('Better but worse review list:')
                    print(betterbutworsedf)
                    # CUT LENGTH OF REVIEWLIST
                    betterbutworselist = betterbutworselist[0:reviewamount]

                    # FOR EACH STOCK IN COMPARELIST...
                    for compstock in betterbutworselist:

                        # was the compstock actually better than this stock? if so tally
                        firstticker = stock1
                        secondticker = compstock

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

                                # GET RANKS OF THE COMPSTOCK
                                compfocuscolrank = scratchdf[scratchdf['stock'] == secondticker][focuscol].iloc[0]
                                compnonfocuscolrank = scratchdf[scratchdf['stock'] == secondticker][nonfocuscol].iloc[0]

                                plt.subplot(2, 2, 1)
                                plt.plot(firsttickerdf2[[priceline.format(firstticker), trajectoryline.format(firstticker)]])
                                plt.suptitle('{}: {} {}: {}     ---    {}: {} {}: {}'.format(focuscol, focuscolrank, nonfocuscol, nonfocuscolrank, focuscol, compfocuscolrank, nonfocuscol, compnonfocuscolrank))
                                plt.title('{} TrueDailyGrowth: {} Sharpe: {}'.format(firstticker, truedailygrowth1, sharpe1))

                                plt.subplot(2, 2, 2)
                                plt.plot(secondtickerdf2[[priceline.format(secondticker), trajectoryline.format(secondticker)]])
                                plt.title('{} TrueDailyGrowth: {} Sharpe: {}'.format(secondticker, truedailygrowth2, sharpe2))

                                ax1 = plt.subplot(2, 2, 3)
                                plt.plot(firsttickerdf2[[deviationline.format(firstticker)]])
                                plt.title('Smooth Score: {}'.format(smoothscore1))

                                plt.subplot(2, 2, 4, sharey=ax1)
                                plt.plot(secondtickerdf2[[deviationline.format(secondticker)]])
                                plt.title('Smooth Score: {}'.format(smoothscore2))
                                plt.show()

                                # ASK WHICH YOU LIKE BETTER:
                                choice = easygui.ynbox('Was {} better than {}? If it is too close to call, choose YES'.format(firstticker, secondticker))

                                if choice is False:
                                    tallylist.append(1)
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

                    # TALLY SCORE AND ADD TO SCORE LIST
                    incorrectscore = np.mean(tallylist)
                    inacclist.append(incorrectscore)

                else:
                    print('Not enough better but worse stocks to obtain an inaccuracy score.  Examining next focus stock available...')
                inacclistlen = len(inacclist)
                print('focuscol: {}. Current Inacclist: {}'.format(focuscol, inacclist))
                if stock1 == fullreviewlist[-1] and inacclistlen < targetinacclen:
                    print('All the available stocks to review were reviewed where the focuscol was {}.  But not enough inaccurate scores have been collected, meaning that there have not been enough review stocks that had stocks that did better than those review stocks in {} but same or worse than them in {}.  This fact inconclusively means that the focuscol: {} correlates with nonfocuscol: {}'.format(focuscol, nonfocuscol, focuscol, focuscol, nonfocuscol))
                    break

                count += 1

    else:
        print('{} and {} have no ranking discrepancies.  It is likely that they are identical in how they function.'.format(col1, col2))

    # CALCULATE INACCURACY SCORES
    if len(col1inacclist) == 0:
        col1inaccscore = 0
    else:
        col1inaccscore = np.mean(col1inacclist)
    if len(col2inacclist) == 0:
        col2inaccscore = 0
    else:
        col2inaccscore = np.mean(col2inacclist)

    # PRESENT RESULTS
    print('{} stocks reviewed per method'.format(targetinacclen))
    print('{} and {} methods were compared'.format(col1, col2))
    print('Each stock was compared to {} benchmark stocks (those stocks that did better in the other method but worse in the method focused on)'.format(reviewamount))
    print('Inaccuracy criteria: sharpe ratio (baremin_geodgr / mmbm_smoothscore)')
    print('INACCURACY RATE OF {}: {}'.format(col1, col1inaccscore))
    print('INACCURACY RATE OF {}: {}'.format(col2, col2inaccscore))

    return col1inaccscore, col2inaccscore


def rankmethods(testsample, targetinacclen, reviewamount, viewmod, reviewtype, rankcols, dataloc):

    if rankcols == '':
        # GET RANK COLUMNS
        rfile = testsample.rankingfile()
        allcols = list(rfile.columns)
        rankcols = []
        for item in allcols:
            if item.find('RANK') != -1:
                rankcols.append(item)
    else:
        rankcols = rankcols

    # GET ALL POSSIBLE PAIRS OF rankcols
    allpairs = []
    inaccdict = {}
    for item in rankcols:
        # GET INDEX OF CURRENT ITEM
        curritemindex = rankcols.index(item)
        # IF CURRENT ITEM IS NOT THE LAST ITEM...
        if curritemindex != rankcols.index(rankcols[-1]):
            newlist = rankcols[curritemindex+1:]
            for elem in newlist:
                allpairs.append([item, elem])

        # CREATE DICTIONARY FOR INACCURACY SCORES
        inaccdict.update({item: 0})

    for pair in allpairs:
        print('CURRENT PAIR: {} AND {}...'.format(pair[0], pair[1]))
        col1 = pair[0]
        col2 = pair[1]

        # RETRIEVE CURRENT SCORES
        col1currscore = inaccdict[col1]
        col2currscore = inaccdict[col2]

        # RETRIEVE ADDITIONAL SCORES
        col1inaccscore, col2inaccscore = comparetworanks(testsample, col1, col2, targetinacclen, reviewamount, viewmod, reviewtype, dataloc)

        # UPDATE INACC SCORES
        col1update = col1currscore + col1inaccscore
        col2update = col2currscore + col2inaccscore
        inaccdict.update({col1: col1update, col2: col2update})
        print(inaccdict)
        print('\n')

    # CALCULATE AVERAGE INACC SCORE
    num_trials = len(rankcols) - 1
    for key in inaccdict:
        inaccdict.update({key: (inaccdict[key] / num_trials)})
    inaccdf = pd.DataFrame.from_dict(inaccdict, orient='index')
    inaccdf.sort_values(ascending=True, by=0, inplace=True)
    inaccdf.rename(columns={0: 'INACCURACY RATE'}, inplace=True)

    print(inaccdf)
