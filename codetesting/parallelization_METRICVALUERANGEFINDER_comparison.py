"""
These were the results of running various parallelization methods for the Metricvaluerangefinder script.  Serial method was best when the number of stocks to analyze was 400 or less.  But for running on all available stocks for an existing date, the following results show that map_async was the best:
serial method
elapsed: 42.132761001586914 secs
Map method
elapsed: 5.632718086242676 secs
Map_async method
elapsed: 5.4999260902404785 secs
starmap_async method
elapsed: 5.524461269378662 secs
starmap async matrix method
elapsed: 7.384683132171631 secs
map async matrix method
elapsed: 6.623548269271851 secs
map async pathos matrix method
elapsed: 7.6267781257629395 secs
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import time
from functools import partial
import multiprocessing as mp
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
from pathos.multiprocessing import ProcessingPool as pathosp
#   LOCAL APPLICATION IMPORTS
from BESTPERFORMERS_BASE import bestperformer_cruncher
from STRATTEST_FUNCBASE_RAW import atltoipo_single
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from UPDATEPRICEDATA_FILELOCATIONS import PRICES, tickerlistcommon_source, daterangedb_source
from filelocations import readpkl
from genericfunctionbot import trimdfbydate
from tickerportalbot import tickerportal2


# get metricval
def getstockmetvalrow(beg_date, end_date, metricvalcolname, stock):
    # get stock prices
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(drop=True, inplace=True)
    # run metric function on stock prices
    metricval = atltoipo_single(prices, stock)
    return {
        'stock': stock,
        metricvalcolname: metricval
    }


# serial method
def getallmetricvals_serial(beg_date, end_date, stockpool, metricfunc, metricname, ascending):
    # SET METRIC VAL COL NAME
    metricvalcolname = f'{metricname}_value'
    # FOR EACH STOCK IN POOL, GET METRIC VALUE

    resultlist = []
    for stock in stockpool:
        resultlist.append(getstockmetvalrow(beg_date, end_date, metricvalcolname, stock))

    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=ascending, by=[metricvalcolname], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


# map method
def getallmetricvals_map(beg_date, end_date, stockpool, metricfunc, metricname, ascending):
    # SET METRIC VAL COL NAME
    metricvalcolname = f'{metricname}_value'
    # FOR EACH STOCK IN POOL, GET METRIC VALUE
    pool = mp.Pool(mp.cpu_count())
    fn = partial(getstockmetvalrow, beg_date, end_date, metricvalcolname)
    resultlist = pool.map(fn, stockpool)
    pool.close()

    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=ascending, by=[metricvalcolname], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


# mapasync method
def getallmetricvals_mapasync(beg_date, end_date, stockpool, metricfunc, metricname, ascending):
    # SET METRIC VAL COL NAME
    metricvalcolname = f'{metricname}_value'
    # FOR EACH STOCK IN POOL, GET METRIC VALUE
    pool = mp.Pool(mp.cpu_count())
    fn = partial(getstockmetvalrow, beg_date, end_date, metricvalcolname)
    resultlist = pool.map_async(fn, stockpool).get()
    pool.close()
    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=ascending, by=[metricvalcolname], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


# starmapasync method
def getallmetricvals_starmapasync(beg_date, end_date, stockpool, metricfunc, metricname, ascending):
    # SET METRIC VAL COL NAME
    metricvalcolname = f'{metricname}_value'
    # FOR EACH STOCK IN POOL, GET METRIC VALUE
    pool = mp.Pool(mp.cpu_count())
    resultlist = pool.starmap_async(getstockmetvalrow, [(beg_date, end_date, metricvalcolname, stock) for stock in stockpool]).get()
    pool.close()
    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=ascending, by=[metricvalcolname], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


# get metricval - matrix version
def getstockmetvalrow_matrixversion(metricvalcolname, stockcolname, stockcolseries):
    # ignore nans
    prices = stockcolseries.dropna()
    return {
        'stock': stockcolname,
        metricvalcolname: prices.min()/prices.iat[0]
    }


# get metricval - matrix version
def getstockmetvalrow_matrixversion_map(metricvalcolname, stockcol):
    # ignore nans
    prices = stockcol[1].dropna()
    return {
        'stock': stockcol[0],
        metricvalcolname: prices.min()/prices.iat[0]
    }


# starmap async matrix version method
def getallmetricvals_matrix(beg_date, end_date, stockpool, metricfunc, metricname, ascending):
    # GET PRICEMATRIX
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    # SLICE OUT STOCKS AND DATES
    all_cols = ['date'] + stockpool
    pricematrixdf = pricematrixdf[all_cols]
    pricematrixdf = trimdfbydate(pricematrixdf, 'date', beg_date, end_date)
    pricematrixdf = pricematrixdf[stockpool]
    # SET METRIC VAL COL NAME
    metricvalcolname = f'{metricname}_value'
    # FOR EACH STOCK IN POOL, GET METRIC VALUE
    # Column wise Operation
    #with mp.Pool(mp.cpu_count()) as pool:
    #fn = partial(getstockmetvalrow_matrixversion, metricvalcolname)
    #result = pool.imap(fn, pricematrixdf.iteritems(), chunksize=10)
    #resultlist = [x for x in result]
    pool = mp.Pool(mp.cpu_count())
    fn = partial(getstockmetvalrow_matrixversion, metricvalcolname)
    resultlist = pool.starmap_async(fn, pricematrixdf.iteritems()).get()
    pool.close()
    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=ascending, by=[metricvalcolname], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


# map async matrix version method
def getallmetricvals_matrix_mapasync(beg_date, end_date, stockpool, metricfunc, metricname, ascending):
    # GET PRICEMATRIX
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    # SLICE OUT STOCKS AND DATES
    all_cols = ['date'] + stockpool
    pricematrixdf = pricematrixdf[all_cols]
    pricematrixdf = trimdfbydate(pricematrixdf, 'date', beg_date, end_date)
    pricematrixdf = pricematrixdf[stockpool]
    # SET METRIC VAL COL NAME
    metricvalcolname = f'{metricname}_value'
    # FOR EACH STOCK IN POOL, GET METRIC VALUE
    pool = mp.Pool(mp.cpu_count())
    fn = partial(getstockmetvalrow_matrixversion_map, metricvalcolname)
    resultlist = pool.map_async(fn, pricematrixdf.iteritems()).get()
    pool.close()
    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=ascending, by=[metricvalcolname], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


# matrix map async pathos version method
def getallmetricvals_matrix_pathos(beg_date, end_date, stockpool, metricfunc, metricname, ascending):
    # GET PRICEMATRIX
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    # SLICE OUT STOCKS AND DATES
    all_cols = ['date'] + stockpool
    pricematrixdf = pricematrixdf[all_cols]
    pricematrixdf = trimdfbydate(pricematrixdf, 'date', beg_date, end_date)
    pricematrixdf = pricematrixdf[stockpool]
    # set date col as index
    # SET METRIC VAL COL NAME
    metricvalcolname = f'{metricname}_value'
    pool = pathosp(mp.cpu_count())
    fn = partial(getstockmetvalrow_matrixversion_map, metricvalcolname)
    resultlist = pool.amap(fn, pricematrixdf.iteritems()).get()
    pool.close()
    pool.join()
    pool.clear()
    # assemble dataframe of results
    resultdf = pd.DataFrame(data=resultlist)
    # sort dataframe by metricval
    resultdf.sort_values(ascending=ascending, by=[metricvalcolname], inplace=True)
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf


if __name__ == '__main__':
    # TIME PERIOD
    beg_date = ''
    end_date = '2016-10-29'

    # SET OF STOCKS TO EXAMINE
    '''
    stockpool = bestperformer_cruncher(
        {
            'beg_date': end_date,
            'end_date': '2021-10-29',
            'benchmarks': 'yes',
            'saveresults': 'no',
            'annualized': 'yes',
            'marketbeatersonly': 'yes',
            'marginrate': 0.10
        }
    )
    '''
    stockpool = tickerportal2(daterangedb_source, tickerlistcommon_source, end_date, 'common')

    # SET METRIC YOU WANT THE RANGE FOR
    metricfunc = atltoipo_single
    metricname = 'atltoipo'
    # FINAL DATAFRAME SORT DIRECTION
    ascending = False

    # serial method
    start = time.time()
    serialmethdf = getallmetricvals_serial(beg_date, end_date, stockpool, metricfunc, metricname, ascending)
    end = time.time()
    print('serial method')
    print(f'elapsed: {end-start} secs')
    #print(serialmethdf)

    # Map method
    start = time.time()
    mapmethdf = getallmetricvals_map(beg_date, end_date, stockpool, metricfunc, metricname, ascending)
    end = time.time()
    print('Map method')
    print(f'elapsed: {end-start} secs')
    #print(mapmethdf)

    # check if alternate method produced identical results
    if serialmethdf.equals(mapmethdf) is False:
        print('WARNING: RESULTING DFs did not match!!')

    # Map_async
    start = time.time()
    mapasyncmethdf = getallmetricvals_mapasync(beg_date, end_date, stockpool, metricfunc, metricname, ascending)
    end = time.time()
    print('Map_async method')
    print(f'elapsed: {end-start} secs')
    #print(mapasyncmethdf)

    # check if alternate method produced identical results
    if serialmethdf.equals(mapasyncmethdf) is False:
        print('WARNING: RESULTING DFs did not match!!')

    # starmap async
    start = time.time()
    starmapasyncmethdf = getallmetricvals_starmapasync(beg_date, end_date, stockpool, metricfunc, metricname, ascending)
    end = time.time()
    print('starmap_async method')
    print(f'elapsed: {end-start} secs')
    #print(starmapasyncmethdf)

    # check if alternate method produced identical results
    if serialmethdf.equals(starmapasyncmethdf) is False:
        print('WARNING: RESULTING DFs did not match!!')

    # starmap async matrix
    start = time.time()
    matrixmethdf = getallmetricvals_matrix(beg_date, end_date, stockpool, metricfunc, metricname, ascending)
    end = time.time()
    print('starmap async matrix method')
    print(f'elapsed: {end-start} secs')
    #print(matrixmethdf)

    # check if alternate method produced identical results
    if serialmethdf.equals(matrixmethdf) is False:
        print('WARNING: RESULTING DFs did not match!!')

    # map async matrix
    start = time.time()
    matrixmethdf = getallmetricvals_matrix_mapasync(beg_date, end_date, stockpool, metricfunc, metricname, ascending)
    end = time.time()
    print('map async matrix method')
    print(f'elapsed: {end-start} secs')
    #print(matrixmethdf)

    # check if alternate method produced identical results
    if serialmethdf.equals(matrixmethdf) is False:
        print('WARNING: RESULTING DFs did not match!!')

    # map async matrix pathos
    start = time.time()
    matrixmethdf = getallmetricvals_matrix_pathos(beg_date, end_date, stockpool, metricfunc, metricname, ascending)
    end = time.time()
    print('map async pathos matrix method')
    print(f'elapsed: {end-start} secs')
    #print(matrixmethdf)

    # check if alternate method produced identical results
    if serialmethdf.equals(matrixmethdf) is False:
        print('WARNING: RESULTING DFs did not match!!')
