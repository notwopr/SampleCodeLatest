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
import scipy
import numpy as np
from scipy import stats
#   LOCAL APPLICATION IMPORTS
from Modules.price_calib_cruncher import oldbaremin_cruncher, baremax_cruncher
from newbacktest.ingredients_funclib.STRATTEST_FUNCBASE import allpctchanges
from newbacktest.ingredients_funclib.STRATTEST_FUNCBASE_RAW import getallseglens, slopescore_single, resampledslopescore_single, selectsampfreqslopescore_single, allsampfreqslopescore_single, slopescorefocus_single
from Modules.price_calib import add_calibratedprices
from Modules.price_history_slicing import pricedf_daterange, trimdfbydate
from newbacktest.baking.curvetype import CurveType
from newbacktest.datasource import DataSource
from newbacktest.dataframe_operations import DataFrameOperations


# calc stat on price series
def getstatval(priceseries, stat_type):
    if stat_type == 'mean':
        statval = priceseries.mean()
    elif stat_type == 'median':
        statval = priceseries.median()
    elif stat_type == 'avg':
        statval = np.mean([priceseries.mean(), priceseries.median()])
    elif stat_type == 'min':
        statval = priceseries.min()
    elif stat_type == 'max':
        statval = priceseries.max()
    elif stat_type == 'std':
        statval = priceseries.std()
    elif stat_type == 'mad':
        statval = scipy.stats.median_abs_deviation(priceseries)#priceseries.mad()
    elif stat_type == 'dev':
        statval = np.mean([priceseries.std(), scipy.stats.median_abs_deviation(priceseries)])#priceseries.mad()])
    return statval


# RETURNS fatpct given two columns to compare but scaled to idealcol
def unifatshell_single(focuscol, idealcol, stat_type, seriesdata):
    focuscolseries = seriesdata if focuscol == 'raw' else CurveType().transform(seriesdata, 0, focuscol, 'removeall')
    idealcolseries = seriesdata if idealcol == 'raw' else CurveType().transform(seriesdata, 0, idealcol, 'removeall')
    return getstatval(abs(focuscolseries - idealcolseries) / idealcolseries, stat_type)


# (unifatscore_rawbareminraw_avg + unifatscore_rawbareminraw_dev)
def unifatvolscorebmin_single(seriesdata):
    return unifatshell_single('raw', 'baremin', 'avg', seriesdata) + unifatshell_single('raw', 'baremin', 'dev', seriesdata)


# Slopescore / (unifatscore_rawbareminraw_avg + unifatscore_rawbareminraw_dev)
def slopetounifatratiobmin_single(seriesdata):
    numerator = slopescorefocus_single(seriesdata)
    denominator = unifatvolscorebmin_single(seriesdata)
    if denominator != 0:
        return numerator / abs(denominator)
    else:
        return np.nan


# get nonzerodrops
def getnonzerodrops(upperseries, lowerseries):
    droparr = (lowerseries - upperseries) / upperseries
    return droparr[droparr < 0]


# get pct drop samples; use raw calibration only
def getdropstat_single(nonzerodrops, stat_type, seriesdata):
    if stat_type == 'prev':  # prev=prevalence
        return len(nonzerodrops) / len(seriesdata)
    else:
        if len(nonzerodrops) != 0:
            return getstatval(nonzerodrops, stat_type)
        else:
            return 0


# get pct drop samples; use raw calibration only
def allpctdrops_single(uppercol, lowercol, stat_type, seriesdata):
    lowerseries = seriesdata if lowercol == 'raw' else CurveType().transform(seriesdata, 0, lowercol, 'removeall')
    upperseries = seriesdata if uppercol == 'raw' else CurveType().transform(seriesdata, 0, uppercol, 'removeall')
    nonzerodrops = getnonzerodrops(upperseries, lowerseries)
    return getdropstat_single(nonzerodrops, stat_type, seriesdata)


