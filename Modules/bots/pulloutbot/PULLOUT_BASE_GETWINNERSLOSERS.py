"""
Title: PULLOUT BOT BASE - PRICE DOWNLOAD FUNCS
Date Started: Dec 4, 2020
Version: 4.00
Version Start: Jan 15, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Versions:
4: consolidate functions to reduce memory usage.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory, add_calibratedprices
from fillgapbot import fill_gaps2
from tickerportalbot import tickerportal2
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, tickerlistcommon_source
from growthcalcbot import removeleadingzeroprices
from STRATTEST_FUNCBASE_MMBM import unifatshell_single, dropscore_single
from filelocations import savetopkl


# get no-leading zero rawprice df of bench and portfolio
def getnoleadingzerorawpricedf(pricematrixdf, benchpricematrixdf, portfolio, benchticker, beg_date, end_date):
    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    all_cols = ['date'] + portfolio
    nonbenchsliced = pricematrixdf[all_cols].copy()
    # PULL BENCH PRICES
    all_bcols = ['date', benchticker]
    benchsliced = benchpricematrixdf[all_bcols].copy()
    # JOIN
    benchsliced = benchsliced.join(nonbenchsliced.set_index('date'), how="left", on="date")
    # SLICE OUT DATE RANGE REQUESTED
    benchsliced = benchsliced.loc[(benchsliced['date'] >= beg_date) & (benchsliced['date'] <= end_date)].copy()
    # RESET INDEX
    benchsliced.reset_index(drop=True, inplace=True)
    # remove leading zeroes from raw prices
    alltickers = portfolio + [benchticker]
    benchsliced = removeleadingzeroprices(benchsliced, alltickers)
    return benchsliced


# CREATES DF OF BENCH AND PORTFOLIO DPC PRICES
def getdpcprices(pricematrixdf, benchpricematrixdf, portfolio, benchticker, beg_date, end_date):
    dpcpricedf = getnoleadingzerorawpricedf(pricematrixdf, benchpricematrixdf, portfolio, benchticker, beg_date, end_date)
    # calculate dpc prices
    alltickers = portfolio + [benchticker]
    dpcpricedf[alltickers] = dpcpricedf[alltickers].pct_change(periods=1, fill_method='ffill')
    return dpcpricedf


# CREATES DF OF BENCH AND PORTFOLIO NORMALIZED PRICES
def getnormprices(pricematrixdf, benchpricematrixdf, portfolio, benchticker, beg_date, end_date):
    normpricesdf = getnoleadingzerorawpricedf(pricematrixdf, benchpricematrixdf, portfolio, benchticker, beg_date, end_date)
    alltickers = portfolio + [benchticker]
    # NORMALIZE EACH PRICE CURVE
    firstp = normpricesdf.loc[0, alltickers]
    normpricesdf[alltickers] = (normpricesdf[alltickers] - firstp) / firstp
    return normpricesdf


def getvolmetricscore(volmetricname, ticker, beg_date, end_date):
    # get prices
    prices = grabsinglehistory(ticker)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(inplace=True, drop=True)
    # get calibrated prices
    if volmetricname == 'unifatscore':
        calibs = ['baremaxraw']
        metricvars = (ticker, 'baremaxraw', 'avg')
        metricfunc = unifatshell_single
    elif volmetricname == 'dropscore':
        calibs = ['baremaxraw']
        metricvars = ('baremaxraw', ticker, 'avg')
        metricfunc = dropscore_single
    # calculate volmetricscore
    prices = add_calibratedprices(prices, calibs, ticker)
    volmetricscore = metricfunc(prices, *metricvars)
    return volmetricscore


# get winner/loser by volatility metric function
def getgroupbyvolmetricfunc(pool, key, val, benchticker, bencherr, test_beg, test_end):
    # set volmetric func to run
    if key == 'max_unifatscore' or key == 'min_unifatscore':
        volmetricname = 'unifatscore'
    elif key == 'max_dropscore' or key == 'min_dropscore':
        volmetricname = 'dropscore'
    # set threshold value
    if val == 'bench':
        benchval = getvolmetricscore(volmetricname, benchticker, test_beg, test_end)
        thresherr = benchval * bencherr
        if key.startswith('max'):
            threshval = benchval + thresherr
        elif key.startswith('min'):
            threshval = benchval - thresherr
    else:
        threshval = val
    # add stock to group if meet threshold requirement
    targetpool = []
    for stock in pool:
        # get volmetric score of stock
        stockval = getvolmetricscore(volmetricname, stock, test_beg, test_end)
        if key == 'max_unifatscore' or key == 'max_dropscore':
            if stockval < threshval:
                targetpool.append(stock)
        elif key == 'min_unifatscore' or key == 'min_dropscore':
            if stockval > threshval:
                targetpool.append(stock)
    return targetpool


# define winner/loser
def winnerloserdefiner(startingpool, groupdefinition, normpricesdf, benchticker, test_beg, test_end):
    targetpool = startingpool
    for key, val in groupdefinition.items():
        if key == 'beatbench':
            if val == 'yes':
                targetpool = normpricesdf[targetpool].columns[(normpricesdf.iloc[-1][targetpool] > normpricesdf.iloc[-1][benchticker])].tolist()
            elif val == 'no':
                targetpool = normpricesdf[targetpool].columns[(normpricesdf.iloc[-1][targetpool] < normpricesdf.iloc[-1][benchticker])].tolist()
        if key == 'min_gain':
            targetpool = normpricesdf[targetpool].columns[(normpricesdf.iloc[-1][targetpool] >= val)].tolist()
        if key == 'max_gain':
            targetpool = normpricesdf[targetpool].columns[(normpricesdf.iloc[-1][targetpool] <= val)].tolist()
        if key.endswith('unifatscore') or key.endswith('dropscore'):
            # get bencherr
            bencherr = groupdefinition[f'{key}_bench_err']
            targetpool = getgroupbyvolmetricfunc(targetpool, key, val, benchticker, bencherr, test_beg, test_end)
    return targetpool


# single trial normpricedf download
def normpricedf_singletrial(npdfs, pricematrixdf, benchpricematrixdf, benchticker, testlen, winnerdefined, loserdefined, trial):
    trialno = trial[0]
    exist_date = trial[1]
    # get testperiod
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    # get existing stocks
    startpool = tickerportal2(exist_date, 'common')
    # get df of normalized bench and pool prices
    normpricesdf = getnormprices(pricematrixdf, benchpricematrixdf, startpool, benchticker, test_beg, test_end)
    # define winners
    winnerpool = winnerloserdefiner(startpool, winnerdefined, normpricesdf, benchticker, test_beg, test_end)
    # define losers
    loserstartpool = [item for item in startpool if item not in winnerpool]
    loserpool = winnerloserdefiner(loserstartpool, loserdefined, normpricesdf, benchticker, test_beg, test_end)
    # get dpcpricedf
    dpcpricedf = getdpcprices(pricematrixdf, benchpricematrixdf, startpool, benchticker, test_beg, test_end)
    trialdata = {
        'normpricesdf': normpricesdf,
        'dpcpricedf': dpcpricedf,
        'startpool': startpool,
        'winnerpool': winnerpool,
        'loserpool': loserpool,
        'test_beg': test_beg,
        'test_end': test_end
    }
    # save to file
    savetopkl(f'npdfdatadict_trial{trialno}', npdfs, trialdata)
