"""
Title: Layercake - Function Database - minmaxbaremin
Date Started: Apr 5, 2020
Version: 2.0
Version Start Date: July 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: This is a script storing all the metrics to choose from for the filter method.  Done to keep things organized.

Version Notes:
1.1: Migrated layercake functions over.
1.2: Split smooth into median and mean.
1.3: Optimize smooth squeeze functions and remove old functions.
2.0: Clean up functions. Remove unused functions.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
#   LOCAL APPLICATION IMPORTS
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher
from STRATTEST_FUNCBASE import allpctchanges
from STRATTEST_FUNCBASE_RAW import getallseglens


# shell function for running unismooth or unisqueeze metrics
def unismoothsqueeze_single(prices, uppercol, lowercol, stat_type):
    prices['diffline'] = (prices[uppercol] - prices[lowercol]) / prices[lowercol]
    if stat_type == 'mean':
        metricscore = prices['diffline'].mean()
    elif stat_type == 'median':
        metricscore = prices['diffline'].median()
    elif stat_type == 'std':
        metricscore = prices['diffline'].std()
    elif stat_type == 'mad':
        metricscore = prices['diffline'].mad()
    return metricscore


# finds diff between uppercol and lowercol for the last date of price df
def dipfinder_single(prices, uppercol, lowercol):
    lastupperval = prices.iloc[-1][uppercol].item()
    lastlowerval = prices.iloc[-1][lowercol].item()
    diplitmus = lastupperval - lastlowerval
    return diplitmus


# finds beginning index of region2 for lastdipbot
def reg2begfinder(prices):
    reg2begindex = -1
    for indmark in range(2, len(prices)+1):
        currindex = indmark*(-1)
        currbmaxprice = prices.iloc[currindex]["baremaxraw"].item()
        lastbmaxprice = prices.iloc[currindex+1]["baremaxraw"].item()
        if currbmaxprice == lastbmaxprice:
            reg2begindex = currindex
        else:
            break
    return reg2begindex


# returns proportion of lifespan region1 makes up
def reg1pct_single(prices, stock):
    # get reg2begindex
    reg2begindex = reg2begfinder(prices)
    # get age
    age = len(prices) - 1
    # get reg2 length
    reg2prices = prices[['date', stock]].iloc[reg2begindex:]
    reg2len = len(reg2prices) - 1
    # get reg1 proportion
    reg1pct = 1 - (reg2len / age)
    return reg1pct


# gets region1/region2 pricedf for lastdipbot
def regprices(prices, stock, reg2begindex, region):
    if region == 'reg1':
        prices = prices[['date', stock]].iloc[:reg2begindex+1]
    elif region == 'reg2':
        prices = prices[['date', stock]].iloc[reg2begindex:]
    prices.reset_index(drop=True, inplace=True)
    return prices


# get length of region2 (last dip period)
def lastdiplen_single(prices, stock):
    # find region2 beg date
    reg2begindex = reg2begfinder(prices)
    # get region2 prices
    reg2prices = regprices(prices, stock, reg2begindex, 'reg2')
    reg2len = len(reg2prices) - 1
    return reg2len


# get quality score for a region for lastdipbot
def getregqualscore(prices, stock, reg2begindex, region):
    # get region prices
    regionprices = regprices(prices, stock, reg2begindex, region)
    # get region uppercol and lowercol prices
    allprices = regionprices[stock].tolist()
    baremaxrawpricelist = baremax_cruncher(allprices)
    regionprices['baremaxraw'] = np.array(baremaxrawpricelist)
    oldbareminrawpricelist = oldbaremin_cruncher(allprices)
    regionprices['oldbareminraw'] = np.array(oldbareminrawpricelist)
    # calculate quality score
    regionqualscore = unismoothsqueeze_single(regionprices, 'baremaxraw', 'oldbareminraw', 'mean')
    return regionqualscore


# get quality score of region
def regqualscore_single(prices, stock, region):
    # find region2 beg date
    reg2begindex = reg2begfinder(prices)
    # get quality scores of region
    regqualscore = getregqualscore(prices, stock, reg2begindex, region)
    return regqualscore


# reg1/reg2 quality ratio
def reg1reg2ratio_single(prices, stock):
    # get quality scores of each region
    reg1qualscore = regqualscore_single(prices, stock, 'reg1')
    reg2qualscore = regqualscore_single(prices, stock, 'reg2')
    # get ratio of two quality scores
    reg1reg2ratio = reg1qualscore / reg2qualscore
    return reg1reg2ratio


# get min max and avg bmaxflat len of region 1
def getreg1stats_single(prices, stock, stat_type):
    # find region2 beg date
    reg2begindex = reg2begfinder(prices)
    # get region 1 prices
    reg1prices = regprices(prices, stock, reg2begindex, 'reg1')
    # get bmaxprices
    allprices = reg1prices[stock].tolist()
    baremaxrawpricelist = baremax_cruncher(allprices)
    reg1prices['baremaxraw'] = np.array(baremaxrawpricelist)
    # get bmax daily changes
    baremaxraw_changes = allpctchanges(reg1prices, 'baremaxraw', 1)
    allbmaxflatsegs = getallseglens(baremaxraw_changes, 'flat')
    # get min bmaxflat > 3
    if stat_type == 'min':
        bmaxflatsegs_gt3 = [item for item in allbmaxflatsegs if item > 3]
        answer = np.min(bmaxflatsegs_gt3)
    elif stat_type == 'avg':
        meanseglen = np.mean(allbmaxflatsegs)
        medianseglen = np.median(allbmaxflatsegs)
        answer = np.mean([medianseglen, meanseglen])
    elif stat_type == 'max':
        answer = np.max(allbmaxflatsegs)
    return answer


# get pct drop samples; use raw calibration only
def allpctdrops_single(prices, uppercol, lowercol, origpricecol, stat_type):
    prices['pctdrops'] = (prices[lowercol] - prices[uppercol])
    nonzerodrops = prices['pctdrops'][prices['pctdrops'] < 0].copy()
    if len(nonzerodrops) != 0:
        if stat_type == 'mean':
            metricscore = nonzerodrops.mean()
        elif stat_type == 'median':
            metricscore = nonzerodrops.median()
        elif stat_type == 'composite':
            metricscore = np.mean([nonzerodrops.mean(), nonzerodrops.median()])
        elif stat_type == 'max':
            metricscore = nonzerodrops.min()
        elif stat_type == 'std':
            metricscore = nonzerodrops.std()
        elif stat_type == 'mad':
            metricscore = nonzerodrops.mad()
        elif stat_type == 'devcomposite':
            metricscore = np.mean([nonzerodrops.std(), nonzerodrops.mad()])
        elif stat_type == 'comp-devcomp':
            metricscore = np.mean([nonzerodrops.mean(), nonzerodrops.median()]) - np.mean([nonzerodrops.std(), nonzerodrops.mad()])
    else:
        metricscore = 0
    return metricscore


# smoothsqueeze metric cruncher
def smoothsqueeze_cruncher(pricearr, diffarr, stat_type):
    maxsamp = np.max(pricearr)
    minsamp = np.min(pricearr)
    if minsamp != maxsamp:
        if stat_type == 'area':
            ssans = np.sum(diffarr) / ((maxsamp - minsamp) * len(pricearr))
        else:
            diffarr = diffarr / (maxsamp - minsamp)
            if stat_type == 'std':
                ssans = np.std(diffarr)
            elif stat_type == 'mad':
                ssans = stats.median_abs_deviation(diffarr)
            elif stat_type == 'devcomposite':
                ssans = np.mean([np.std(diffarr), stats.median_abs_deviation(diffarr)])
    else:
        ssans = 0
    return ssans


# shell function for running smooth or squeeze metrics
def smoothsqueezeshell(prices, uppercol, lowercol, origpricecol, stat_type):
    if stat_type == 'ssratio':
        prices['diff'] = prices[uppercol] - prices[lowercol]
        prices['diffsmooth'] = prices[origpricecol] - prices[lowercol]
        smoothscore = smoothsqueeze_cruncher(prices[origpricecol].to_numpy(), prices['diffsmooth'].to_numpy(), 'area')
        squeezescore = smoothsqueeze_cruncher(prices[origpricecol].to_numpy(), prices['diff'].to_numpy(), 'area')
        if squeezescore != 0:
            metricscore = smoothscore / squeezescore
        else:
            metricscore = 0
    elif stat_type == 'roughnessfactor':
        prices['trueline'] = ((prices[uppercol] - prices[lowercol]) / 2) + prices[lowercol]
        roughnessarea = (abs(prices['trueline'] - prices[origpricecol])).sum()
        totalarea = (prices[origpricecol].max() - prices[origpricecol].min()) * (len(prices) - 1)
        metricscore = roughnessarea / totalarea
    else:
        prices['diff'] = prices[uppercol] - prices[lowercol]
        metricscore = smoothsqueeze_cruncher(prices[origpricecol].to_numpy(), prices['diff'].to_numpy(), stat_type)
    return metricscore


# smoothsqueeze metric cruncher with no inheritance of baregraphs
def rollingss_cruncher(pricearr, ssmode, stat_type):
    maxsamp = np.max(pricearr)
    minsamp = np.min(pricearr)
    if minsamp != maxsamp:
        oldbareminarr = np.array(oldbaremin_cruncher(pricearr))
        if ssmode == 'squeeze':
            baremaxarr = np.array(baremax_cruncher(pricearr))
            diffarr = baremaxarr - oldbareminarr
        elif ssmode == 'smooth':
            diffarr = pricearr - oldbareminarr
        if stat_type in ['std', 'mad', 'devcomposite']:
            diffarr = diffarr / (maxsamp - minsamp)
            if stat_type == 'std':
                ssans = np.std(diffarr)
            elif stat_type == 'mad':
                ssans = stats.median_abs_deviation(diffarr)
            elif stat_type == 'devcomposite':
                ssans = np.mean([np.std(diffarr), stats.median_abs_deviation(diffarr)])
        else:
            ssans = np.sum(diffarr) / ((maxsamp - minsamp) * len(pricearr))
    else:
        ssans = 0
    return ssans


# shell function for running given metric over rolling window
def rollingss_single(prices, win_len, age, stat_type, agg_type, uppercol, lowercol, origpricecol):
    if age <= win_len:
        prices['diff'] = prices[uppercol] - prices[lowercol]
        metricscore = smoothsqueeze_cruncher(prices[origpricecol].to_numpy(), prices['diff'].to_numpy(), stat_type)
    else:
        if 'baremax' in uppercol:
            ssmode = 'squeeze'
        elif origpricecol in uppercol:
            ssmode = 'smooth'
        prices['rolling'] = prices.index.map(lambda x: rollingss_cruncher(prices[origpricecol].iloc[x:x+win_len].to_numpy(), ssmode, stat_type) if x < len(prices)-(win_len-1) else None)
        # AGGREGATE ALL WINDOW RESULTS
        if agg_type == 'mean':
            metricscore = prices['rolling'].mean()
        elif agg_type == 'median':
            metricscore = prices['rolling'].median()
        elif agg_type == 'composite':
            metricscore = np.mean([prices['rolling'].mean(), prices['rolling'].median()])
        elif agg_type == 'std':
            metricscore = prices['rolling'].std()
        elif agg_type == 'mad':
            metricscore = prices['rolling'].mad()
        elif agg_type == 'devcomposite':
            metricscore = np.mean([prices['rolling'].std(), prices['rolling'].mad()])
    return metricscore


# bigjump stats
def getallbigjumps(daily_changes, bigjumpstrength):
    # get nonzero dpc
    allnonzerodpc = [item for item in daily_changes if item > 0]
    # get all blips
    allblips = []
    for iternum in range(1, len(allnonzerodpc)-1):
        prevdpc = allnonzerodpc[iternum-1]
        currdpc = allnonzerodpc[iternum]
        nextdpc = allnonzerodpc[iternum+1]
        if currdpc > prevdpc and currdpc > nextdpc:
            allblips.append(currdpc)
    # if no blips
    if len(allblips) == 0:
        allbigs = []
    else:
        # get big jumps
        allbigs = []
        avgblip = np.median(allblips)
        for blip in allblips:
            if blip / avgblip > bigjumpstrength:
                allbigs.append(blip)
    return allbigs


# bigjump prevalence
def bigjumpprev_single(daily_changes, bigjumpstrength):
    allbigs = getallbigjumps(daily_changes, bigjumpstrength)
    # if no bigjumps
    if len(allbigs) == 0:
        bigjump_preval = 0
    else:
        bigjump_preval = len(allbigs) / len(daily_changes)
    return bigjump_preval


# bigjump magnitude
def bigjumpmag_single(daily_changes, bigjumpstrength):
    allbigs = getallbigjumps(daily_changes, bigjumpstrength)
    # if no blips
    if len(allbigs) == 0:
        bigjump_mag = 1
    else:
        # get all nonbigjumps
        nonbigs = [item for item in daily_changes if item not in allbigs]
        bigjump_mag = np.mean(allbigs) / np.mean(nonbigs)
    return bigjump_mag
