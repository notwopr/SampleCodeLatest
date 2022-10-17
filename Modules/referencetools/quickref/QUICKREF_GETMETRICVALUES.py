from Modules.price_history import grabsinglehistory, add_calibratedprices, tradedateonlypricedf, add_calibratedprices_universal, grabsinglehistory_fundies
from fillgapbot import fill_gaps2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path
import seaborn as sns
import datetime as dt
from STRATTEST_FUNCBASE_RAW import dpc_cruncher_single, flatline_single, segliferatio_single, age_single, slopescorefocus_single, segbackslopescore_single, getpctchange_single, psegnegsegratio_single, statseglen_single, posnegmag_single, posnegprevalence_single, rollingslopescore_single, dpc_cruncher_posneg_single
from STRATTEST_FUNCBASE_MMBM import smoothsqueezeshell, unifatshell_single, fatarea_single, dropscoreratio_single, dropscore_single, rollgrowthtoloss_single, allpctdrops_single, growthtoloss_single
from STRATTEST_FUNCBASE import allpctchanges
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher
from SCRATCHPAPER_GRAPHING import graphtopbottom, graphtopbottombenchcompare
from filelocations import readcsv
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, tickerlistcommon_source
from tickerportalbot import tickerportal3


#resultfileloc = Path(r'C:\Users\david\Documents\PROJECTBELUGA\BOT_DUMP\strattest_singles')
#resultfilename = 'Stage 3_recoverybotv9_finalists_as_of_2021-10-29'
#resultdf = readcsv(resultfilename, resultfileloc)
#resultdf = resultdf.query('0.0009 <= slopescore_LB1095 <= 0.0012')
#resultdf.sort_values(ascending=False, by=['bigjumpscore_oldbareminraw'], inplace=True)
#fullstocklist = resultdf['stock'].tolist()
#fullstocklist = tickerportal3('2020-01-26', 'common', 180)
fullstocklist = ['AXSM']
beg_date = '2016-10-29'
end_date = '2021-10-29'
metrifunc = unifatshell_single
win_len = 30
fundytype = 'fundies'
datasourcetype = 'revenue'
# ADD BENCH TO COMPARE
benchticker = '^IXIC'
groparams = {
    'gmeth': 'slopescore',
    'focuscol': 'rawprice'}
lossparams = {
    'lmeth': 'allpctdrop',
    'uppercol': 'baremaxraw',
    'lowercol': 'rawprice',
    'allcalibrations': ['baremaxraw'],
    'stat_type': 'min'}
combtype = 'ratio'
for stock in fullstocklist:
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(drop=True, inplace=True)
    #prices = tradedateonlypricedf(prices)
    #prices = priceslicer(prices, 360)
    prices = add_calibratedprices_universal(prices, ['baremaxraw'], stock)
    #fundydf = grabsinglehistory_fundies(stock, fundytype)
    #fundydf = fill_gaps2(fundydf, beg_date, end_date)
    #fundydf.reset_index(drop=True, inplace=True)
    #fundydf = fundydf[["date", f'{datasourcetype}_{stock}']].copy()
    #fundydf.rename(columns={f'{datasourcetype}_{stock}': stock}, inplace=True)
    #fundydf = add_calibratedprices_universal(fundydf, ['baremaxraw'], stock)
    #prices = fundydf
    #prices = prices.join(fundydf.set_index('date'), how="left", on="date")
    # get bench dropscore for same date range
    benchprices = grabsinglehistory(benchticker)
    benchprices = fill_gaps2(benchprices, '', '')
    prices = prices.join(benchprices.set_index('date'), how="left", on="date")
    prices = add_calibratedprices_universal(prices, ['baremaxraw'], benchticker)
    #dpc = allpctchanges(prices, 'oldbareminraw', 1)
    metricfuncinputs = (prices, stock, f'{stock}_baremaxraw', 'avg')
    metval = metrifunc(*metricfuncinputs)
    metricfuncinputs2 = (prices, benchticker, f'{benchticker}_baremaxraw', 'avg')
    benchval = metrifunc(*metricfuncinputs2)
    print(stock, metval, benchval)
    #print(metval)
    # graph
    #prices['dpc'] = prices[stock].pct_change(periods=1, fill_method='ffill')
    prices[f'{stock}_diff'] = (prices[stock] - prices[f'{stock}_baremaxraw']) / prices[f'{stock}_baremaxraw']
    #prices[f'{benchticker}_diff'] = (prices[benchticker] - prices[f'{benchticker}_baremaxraw']) / prices[f'{benchticker}_baremaxraw']
    #print(prices[stock].rolling(360))
    #age = len(prices) - 1
    #if age <= win_len:
        #prices['rolling'] = growthtoloss_single(prices, stock, groparams, lossparams, combtype)
    #else:
        #prices['rolling'] = prices.index.map(lambda x: growthtoloss_single(prices.iloc[x:x+win_len, :].copy(), stock, groparams, lossparams, combtype) if x < len(prices)-(win_len-1) else None)
    graphtopbottom(prices, prices, 'date', 'date', [stock, f'{stock}_baremaxraw'], [f'{stock}_diff'], [2, 1], 'True', 'True')
    #graphtopbottombenchcompare(prices, prices, 'date', 'date', [stock, f'{stock}_baremaxraw'], [benchticker, f'{benchticker}_baremaxraw'], [f'{stock}_diff', f'{benchticker}_diff'], [2, 1], 'True', 'True')
    #sns.lineplot(data=fundydf)
    #sns.lineplot(data=prices[[stock]])
    #ax2 = plt.twinx()
    #sns.lineplot(data=prices[[f'revenue_{stock}', f'freecashflow_{stock}']], ax=ax2)
    #plt.show()