# calc dropscore (dropprev * dropmag)
def dropscore_single(uppercol, lowercol, seriesdata):
    lowerseries = seriesdata if lowercol == 'raw' else CurveType().transform(seriesdata, 0, lowercol, 'removeall')
    upperseries = seriesdata if uppercol == 'raw' else CurveType().transform(seriesdata, 0, uppercol, 'removeall')
    nonzerodrops = getnonzerodrops(upperseries, lowerseries)
    dropprevalence = getdropstat_single(nonzerodrops, 'prev', seriesdata)
    dropmag = getdropstat_single(nonzerodrops, 'avg', seriesdata)
    return dropprevalence * dropmag


# ratio of stock dropscore / bench dropscore
def dropscoreratio_single(benchticker, uppercol, lowercol, invest_startdate, seriesdata):
    stockds = dropscore_single(uppercol, lowercol, seriesdata)
    ds = DataSource().opends('eodprices_bench')
    ds = DataFrameOperations().filter_bycolandrow_single(ds, '<=', invest_startdate, 'date', [benchticker])
    benchseriesuntrimmed = ds[benchticker]
    benchseriesdata = CurveType().transform(benchseriesuntrimmed, len(seriesdata)-1, 'raw', 'ffillandremove')

    benchds = dropscore_single(uppercol, lowercol, benchseriesdata)
    return 1 if benchds == 0 else stockds / benchds


'''UNREVISED CODE'''


# RETURNS fatpct given two columns to compare
def fatarea_single(prices, uppercol, lowercol, datarangecol):
    focalarea = abs(prices[uppercol] - prices[lowercol]).sum()
    totaldatarange = prices[datarangecol].max() - prices[datarangecol].min()
    totalarea = totaldatarange * len(prices)
    return 0 if totalarea == 0 else focalarea / totalarea


# same as unifatshell except numerator is raw, no absolute value
def unifatshellraw_single(prices, focuscol, idealcol, stat_type):
    return getstatval((prices[focuscol] - prices[idealcol]) / prices[idealcol], stat_type)



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


# growth / loss per unit time
def slopeoverlosspertime_single(prices, stock, stat_type, combtype):
    numerator = slopescore_single(prices)
    denominator = allpctdrops_single(prices, stock, 'oldbareminraw', stat_type)
    if combtype == 'ratio':
        answer = numerator / abs(denominator)
    elif combtype == 'sum':
        answer = numerator + denominator
    return answer


# (unifatscore_rawbaremaxraw_avg + unifatscore_rawbaremaxraw_dev)
def unifatvolscore_single(prices, focuscol):
    prices.reset_index(drop=True, inplace=True)
    answer = unifatshell_single(prices, focuscol, 'baremaxraw', 'avg') + unifatshell_single(prices, focuscol, 'baremaxraw', 'dev')
    return answer


# Slopescore / (unifatscore_rawbaremaxraw_avg + unifatscore_rawbaremaxraw_dev)
def slopetounifatratio_single(prices, focuscol):
    prices.reset_index(drop=True, inplace=True)
    numerator = slopescorefocus_single(prices, focuscol)
    # get unifatscore metrics
    denominator = unifatvolscore_single(prices, focuscol)
    if denominator != 0:
        answer = numerator / abs(denominator)
    else:
        answer = None
    return answer


# Slopescore / dropscore
def slopetodropscoreratio_single(prices, focuscol):
    prices.reset_index(drop=True, inplace=True)
    numerator = slopescorefocus_single(prices, focuscol)
    # get dropscore metric
    denominator = dropscore_single(prices, 'baremaxraw', focuscol, 'avg')
    if denominator != 0:
        answer = numerator / abs(denominator)
    else:
        answer = None
    return answer


