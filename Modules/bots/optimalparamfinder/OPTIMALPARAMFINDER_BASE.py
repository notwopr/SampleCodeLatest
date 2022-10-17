"""
Title: OPTIMAL PARAM FINDER MASTER.
Date Started: July 9, 2020
Version: 1.00
Version Start: July 9, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given a date, testlen, return stats of the metric profile for the pool of stocks that beat the market for that period.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import copy
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import savetopkl, buildfolders_parent_cresult_cdump
from BACKTEST_GATHERMETHOD_FILTERANDLAYER_LAYER import layercake_all
from BACKTEST_GATHERMETHOD_FILTERANDLAYER_FUNCBASE import getmetcolname
from statresearchbot import stat_profiler
from ONETIME_GETSINGLEPASSPOOL import getsinglepasspool
from TESTPERIOD_PERFORMANCE_FUNCBASE import mktbeatpool_list, growthandmarginrate
from tickerportalbot import tickerportal2
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source
from ONETIME_MKTBEATPOOL_MASTERfunc import getmktbeatpoolpct
from OPTIMALPARAMFINDER_BASE_METPANELACCURACY import getfiltermetricparams


def getidealportfolio(verbose, testrunparent, exist_date, testlen, benchticker, firstpass_params, secondpass_params):
    # BUILD FIRSTPASS DUMP FOLDERS
    firstpassparent, firstpassresults, firstpassdump = buildfolders_parent_cresult_cdump(testrunparent, 'firstpassdump')
    # GET FULL EXTANT POOL
    fullpool = tickerportal2(exist_date, 'common')
    # GET FIRST PASS POOL
    firstpool = getsinglepasspool(firstpass_params, firstpassresults, firstpassdump, '', exist_date, fullpool)
    # GET MARKETBEATER POOL
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    mktbeaterpool = mktbeatpool_list(firstpool, benchticker, test_beg, test_end)
    # BUILD SECONDPASS DUMP FOLDERS
    secondpassparent, secondpassresults, secondpassdump = buildfolders_parent_cresult_cdump(testrunparent, 'secondpassdump')
    # GET SECOND PASS POOL
    mktbeaterpool = getsinglepasspool(secondpass_params, secondpassresults, secondpassdump, test_beg, test_end, mktbeaterpool)
    if verbose == 'verbose':
        print(f'The ideal portfolio for the {testlen}-day test period of {test_beg} to {test_end} is as follows:\n{mktbeaterpool}')
        getmktbeatpoolpct(exist_date, testlen, mktbeaterpool, benchticker)
        portfoliogrowth, benchperf, marginrate = growthandmarginrate(mktbeaterpool, benchticker, test_beg, test_end)
        print(f'Over the course of the {testlen}-day test period of {test_beg} to {test_end}, the benchmark {benchticker} gained/lost {benchperf*100} %, while the ideal portfolio gained/lost {portfoliogrowth*100} %, a difference of {marginrate*100} %.')
    return mktbeaterpool


# RETURN METRIC PANEL RANGES OF GIVEN POOL AND EXISTENCE DATE
def getmetricpanel(metricpanelresults, metricpaneldump, exist_date, test_beg, test_end, metricpanel_params, fullpool, mktbeaterpool):

    # GET METRICPANELDF OF FULL EXTANT POOL
    # collect metrics to run
    metrics_to_run = metricpanel_params[0]['method_specific_params']['fnlbatches'][0]['batch']
    layercakemetrics = [item for item in metrics_to_run if item['metricname'] != 'age']
    # create dump folders
    batchname = 'metricpaneldata'
    allmetricdataparent, allmetricdataresults, allmetricdatadump = buildfolders_parent_cresult_cdump(metricpaneldump, batchname)
    # get metricdata
    allmetricsdf = layercake_all(allmetricdataparent, allmetricdataresults, allmetricdatadump, layercakemetrics, batchname, '', exist_date, fullpool)

    # REMOVE RANKCOLS
    allmetcolnames = [getmetcolname(metricitem) for metricitem in metrics_to_run]
    keepcols = ['stock', 'age'] + allmetcolnames
    allmetricsdf = allmetricsdf[keepcols]

    # REPLACE METRIC COL WITH PCTRANK COL
    pctrankmetricnames = ['marketbeater', 'winrateranker_mean', 'winrateranker_median', 'winvolranker_std', 'winvolranker_mad']
    pctrankmetricitems = [metricitem for metricitem in metrics_to_run if metricitem['metricname'] in pctrankmetricnames]
    for metricitem in pctrankmetricitems:
        rankdirection = metricitem['rankascending']
        metcolname = getmetcolname(metricitem)
        allmetricsdf[metcolname] = allmetricsdf[metcolname].rank(ascending=rankdirection, pct=True)

    # SAVE NONFILTERED METRICDF TO FILE
    formatallmetfn = f'formattedallmetricsdf_testperiod{test_beg}_{test_end}'
    savetopkl(formatallmetfn, metricpanelresults, allmetricsdf)
    allmetricsdf.to_csv(index=False, path_or_buf=metricpanelresults / f"{formatallmetfn}.csv")

    # FILTER OUT NONMKTBEATER STOCKS
    allmetricsdf = allmetricsdf[allmetricsdf['stock'].isin(mktbeaterpool)]

    # SAVE MKTBEATERPOOL VERSION OF METRICDF TO FILE
    mktbeatfn = f'mktbeatermetricsdf_testperiod{test_beg}_{test_end}'
    savetopkl(mktbeatfn, metricpanelresults, allmetricsdf)
    allmetricsdf.to_csv(index=False, path_or_buf=metricpanelresults / f"{mktbeatfn}.csv")

    # GET RANGES FOR EACH METRIC COLUMN
    rangesummdata = []
    for metricitem in metrics_to_run:
        metricname = metricitem['metricname']
        metcolname = getmetcolname(metricitem)
        metcolseries = allmetricsdf[metcolname].to_numpy()
        statsumm = stat_profiler(metcolseries)
        summdict = {'metricname': metricname}
        summdict.update(statsumm)
        rangesummdata.append(summdict)

    # CREATE DF OF SUMMARY
    mktbeatstatsummdf = pd.DataFrame(data=rangesummdata)

    # SAVE DF TO FILE
    mktbeatsummfn = f'mktbeatstatsummdf_testperiod{test_beg}_{test_end}'
    savetopkl(mktbeatsummfn, metricpanelresults, mktbeatstatsummdf)
    mktbeatstatsummdf.to_csv(index=False, path_or_buf=metricpanelresults / f"{mktbeatsummfn}.csv")
    return mktbeatstatsummdf


def getmetricrangesandaccuracy(testrunparent, metricpanel_params_temp, exist_date, testlen, firstpass_params, mktbeaterpool, todaysdate):
    # BUILD METRICPANEL DUMP FOLDERS
    metricpanelparent, metricpanelresults, metricpaneldump = buildfolders_parent_cresult_cdump(testrunparent, 'metricpaneldump')
    # CREATE NO FILTER VERSION OF METRICPARAM TEMPLATE
    metricpanel_nofilterparams = copy.deepcopy(metricpanel_params_temp)
    metrics_to_run_temp = metricpanel_nofilterparams[0]['method_specific_params']['fnlbatches'][0]['batch']
    for metricitem in metrics_to_run_temp:
        metricitem.update({'filterdirection': 'no'})
    metricpanel_nofilterparams[0]['method_specific_params']['fnlbatches'][0]['batch'] = metrics_to_run_temp
    # RETURN METRIC PANEL RANGES OF GIVEN POOL AND EXISTENCE DATE
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    fullpool = tickerportal2(exist_date, 'common')
    firstpassparent, firstpassresults, firstpassdump = buildfolders_parent_cresult_cdump(testrunparent, 'firstpassdump')
    firstpool = getsinglepasspool(firstpass_params, firstpassresults, firstpassdump, '', exist_date, fullpool)
    mktbeatstatsummdf = getmetricpanel(metricpanelresults, metricpaneldump, exist_date, test_beg, test_end, metricpanel_nofilterparams, firstpool, mktbeaterpool)
    # GET FILTER VERSION OF METRICPANEL
    metrics_to_run = metricpanel_params_temp[0]['method_specific_params']['fnlbatches'][0]['batch']
    newmetrics_to_run = getfiltermetricparams(mktbeatstatsummdf, metrics_to_run)
    # SAVE FILTER VERSION TO FILE
    newmetricpanel_params = copy.deepcopy(metricpanel_params_temp)
    newmetricpanel_params[0]['method_specific_params']['fnlbatches'][0]['batch'] = newmetrics_to_run
    savetopkl(f'newmetricstorun_exist{exist_date}_today{todaysdate}', testrunparent, newmetricpanel_params)
    return newmetricpanel_params
