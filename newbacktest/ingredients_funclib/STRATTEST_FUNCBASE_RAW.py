"""
Title: Layercake - Function Database - Raw Functions
Date Started: Apr 5, 2020
Version: 2.00
Version Start Date: Jan 2, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: The raw metrics.

Version Notes:
1.01: Added marketbeater submethod for filterandlayer method.
1.02: Add maxflatlitmus metric.
1.03: Revise litmus metric into 1 or 0 switch.
2: Simplify all related dpc functions into one.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import operator
import math
#   THIRD PARTY IMPORTS
import numpy as np
from scipy import stats
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from Modules.dates import DateOperations
from Modules.price_history import grabsinglehistory
from Modules.price_history_fillgaps import fill_gaps2
from newbacktest.ingredients_funclib.STRATTEST_FUNCBASE import cleanchanges
from Modules.growthcalcbot import removeleadingzeroprices
from newbacktest.growthcalculator import GrowthCalculator


# slopescore but custom choose column
def slopescorefocus_single(seriesdata):
    age = age_single(seriesdata)
    # if first price is zero, get first nonzero price
    seriesdata = GrowthCalculator().replaceleadzeros(seriesdata)
    firstp = globalvalgrab_single('first', seriesdata)
    lastp = globalvalgrab_single('last', seriesdata)
    # # if first price is zero, get first nonzero price
    # i = 1
    # while firstp == 0 and i < len(seriesdata):
    #     firstp = prices.iloc[i][focuscol]
    #     i += 1
    if firstp != 0 and age != 0:
        return ((lastp/firstp) ** (1 / age)) - 1
    else:
        return 0


def globalvalgrab_single(valtype, seriesdata):
    '''
    get min/max/first/last val of a series
    '''
    if valtype == 'min':
        return seriesdata.min()
    elif valtype == 'max':
        return seriesdata.max()
    elif valtype == 'first':
        # return seriesdata.iloc[0]
        '''if the series contains no data return nan otherwise return first non-nan value'''
        s = seriesdata.loc[~seriesdata.isnull()]
        return np.nan if not s.any() else s.iloc[0]

    elif valtype == 'last':
        # return seriesdata.iloc[-1]
        '''if the series contains no data return nan otherwise return last non-nan value'''
        s = seriesdata.loc[~seriesdata.isnull()]
        return np.nan if not s.any() else s.iloc[-1]


def valdiff_single(firstval, secondval, seriesdata):
    return globalvalgrab_single(secondval, seriesdata) - globalvalgrab_single(firstval, seriesdata)


def drawdown_to_ipotoathdiff_single(seriesdata):
    drawdowndiff = valdiff_single('last', 'max', seriesdata)
    ipotoathdiff = valdiff_single('first', 'max', seriesdata)
    if ipotoathdiff == 0:
        return np.nan
    return drawdowndiff / ipotoathdiff


# get pctchange between two dates:
def getpctchange_single(seriesdata):

    firstp = globalvalgrab_single('first', seriesdata)
    lastp = globalvalgrab_single('last', seriesdata)
    try:
        if firstp != 0 and not np.isnan(firstp) and not np.isnan(lastp):
            return (lastp - firstp) / firstp
        else:
            return np.nan
    except TypeError:
        print(seriesdata)
        print(firstp)


def xtoathdiff_single(compmode, seriesdata):
    if compmode == 'last':
        '''get pct difference between last val and ATH val'''
        topval = globalvalgrab_single('last', seriesdata)
        botval = globalvalgrab_single('max', seriesdata)
    elif compmode == 'first':
        '''get pct difference between first val and ATH val'''
        topval = globalvalgrab_single('max', seriesdata)
        botval = globalvalgrab_single('first', seriesdata)
    if any([np.isnan(topval), np.isnan(botval)]):
        return np.nan
    return (topval - botval) / botval


def getvalindex_occurcandidates_single(valtype, seriesdata):
    '''# returns all candidates for type of price specified'''
    return seriesdata[seriesdata == globalvalgrab_single(valtype, seriesdata)].index


def getvalindex_single(valtype, occurtype, seriesdata):
    '''# returns indice values of the type of occurrence of type of val specified'''
    if valtype == 'first':
        return seriesdata.index.iloc[0]
    elif valtype == 'last':
        return seriesdata.index.iloc[-1]
    else:
        hits = getvalindex_occurcandidates_single(valtype, seriesdata)
        if occurtype == 'first':
            return hits[0]
        elif occurtype == 'last':
            return hits[-1]


def xtoathduration_single(occurtype, compmode, seriesdata):
    athageindex = getvalindex_single('max', occurtype, seriesdata)
    if compmode == 'first':
        return len(seriesdata.loc[:athageindex]) - 1
    elif compmode == 'last':
        return len(seriesdata.loc[athageindex:]) - 1


def xtoathslope_single(occurtype, compmode, seriesdata):
    '''get slope between ATH val and xval'''
    duration = xtoathduration_single(occurtype, compmode, seriesdata)
    if any([np.isnan(duration), duration == 0]):
        return np.nan
    xtoathdiff = xtoathdiff_single(compmode, seriesdata)
    return ((1 + xtoathdiff) ** (1 / duration)) - 1


def xtoathtoageratio_single(occurtype, compmode, seriesdata):
    xtoath = xtoathduration_single(occurtype, compmode, seriesdata)
    age = age_single(seriesdata)
    if age == 0:
        return np.nan
    return xtoath / age


def currtoathslope_to_ipotoathslope(occurtype, seriesdata):
    slope_ipotoath = xtoathslope_single(occurtype, 'first', seriesdata)
    slope_currtoath = xtoathslope_single(occurtype, 'last', seriesdata)
    if slope_ipotoath == 0:
        return np.nan
    return abs(slope_currtoath) / slope_ipotoath


# AGE
def age_single(seriesdata):
    return len(seriesdata) - 1


def getallseglens(seriesdata, seglenmode):
    '''gives an array of lengths of segments in a time-series.  if mode e.g. is positive, it will give you the segment lengths of consecutive positive daily pct-changes over the entire series. if the mode is flat, it will return the lengths of all flat segments in the time-series.'''
    allseglens = []
    single_seg = 0
    # FOR EACH CHANGE...
    # count = 0
    for sample in seriesdata:
        # IF SAMPLE IS POS/NEG/FLAT, ADD TO TALLY
        if seglenmode == 'positive':
            condstat = operator.gt(sample, 0)
        elif seglenmode == 'negative':
            condstat = operator.lt(sample, 0)
        elif seglenmode == 'flat':
            condstat = operator.eq(sample, 0)
        if condstat is True:
            single_seg += 1
        # IF SAMPLE IS NOT POS/NEG/FLAT,
        else:
            # CLOSE TALLY AND SAVE
            if single_seg > 0:
                allseglens.append(single_seg)
            # RESET TALLY TO ZERO
            single_seg = 0
        # count += 1
    # IF REACH END OF ALL SAMPLES, RECORD LAST TALLY IF ANY
    if single_seg > 0:
        allseglens.append(single_seg)
    # IF NO POS/NEG/FLAT SEGS FOUND, RETURN LIST WITH VALUE OF ZERO
    return [0] if len(allseglens) == 0 else allseglens


# get avg/mean/median/max pos/neg/flat seg len
def statseglen_single(seglenmode, stat_type, seriesdata):
    if stat_type == 'mean':
        return np.mean(getallseglens(seriesdata, seglenmode))
    elif stat_type == 'median':
        return np.median(getallseglens(seriesdata, seglenmode))
    elif stat_type == 'avg':
        meanseglen = np.mean(getallseglens(seriesdata, seglenmode))
        medianseglen = np.median(getallseglens(seriesdata, seglenmode))
        return np.mean([medianseglen, meanseglen])
    elif stat_type == 'max':
        return np.max(getallseglens(seriesdata, seglenmode))
    elif stat_type == 'min':
        return np.min(getallseglens(seriesdata, seglenmode))
    elif stat_type == '1q':
        return np.quantile(getallseglens(seriesdata, seglenmode), .25)
    elif stat_type == '3q':
        return np.quantile(getallseglens(seriesdata, seglenmode), .75)
    elif stat_type == 'std':
        return np.std(getallseglens(seriesdata, seglenmode))
    elif stat_type == 'mad':
        return stats.median_abs_deviation(getallseglens(seriesdata, seglenmode))
    elif stat_type == 'dev':
        stdseglen = np.std(getallseglens(seriesdata, seglenmode))
        madseglen = stats.median_abs_deviation(getallseglens(seriesdata, seglenmode))
        return np.mean([stdseglen, madseglen])
    elif stat_type == 'sum':
        return np.sum(getallseglens(seriesdata, seglenmode))


'''UNEDITED CODE'''
# returns all candidates for type of price specified
def getpricedate_occurcandidates_single(prices, stock, pricetype):
    return prices[prices[stock] == globalpricegrab_single(prices, stock, pricetype)]['date']


# returns date of the type of occurrence of type of price specified
def getpricedate_single(prices, stock, pricetype, occurtype):
    if pricetype == 'first':
        return prices['date'].iloc[0]
    elif pricetype == 'last':
        return prices['date'].iloc[-1]
    else:
        hits = getpricedate_occurcandidates_single(prices, stock, pricetype)
        if occurtype == 'first':
            return hits.iloc[0] if len(hits) > 1 else hits.item()
        elif occurtype == 'last':
            return hits.iloc[-1] if len(hits) > 1 else hits.item()


# get ratio of global min price to ipo price
def atltoipo_single(prices, stock):
    # get global min price
    minprice = globalpricegrab_single(prices, stock, 'min')
    # get ipo price
    ipoprice = globalpricegrab_single(prices, stock, 'first')
    # get ratio
    return minprice / ipoprice



# get num days between current price and most recent ATH
def currtoathdays_single(prices, stock, ath_occur):
    currdate = getpricedate_single(prices, stock, 'last', 'last')
    athdate = getpricedate_single(prices, stock, 'max', ath_occur)
    return DateOperations().num_days(athdate, currdate)



# CALCULATE POS NEG AREA BETWEEN TWO NORMALIZED GRAPHS
def posnegarea(prices, stock1, stock2):
    # pull up stock history of desired time period
    prices.reset_index(inplace=True, drop=True)
    # pull up same of comparison stock
    stock2prices = grabsinglehistory(stock2)
    stock2prices = fill_gaps2(stock2prices, '', '')
    # join stock2 to stock1
    prices = prices.join(stock2prices.set_index('date'), how="left", on="date")
    # normalize prices
    firstp = prices.loc[0, [stock1, stock2]]
    prices[[stock1, stock2]] = (prices[[stock1, stock2]] - firstp) / firstp
    prices['marginarea'] = prices[stock1] - prices[stock2]
    allmarginvals = prices['marginarea'].tolist()
    pos_samp = [item for item in allmarginvals if item > 0]
    if len(pos_samp) != 0:
        posarea = np.sum(pos_samp)
    else:
        posarea = 0
    neg_samp = [abs(item) for item in allmarginvals if item < 0]
    if len(neg_samp) != 0:
        negarea = np.sum(neg_samp)
    else:
        negarea = 0
    return posarea, negarea


# $ earned per day
def dollarsperday_single(prices, stock):
    slopescore = slopescore_single(prices)
    currprice = globalpricegrab_single(prices, stock, 'last')
    dollarsperday = currprice * slopescore
    return dollarsperday


# PRICE TO AGE RATIO
def paratio_single(prices, stock):
    age = len(prices) - 1
    currprice = globalpricegrab_single(prices, stock, 'last')
    paratio = currprice / age
    return paratio


# CALCULATE WHETHER MORE POS THAN NEG AREA
def posareamargin_single(prices, stock1, stock2):
    posarea, negarea = posnegarea(prices, stock1, stock2)
    posareamargin = posarea - negarea
    return posareamargin


# CALCULATE PERCENTAGE OF POSNEGAREA IS POSITIVE
def posareapct_single(prices, stock1, stock2):
    posarea, negarea = posnegarea(prices, stock1, stock2)
    if posarea != 0:
        pospct = posarea / (posarea + negarea)
    else:
        pospct = 0
    return pospct


# GET PREVALENCE TRENDS
def prevalence_cruncher_pos(array):
    # separate pctdailychange data into positive and negative samples
    pos_samps = array[array > 0]
    # get proportion positive and proportion negative
    pct_pos = len(pos_samps) / len(array)
    return pct_pos


def prevalence_cruncher_neg(array):
    # separate pctdailychange data into positive and negative samples
    neg_samps = array[array < 0]
    # get proportion positive and proportion negative
    pct_neg = len(neg_samps) / len(array)
    return pct_neg


# calculates rolling average of the proportion of pctchanges that is pos/neg
def prevalencetrend_single(prices, stock, changewinsize, changetype):
    # get changerate data
    changeratedata = prices[stock].pct_change(periods=changewinsize, fill_method='ffill')
    all_changes = changeratedata.tolist()
    all_changes = cleanchanges(all_changes)
    rollingwinsize = math.floor(0.25 * len(all_changes))
    if rollingwinsize >= 5:
        # changedf
        changedf = pd.DataFrame(data={'all_changes': all_changes})
        # get rolling averages
        if changetype == 'pos':
            changedf['rollpreval'] = changedf.index.map(lambda x: prevalence_cruncher_pos(changedf['all_changes'].iloc[x:x+rollingwinsize].to_numpy()) if x < len(changedf)-(rollingwinsize-1) else None)
        elif changetype == 'neg':
            changedf['rollpreval'] = changedf.index.map(lambda x: prevalence_cruncher_neg(changedf['all_changes'].iloc[x:x+rollingwinsize].to_numpy()) if x < len(changedf)-(rollingwinsize-1) else None)
        allprevals = changedf['rollpreval'].dropna().tolist()
        i = 0
        while allprevals[i] == 0:
            i += 1
        prevalencetrend = (allprevals[-1] - allprevals[0]) / allprevals[i]
    else:
        prevalencetrend = 0
    return prevalencetrend


# RETURN POS OR NEG SAMPLES OF SET OF DAILY PERCENT CHANGES
def getposornegchangesonly(daily_changes, changetype):
    daily_changes = np.array(daily_changes)
    if changetype == 'pos':
        iso_samps = daily_changes[daily_changes > 0]
    elif changetype == 'neg':
        iso_samps = daily_changes[daily_changes < 0]
    return iso_samps


# GET STATS ON SET OF POS OR NEG SAMPLES
def isosampstats(iso_samps, stat_type):
    if len(iso_samps) == 0:
        answer = 0
    else:
        if stat_type == 'mean':
            answer = np.mean(iso_samps)
        elif stat_type == 'median':
            answer = np.median(iso_samps)
        elif stat_type == 'avg':
            mean_val = np.mean(iso_samps)
            median_val = np.median(iso_samps)
            answer = np.mean([mean_val, median_val])
        elif stat_type == 'max':
            answer = np.max(iso_samps)
        elif stat_type == 'min':
            answer = np.min(iso_samps)
        elif stat_type == 'std':
            answer = np.std(iso_samps)
        elif stat_type == 'mad':
            answer = stats.median_abs_deviation(iso_samps)
        elif stat_type == 'dev':
            std_val = np.std(iso_samps)
            mad_val = stats.median_abs_deviation(iso_samps)
            answer = np.mean([std_val, mad_val])
    return answer


# GET AVG CHANGE OF POS/NEG DAILY CHANGES
def posnegmag_single(daily_changes, changetype, stat_type):
    iso_samps = getposornegchangesonly(daily_changes, changetype)
    answer = isosampstats(iso_samps, stat_type)
    return answer


# get ratio of positive mag to negative magnitude
def posnegmagratio_single(daily_changes, stat_type):
    posmag = posnegmag_single(daily_changes, 'pos', stat_type)
    negmag = abs(posnegmag_single(daily_changes, 'neg', stat_type))
    if negmag != 0:
        posnegmagratio = posmag / negmag
    else:
        posnegmagratio = np.inf
    return posnegmagratio


# GET PREVALENCE OF POS/NEG DAILY CHANGES
def posnegprevalence_single(daily_changes, changetype):
    iso_samps = getposornegchangesonly(daily_changes, changetype)
    pct_preval = len(iso_samps) / len(daily_changes)
    return pct_preval


# get ratio of positive prevalence to negative prevalence
def posnegprevratio_single(daily_changes):
    posprev = posnegprevalence_single(daily_changes, 'pos')
    negprev = posnegprevalence_single(daily_changes, 'neg')
    if negprev != 0:
        posnegprevratio = posprev / negprev
    else:
        posnegprevratio = np.inf
    return posnegprevratio


# composite score combining posnegmag and posnegprev
def posnegmagprevscore_single(daily_changes, changetype, stat_type):
    # get all dpc samples of pos or neg kind only
    iso_samps = getposornegchangesonly(daily_changes, changetype)
    # get posnegmag score
    posnegmagscore = isosampstats(iso_samps, stat_type)
    # get posnegprev score
    posnegprevscore = len(iso_samps) / len(daily_changes)
    # calc final index score
    indexscore = posnegmagscore * posnegprevscore
    return indexscore


# GET CHANGERATE TRENDS
def changeratetrend_single(prices, stock, changewinsize, changetype):
    # get changerate data
    changeratedata = prices[stock].pct_change(periods=changewinsize, fill_method='ffill')
    all_changes = changeratedata.tolist()
    all_changes = cleanchanges(all_changes)
    # isolate changetype
    if changetype == 'pos':
        iso_samps = [item for item in all_changes if item > 0]
    elif changetype == 'neg':
        iso_samps = [item for item in all_changes if item < 0]
    if len(iso_samps) != 0:
        rollingwinsize = math.floor(0.25 * len(iso_samps))
        if rollingwinsize >= 5:
            # changedf
            changedf = pd.DataFrame(data={'iso_changes': iso_samps})
            # get rolling averages
            changedf['rollavg'] = changedf['iso_changes'].rolling(rollingwinsize).mean()
            allrollavgs = changedf['rollavg'].dropna().tolist()
            changeratetrend = (allrollavgs[-1] - allrollavgs[0]) / abs(allrollavgs[0])
        else:
            changeratetrend = 0
    else:
        changeratetrend = 0
    return changeratetrend


# $ earned per day per share
def slopescore_single(prices):
    age = len(prices) - 1
    firstp = prices.iat[0, 1]
    lastp = prices.iat[-1, 1]
    # if first price is zero, get first nonzero price
    i = 1
    while firstp == 0 and i < len(prices):
        firstp = prices.iat[i, 1]
        i += 1
    if firstp != 0:
        slopescore = ((lastp/firstp) ** (1 / age)) - 1
    else:
        slopescore = 0
    return slopescore


# slopescore based on desired growth factor (dgf) see metric library for explanation
def dgfslopescore_single(prices, dgf):
    age = len(prices) - 1
    dgfslopescore = ((((age / 365) * dgf) + 1) ** (1 / age)) - 1
    return dgfslopescore


# slopescore litmus
def slopescorelitmus_single(prices, focuscol, dgf):
    dgfslopescore = dgfslopescore_single(prices, dgf)
    actualslopescore = slopescorefocus_single(prices, focuscol)
    # create ratio of actual / ideal slopescore
    return actualslopescore / dgfslopescore


# gives a stock's personalized slopescore minimum requirement to achievement given overall rate
def minslopescore_single(prices, overallrate):
    age = len(prices) - 1
    slopescoremin = (((overallrate * (age / 365)) + 1) ** (1 / age)) - 1
    return slopescoremin


# litmus that determines whether actual slopescore meets minslopescore or not
def actualtominssratio_single(prices, overallrate, focuscol):
    # get minslopescore needed
    minreq = minslopescore_single(prices, overallrate)
    # get actual slopescore
    actual = slopescorefocus_single(prices, focuscol)
    return actual / minreq


# RETURNS THE SLOPESCORE OF A SELECTED SECTION OF HISTORY GIVEN LENGTH AND NUMBER OF SEGLENS BACK FROM PRESENT
def segbackslopescore_single(prices, focuscol, segsback, winlen):
    # get slopescore of selected segment
    index_left = -1 * ((winlen * (1 + segsback)) + 1)
    index_right = -1 * ((winlen * segsback))
    if index_right == 0:
        index_right = None
    samp_prices = prices.iloc[index_left:index_right]
    # if there is no data for that segment, return avg of all avail segs
    if len(samp_prices) < 2:
        # find last seg where data existed
        while len(samp_prices) < 2:
            segsback -= 1
            # get slopescore of selected segment
            index_left = -1 * ((winlen * (1 + segsback)) + 1)
            index_right = -1 * ((winlen * segsback))
            if index_right == 0:
                index_right = None
            samp_prices = prices.iloc[index_left:index_right]
        lastseg = segsback
        # gather all slopescores of each valid seg
        all_slopescores = []
        for segsback in range(lastseg+1):
            index_left = -1 * ((winlen * (1 + segsback)) + 1)
            index_right = -1 * ((winlen * segsback))
            if index_right == 0:
                index_right = None
            samp_prices = prices.iloc[index_left:index_right]
            samp_slopescore = slopescorefocus_single(samp_prices, focuscol)
            all_slopescores.append(samp_slopescore)
        # get mean of all slopescores
        samp_slopescore = np.mean(all_slopescores)
    else:
        samp_slopescore = slopescorefocus_single(samp_prices, focuscol)
    return samp_slopescore


# RETURNS set of ALL SLOPESCORES GIVEN SAMPLING FREQUENCY
def resampledslopescoredata_single(prices, focuscol, resamplefreq):
    # remove leading zero prices
    prices = removeleadingzeroprices(prices, [prices.columns[1]])
    # create array of index bookmarks
    num_rows = len(prices)
    indarr = np.arange(0, num_rows, resamplefreq)
    # add last index if last index is not present in array
    lastindex = prices.index[-1]
    if lastindex != indarr[-1]:
        indarr = np.append(indarr, lastindex)
    # for every bookmark index, get price data in range, calculate slopescore of range and record
    slopescoredata = []
    for inditem in range(len(indarr)-1):
        samp_prices = prices.loc[indarr[inditem]:indarr[inditem+1]]
        samp_slopescore = slopescorefocus_single(samp_prices, focuscol)
        slopescoredata.append(samp_slopescore)
    return slopescoredata


# RETURNS THE AGGREGATE OF ALL SLOPESCORES GIVEN SAMPLING FREQUENCY
def resampledslopescore_single(slopescoredata, aggtype):
    # aggregate slopescore data
    if aggtype == 'mean':
        resampledslopescore = np.mean(slopescoredata)
    elif aggtype == 'median':
        resampledslopescore = np.median(slopescoredata)
    elif aggtype == 'avg':
        resampledslopescore = np.mean([np.mean(slopescoredata), np.median(slopescoredata)])
    elif aggtype == 'std':
        resampledslopescore = np.std(slopescoredata)
    elif aggtype == 'mad':
        resampledslopescore = stats.median_abs_deviation(slopescoredata)
    elif aggtype == 'dev':
        comp1 = np.std(slopescoredata)
        comp2 = stats.median_abs_deviation(slopescoredata)
        resampledslopescore = np.mean([comp1, comp2])
    return resampledslopescore


# ratio of mag_resampss to dev_resampss
def magtodevresampssratio_single(slopescoredata, aggtype_mag, aggtype_dev):
    # get mag resampless
    magresampless = resampledslopescore_single(slopescoredata, aggtype_mag)
    # get mag resampless
    devresampless = resampledslopescore_single(slopescoredata, aggtype_dev)
    return magresampless / devresampless


# aggregate slopescores together
def slopescoreagg(prices, aggcol, agg2type):
    # aggregate slopescore data
    if agg2type == 'mean':
        aggscore = prices[aggcol].mean()
    elif agg2type == 'median':
        aggscore = prices[aggcol].median()
    elif agg2type == 'composite':
        aggscore_mean = prices[aggcol].median()
        aggscore_median = prices[aggcol].mean()
        aggscore = np.mean([aggscore_mean, aggscore_median])
    return aggscore


# RETURNS THE AGGREGATE OF ALL RESAMPLEDSLOPESCORES OF LIST OF GIVEN FREQUENCIES
def selectsampfreqslopescore_single(prices, aggtype, agg2type, freqlist):
    prices['resampledslopescore'] = prices.index.map(lambda x: resampledslopescore_single(prices, x, aggtype) if x in freqlist else None)
    resampledslopescore_selectfreq = slopescoreagg(prices, 'resampledslopescore', agg2type)
    return resampledslopescore_selectfreq


# RETURNS THE AGGREGATE OF ALL RESAMPLEDSLOPESCORES FROM SAMPLEFREQ 1 TO AGE OF STOCK
def allsampfreqslopescore_single(prices, aggtype, agg2type):
    prices['resampledslopescore'] = prices.index.map(lambda x: resampledslopescore_single(prices, x, aggtype) if x > 0 else None)
    resampledslopescore_allfreq = slopescoreagg(prices, 'resampledslopescore', agg2type)
    return resampledslopescore_allfreq


# rolling slopescore
def rollingslopescore_single(prices, focuscol, win_len, agg_type):
    age = len(prices) - 1
    if age <= win_len:
        if agg_type in ['mean', 'median', 'avg']:
            answer = slopescorefocus_single(prices, focuscol)
        elif agg_type in ['std', 'mad', 'dev']:
            answer = 0
    else:
        prices['rolling'] = prices.index.map(lambda x: slopescorefocus_single(prices.iloc[x:x+win_len, :].copy(), focuscol) if x < len(prices)-(win_len-1) else None)
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


def dpc_cruncher_single(dpcdata, mode):
    if mode == 'mean':
        dpcscore = np.mean(dpcdata)
    elif mode == 'median':
        dpcscore = np.median(dpcdata)
    elif mode == 'avg':
        comp1 = np.mean(dpcdata)
        comp2 = np.median(dpcdata)
        dpcscore = np.mean([comp1, comp2])
    elif mode == 'std':
        dpcscore = np.std(dpcdata)
    elif mode == 'mad':
        dpcscore = stats.median_abs_deviation(dpcdata)
    elif mode == 'dev':
        comp1 = np.std(dpcdata)
        comp2 = stats.median_abs_deviation(dpcdata)
        dpcscore = np.mean([comp1, comp2])
    return dpcscore


# dpcavg + dpcdev
def dpc_cruncher_avgdev_single(dpcdata, avgmode, devmode, combmode):
    dpcavg = dpc_cruncher_single(dpcdata, avgmode)
    dpcdev = dpc_cruncher_single(dpcdata, devmode)
    if combmode == 'sum':
        dpcscore = dpcavg + dpcdev
    elif combmode == 'subtract':
        dpcscore = dpcavg - dpcdev
    return dpcscore


# returns pos or neg samples
def filtersamples(allsamps, mode):
    if mode == 'pos':
        filteredsamps = [item for item in allsamps if item > 0]
    elif mode == 'neg':
        filteredsamps = [item for item in allsamps if item < 0]
    return filteredsamps


# GET POSNEGDPC
def dpc_cruncher_posneg_single(dpcdata, statmeth, statmeth2, calcmeth):
    posnegdict = {}
    for signal in ['pos', 'neg']:
        # isolate pos/neg samps
        iso_samps = filtersamples(dpcdata, signal)
        if len(iso_samps) == 0:
            # dpcbase
            if calcmeth == 'posplusneg':
                sampdict = {signal: 0}
            # dpcbase * pctprev
            elif calcmeth == 'xposplusxneg':
                sampdict = {signal: 0}
            # (dpcavg - dpcdev)*pct, (dpcavg + dpcdev)*pct
            elif calcmeth == 'posnegrange':
                sampdict = {
                    f'{signal}_low': 0,
                    f'{signal}_high': 0
                    }
        else:
            # dpcbase
            if calcmeth == 'posplusneg':
                iso_sampval = dpc_cruncher_single(iso_samps, statmeth)
                sampdict = {signal: iso_sampval}
            # dpcbase * pctprev
            elif calcmeth == 'xposplusxneg':
                samp_pct = len(iso_samps) / len(dpcdata)
                iso_sampbase = dpc_cruncher_single(iso_samps, statmeth)
                iso_sampval = iso_sampbase * samp_pct
                sampdict = {signal: iso_sampval}
            # (dpcavg - dpcdev)*pct, (dpcavg + dpcdev)*pct
            elif calcmeth == 'posnegrange':
                samp_pct = len(iso_samps) / len(dpcdata)
                iso_sampval_low = dpc_cruncher_avgdev_single(dpcdata, statmeth, statmeth2, 'subtract') * samp_pct
                iso_sampval_high = dpc_cruncher_avgdev_single(dpcdata, statmeth, statmeth2, 'sum') * samp_pct
                sampdict = {
                    f'{signal}_low': iso_sampval_low,
                    f'{signal}_high': iso_sampval_high
                    }
        posnegdict.update(sampdict)
    # calc score
    if calcmeth != 'posnegrange':
        dpcscore = posnegdict['pos'] + posnegdict['neg']
    else:
        low_comp = posnegdict['pos_low'] + posnegdict['neg_low']
        high_comp = posnegdict['pos_high'] + posnegdict['neg_high']
        dpcscore = np.mean([low_comp, high_comp])
    return dpcscore


# actual dpc to minslopescore ratio
def dpctominssratio_single(prices, overallrate, dpcdata, mode):
    # get actual dpc
    actualdpc = dpc_cruncher_single(dpcdata, mode)
    # get min slopescore
    minreq = minslopescore_single(prices, overallrate)
    return actualdpc / minreq


def flatline_single(daily_changes):
    # GET PROPORTION OF DAYS WHERE CHANGE WAS ZERO
    zerodaylist = [item for item in daily_changes if item == 0]
    if len(daily_changes) != 0:
        flatlinescore = len(zerodaylist) / len(daily_changes)
    else:
        flatlinescore = np.nan
    return flatlinescore


# get avg/mean/median/max pos/neg/flat seg to life ratios
def segliferatio_single(daily_changes, mode, stat_type):
    age = len(daily_changes)
    statseglen = statseglen_single(daily_changes, mode, stat_type)
    segliferatio = statseglen / age
    return segliferatio


# get ratio of positive seg len to negative seglen
def psegnegsegratio_single(daily_changes, stat_type):
    pseglen = statseglen_single(daily_changes, 'positive', stat_type)
    negseglen = statseglen_single(daily_changes, 'negative', stat_type)
    if negseglen != 0:
        psegnegsegratio = pseglen / negseglen
    else:
        psegnegsegratio = np.inf
    return psegnegsegratio


# get prev proportion of pos/neg consec segs to total set of consec segs
def consecsegprev_single(daily_changes, numer_type):
    totalconsecpseg = statseglen_single(daily_changes, 'positive', 'sum')
    totalconsecnegseg = statseglen_single(daily_changes, 'negative', 'sum')
    if numer_type == 'neg':
        numerator = totalconsecnegseg
    elif numer_type == 'pos':
        numerator = totalconsecpseg
    if totalconsecpseg + totalconsecnegseg != 0:
        consecsegprev = numerator / (totalconsecpseg + totalconsecnegseg)
    else:
        consecsegprev = None
    return consecsegprev


# psegnegsegratio * posnegmagratio * posnegprevratio
def posnegratioproduct_single(daily_changes, nonzerosamples, stat_type):
    posnegratioproduct = psegnegsegratio_single(nonzerosamples, stat_type) * posnegmagratio_single(daily_changes, stat_type) * posnegprevratio_single(daily_changes)
    return posnegratioproduct


def maxflatlitmus_single(daily_changes, age, thresh_maxratio, thresh_maxseg):

    mflratio = maxflatliferatio_single(daily_changes, age)
    mfseg = maxflatseg_single(daily_changes)
    if mflratio >= thresh_maxratio or mfseg >= thresh_maxseg:
        if mfseg < thresh_maxseg or mflratio < thresh_maxratio:
            return 1
        else:
            return 0
    elif mflratio < thresh_maxratio and mfseg < thresh_maxseg:
        return 1


def flatlinescorelitmus_single(daily_changes, thresh_flatscore, thresh_meanseglen):

    flatlinescore = flatline_single(daily_changes)
    meanseglen = meanflatseglen_single(daily_changes)
    if flatlinescore >= thresh_flatscore or meanseglen >= thresh_meanseglen:
        if meanseglen < thresh_meanseglen or flatlinescore < thresh_flatscore:
            return 1
        else:
            return 0
    elif flatlinescore < thresh_flatscore and meanseglen < thresh_meanseglen:
        return 1


def getstockbenchdpcdf(prices, stock, benchmatrixchangesdf):
    # CALCULATE DAILY PRICE CHANGES
    prices[f'dpc_{stock}'] = prices[stock].pct_change(periods=1, fill_method='ffill')
    # ATTACH BENCHMARKDF TO STOCKDF
    prices = prices.join(benchmatrixchangesdf.set_index('date'), how="left", on="date")
    # DELETE NAN ROW
    prices = prices.iloc[1:, :]
    return prices


def marketbeater_single(prices, stock, benchcols, benchmatrixchangesdf, lbsuffix):
    allbcolresults = {}
    prices = getstockbenchdpcdf(prices, stock, benchmatrixchangesdf)
    # CREATE MARGIN COLUMNS
    num_samps = len(prices)
    margincols = []
    # FOR EACH BENCHMARK COMPARED...
    for bcol in benchcols:
        margincolname = f'margin_{bcol}'
        margincols.append(margincolname)
        # CALCULATE DIFFERENCE BETWEEN STOCK CHANGE AND BENCH CHANGE
        prices[margincolname] = prices[f'dpc_{stock}'] - prices[f'dpc_{bcol}']
        # CALCULATE PROPORTION THAT WAS NEGATIVE AND POSITIVE RESPECTIVELY
        posdf = prices[prices[margincolname] > 0].copy()
        negdf = prices[prices[margincolname] < 0].copy()
        pct_pos = len(posdf) / num_samps
        pct_neg = len(negdf) / num_samps
        # CALCULATE AVERAGE MAGNITUDE OF THOSE DIFFERENCES
        if pct_pos == 0:
            avg_pos = 0
        else:
            avg_pos = posdf[margincolname].mean(axis=0)
        if pct_neg == 0:
            avg_neg = 0
        else:
            avg_neg = negdf[margincolname].mean(axis=0)
        bcolresults = {
            f'{bcol}_pct_pos{lbsuffix}': pct_pos,
            f'{bcol}_pct_neg{lbsuffix}': pct_neg,
            f'{bcol}_avg_pos{lbsuffix}': avg_pos,
            f'{bcol}_avg_neg{lbsuffix}': avg_neg
            }
        allbcolresults.update(bcolresults)
    return allbcolresults


# CALCULATES PROPORTION OF LIFESPAN THAT STOCK BEATS GIVEN BENCHMARK ON DAILY BASIS
def benchbeatpct_single(prices, stock1, stock2):
    stock2prices = grabsinglehistory(stock2)
    stock2prices = fill_gaps2(stock2prices, '', '')
    # join stock2 to stock1
    prices = prices.join(stock2prices.set_index('date'), how="left", on="date")
    prices[[f'dpc_{stock1}', f'dpc_{stock2}']] = prices[[stock1, stock2]].pct_change(periods=1, fill_method='ffill')
    # DELETE NAN ROW
    prices = prices.iloc[1:, :]
    # CALCULATE DIFFERENCE BETWEEN STOCK CHANGE AND BENCH CHANGE
    prices['margin'] = prices[f'dpc_{stock1}'] - prices[f'dpc_{stock2}']
    # CALCULATE PROPORTION THAT WAS POSITIVE
    posmargins = prices[prices['margin'] > 0]
    negmargins = prices[prices['margin'] < 0]
    benchbeatpct = len(posmargins) / (len(negmargins) + len(posmargins))
    return benchbeatpct


def marketbeater_cruncher(prices, stock, bcol, avgtype, usedev):
    margincolname = f'margin_{bcol}'
    # CALCULATE DIFFERENCE BETWEEN STOCK CHANGE AND BENCH CHANGE
    prices[margincolname] = prices[f'dpc_{stock}'] - prices[f'dpc_{bcol}']
    # CALCULATE PROPORTION THAT WAS NEGATIVE AND POSITIVE RESPECTIVELY
    posdf = prices[prices[margincolname] > 0].copy()
    negdf = prices[prices[margincolname] < 0].copy()
    num_samps = len(prices)
    pct_pos = len(posdf) / num_samps
    pct_neg = len(negdf) / num_samps
    # CALCULATE AVERAGE MAGNITUDE OF THOSE DIFFERENCES
    if pct_pos == 0:
        avg_pos = 0
        dev_pos = 0
    else:
        if avgtype == 'mean':
            avg_pos = posdf[margincolname].mean(axis=0)
            dev_pos = posdf[margincolname].std(axis=0)
        elif avgtype == 'median':
            avg_pos = posdf[margincolname].median(axis=0)
            dev_pos = posdf[margincolname].mad(axis=0)
        elif avgtype == 'avg':
            avg_pos = np.mean([posdf[margincolname].mean(axis=0), posdf[margincolname].median(axis=0)])
            dev_pos = np.mean([posdf[margincolname].std(axis=0), posdf[margincolname].mad(axis=0)])
    if pct_neg == 0:
        avg_neg = 0
        dev_neg = 0
    else:
        if avgtype == 'mean':
            avg_neg = negdf[margincolname].mean(axis=0)
            dev_neg = negdf[margincolname].std(axis=0)
        elif avgtype == 'median':
            avg_neg = negdf[margincolname].median(axis=0)
            dev_neg = negdf[margincolname].mad(axis=0)
        elif avgtype == 'avg':
            avg_neg = np.mean([negdf[margincolname].mean(axis=0), negdf[margincolname].median(axis=0)])
            dev_neg = np.mean([negdf[margincolname].std(axis=0), negdf[margincolname].mad(axis=0)])
    if usedev == 'yes':
        bcolscore = ((avg_pos - dev_pos) * pct_pos) + ((avg_neg - dev_neg) * pct_neg)
    else:
        bcolscore = (avg_pos * pct_pos) + (avg_neg * pct_neg)
    return bcolscore


# like orig marketbeater, but instead of averaging rankvalues it uses actual metric values
def marketbeaterv2_single(prices, stock, bweights, benchmatrixchangesdf, avgtype, usedev):
    prices = getstockbenchdpcdf(prices, stock, benchmatrixchangesdf)
    allbcolscores = []
    for bcol, bweight in bweights.items():
        bcolscore = marketbeater_cruncher(prices, stock, bcol, avgtype, usedev)
        allbcolscores.append(bcolscore * bweight)
    marketbeaterscore = np.sum(allbcolscores)
    return marketbeaterscore