# growth / loss per unit time
def growthtoloss_single(prices, stock, groparams, lossparams, combtype):
    prices.reset_index(drop=True, inplace=True)
    # choose growth method
    if groparams['gmeth'] == 'slopescore':
        if groparams['focuscol'] == 'rawprice':
            focuscol = stock
        else:
            focuscol = groparams['focuscol']
        numerator = slopescorefocus_single(prices, focuscol)
    elif groparams['gmeth'] == 'resampslopescore':
        numerator = resampledslopescore_single(prices, groparams['resamplefreq'], groparams['aggtype'])
    elif groparams['gmeth'] == 'selectsampfreqslopescore':
        numerator = selectsampfreqslopescore_single(prices, groparams['aggtype'], groparams['agg2type'], groparams['freqlist'])
    elif groparams['gmeth'] == 'allsampfreqslopescore':
        numerator = allsampfreqslopescore_single(prices, groparams['aggtype'], groparams['agg2type'])
    # choose loss method
    if lossparams['lmeth'] == 'allpctdrop':
        if lossparams['uppercol'] == 'rawprice':
            uppercol = stock
        else:
            uppercol = lossparams['uppercol']
        if lossparams['lowercol'] == 'rawprice':
            lowercol = stock
        else:
            lowercol = lossparams['lowercol']
        # get calibrated prices if needed
        prices = add_calibratedprices(prices, lossparams['allcalibrations'], stock)
        denominator = allpctdrops_single(prices, uppercol, lowercol, lossparams['stat_type'])
    elif lossparams['lmeth'] == 'unifatscore':
        if lossparams['focuscol'] == 'rawprice':
            focuscol = stock
        denominator = unifatshell_single(prices, lossparams['idealcol'], focuscol, lossparams['stat_type'])
    if combtype == 'ratio':
        if denominator != 0:
            answer = numerator / abs(denominator)
        else:
            answer = None
    elif combtype == 'sum':
        answer = numerator + denominator
    return answer


# rolling growth / loss per unit time
def rollgrowthtoloss_single(prices, stock, win_len, agg_type, groparams, lossparams, combtype):
    age = len(prices) - 1
    if age <= win_len:
        answer = growthtoloss_single(prices, stock, groparams, lossparams, combtype)
    else:
        prices['rolling'] = prices.index.map(lambda x: growthtoloss_single(prices.iloc[x:x+win_len, :].copy(), stock, groparams, lossparams, combtype) if x < len(prices)-(win_len-1) else None)
        # AGGREGATE ALL WINDOW RESULTS
        if agg_type == 'mean':
            answer = prices['rolling'].mean()
        elif agg_type == 'median':
            answer = prices['rolling'].median()
        elif agg_type == 'avg':
            answer = np.mean([prices['rolling'].mean(), prices['rolling'].median()])
        elif agg_type == 'std':
            answer = prices['rolling'].std()
        elif agg_type == 'mad':
            answer = prices['rolling'].mad()
        elif agg_type == 'dev':
            answer = np.mean([prices['rolling'].std(), prices['rolling'].mad()])
    return answer


# smoothsqueeze metric cruncher
def smoothsqueeze_cruncher(pricearr, diffarr, stat_type):
    maxsamp = np.max(pricearr)
    minsamp = np.min(pricearr)
    if minsamp != maxsamp:
        if stat_type == 'area':
            ssans = np.sum(diffarr) / ((maxsamp - minsamp) * len(pricearr))
        else:
            diffarr = diffarr / (maxsamp - minsamp)
            if stat_type == 'mean':
                ssans = np.mean(diffarr)
            elif stat_type == 'median':
                ssans = np.median(diffarr)
            elif stat_type == 'avg':
                ssans = np.mean([np.mean(diffarr), np.median(diffarr)])
            elif stat_type == 'std':
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
        bigjump_prev = 0
    else:
        bigjump_prev = len(allbigs) / len(daily_changes)
    return bigjump_prev


# bigjump magnitude
def bigjumpmag_single(daily_changes, bigjumpstrength):
    allbigs = getallbigjumps(daily_changes, bigjumpstrength)
    # if no blips
    if len(allbigs) == 0:
        bigjump_mag = 1
    else:
        # get all nonbigjumps
        nonbigs = [item for item in daily_changes if item not in allbigs and item > 0]
        bigjump_mag = np.mean(allbigs) / np.mean(nonbigs)
    return bigjump_mag


# bigjump mag * prev
def bigjumpscore_single(daily_changes, bigjumpstrength):
    # get bigjump_mag
    bigjump_mag = bigjumpmag_single(daily_changes, bigjumpstrength)
    # get bigjump_prev
    bigjump_prev = bigjumpprev_single(daily_changes, bigjumpstrength)
    return bigjump_mag * bigjump_prev
