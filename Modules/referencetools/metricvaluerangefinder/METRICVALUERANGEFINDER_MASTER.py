"""
Title: METRIC VALUE RANGE FINDER Masterscript
Date Started: Nov 29, 2021
Version: 1.0
Version Start Date: Nov 29, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Returns the range of values a given set of stocks occupy with respect to a given metric.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from functools import partial
import multiprocessing as mp
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from BESTPERFORMERS_BASE import bestperformer_cruncher
from STRATTEST_FUNCBASE_RAW import atltoipo_single
from pricehistorybot import add_calibratedprices
from price_history_slicing import pricedf_daterange
from STRATTEST_FUNCBASE_MMBM import allpctdrops_single


# get maxdd
def getmaxdd_single(beg_date, end_date, metricname, stock):
    # get stock prices
    prices = pricedf_daterange(stock, beg_date, end_date)
    # get calibrated prices
    prices = add_calibratedprices(prices, ['baremaxraw'], stock)
    # calculate metricval
    maxdd = allpctdrops_single(prices, 'baremaxraw', stock, 'min')
    return {
        'stock': stock,
        metricname: maxdd
    }


# get metricval
def getstockmetvalrow(beg_date, end_date, metricname, stock):
    # get stock prices
    prices = pricedf_daterange(stock, beg_date, end_date)
    # run metric function on stock prices
    metricval = atltoipo_single(prices, stock)
    return {
        'stock': stock,
        metricname: metricval
    }


# mapasync method
def getallmetricvals_mapasync(beg_date, end_date, stockpool, metricparam):
    # FOR EACH STOCK IN POOL, GET METRIC VALUE
    pool = mp.Pool(mp.cpu_count())
    fn = partial(metricparam["metricfunc"], beg_date, end_date, metricparam["metricname"])
    resultlist = pool.map_async(fn, stockpool).get()
    pool.close()
    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=metricparam["ascending"], by=[metricparam["metricname"]], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


if __name__ == '__main__':
    # TIME PERIOD
    beg_date = ''
    end_date = '2016-10-29'

    # SET OF STOCKS TO EXAMINE
    stockpool = bestperformer_cruncher(
        {
            'beg_date': end_date,
            'end_date': '2021-10-29',
            'benchmarks': 'yes',
            'saveresults': 'no',
            'annualized': 'yes',
            'marketbeatersonly': 'yes',
            'marginrate': 0.20,
            'fatscorecap_hip': 0.16,
            'maxddcap_hip': -.63,
            'fatscorecap_life': 0.18,
            'maxddcap_life': -.63,
            'hipgrolifefatcap': 100
            }
            )

    # SET METRIC YOU WANT THE RANGE FOR
    metricparam = {
        'metricname': 'maxdd',
        'metricfunc': getmaxdd_single,
        'ascending': False}
    '''
    {
        'metricname': 'atltoipo',
        'metricfunc': getstockmetvalrow}
    '''
    # GET DF OF METRIC VALS
    mapasyncmethdf = getallmetricvals_mapasync(beg_date, end_date, stockpool, metricparam)
    # RETURN RANGE OF VALUES
    print(mapasyncmethdf)
    print(f'High value: {mapasyncmethdf[metricparam["metricname"]].max()}')
    print(f'Low value: {mapasyncmethdf[metricparam["metricname"]].min()}')
