"""
Title: MKTBEATERFINDER MASTER
Date Started: Nov 18, 2020
Version: 1.00
Version Start: Nov 18, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Finds a list of stocks that might be marketbeaters given a current date, a testperiod start and end date and a benchmark.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from tickerportalbot import tickerportal3
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source
from PULLOUT_BASE import getnormprices
from genericfunctionbot import intersectlists
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES
from filelocations import readpkl


# single pulloutbot trial
def getoverallpulloutpct(trialresultparent, normpricesdf, startpool, benchticker):
    # convert normprices to boolean whether it beat or did not beat market
    normpricesdf[startpool] = normpricesdf[startpool].apply(lambda x: x > normpricesdf[benchticker])
    # clean df
    # remove first row, remove benchmark and date cols
    normpricesdf = normpricesdf.iloc[1:][startpool]
    # add day column
    normpricesdf['testday'] = normpricesdf.index
    # reorder columns
    normpricesdf = normpricesdf[['testday']+startpool]
    # reset index
    normpricesdf.reset_index(inplace=True, drop=True)
    # save boolean version
    normpricesdf.to_csv(index=False, path_or_buf=trialresultparent / "fullnormpricedf_boolean.csv")
    # get perstock stats
    overallpulloutpctdata = normpricesdf[startpool].mean(axis=0)
    overallpulloutdf = pd.DataFrame(data=overallpulloutpctdata)
    # correct column headers, add index
    overallpulloutdf.reset_index(inplace=True)
    pullpctcolname = 'Overall Pullout Pct'
    overallpulloutdf.rename(columns={'index': 'STOCK', 0: pullpctcolname}, inplace=True)
    # correct sort and reset index
    overallpulloutdf.sort_values(ascending=False, by=[pullpctcolname], inplace=True)
    overallpulloutdf.reset_index(drop=True, inplace=True)
    # save
    overallpulloutdf.to_csv(index=False, path_or_buf=trialresultparent / "overallpulloutpctdf.csv")
    return overallpulloutdf


# get masterdf of current gains, margins and pulloutpct
def getcurrpulloutstats(destfolder, startpool, global_params, pullout_beg, trialdate):
    # get df of normalized bench and pool prices
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    normpricesdf = getnormprices(pricematrixdf, benchpricematrixdf, startpool, global_params['benchticker'], pullout_beg, trialdate)
    # save fulldf
    normpricesdf.to_csv(index=False, path_or_buf=destfolder / f"fullnormpricedf_begdate{pullout_beg}_currdate{trialdate}.csv")
    # create summary list
    masterdf = pd.DataFrame(data={
        'STOCK': startpool,
        'Start Date': pullout_beg,
        'Current Date': trialdate,
        'Current Testlen (days)': global_params['testday']
        })
    # remove every row except first and last
    transposeversiondf = normpricesdf.copy()
    transposeversiondf = transposeversiondf.iloc[[-1], :]
    transposeversiondf.reset_index(drop=True, inplace=True)
    finaldf_transposed = transposeversiondf.transpose()
    finaldf_transposed.reset_index(inplace=True)
    finaldf_transposed.rename(columns={'index': 'STOCK', 0: 'Gain/Loss Rate (%)'}, inplace=True)
    finaldf_transposed = finaldf_transposed.iloc[1:]
    finaldf_transposed.reset_index(drop=True, inplace=True)
    masterdf = masterdf.join(finaldf_transposed.set_index('STOCK'), how="left", on="STOCK")
    # get difference in growth
    benchperf = normpricesdf.iloc[-1][global_params['benchticker']].item()
    masterdf['Difference (%)'] = masterdf['Gain/Loss Rate (%)'] - benchperf
    # get overallpullout pcts for each stock
    overallpulloutdf = normpricesdf.copy()
    overallpulloutdf = getoverallpulloutpct(destfolder, overallpulloutdf, startpool, global_params['benchticker'])
    # add overallpulloutpct column
    masterdf = masterdf.join(overallpulloutdf.set_index('STOCK'), how="left", on="STOCK")
    # sort reset and save
    masterdf.sort_values(ascending=False, by=['Difference (%)'], inplace=True)
    masterdf.reset_index(drop=True, inplace=True)
    masterdfname = 'currentmktbeatersummarydf'
    masterdf.to_csv(index=False, path_or_buf=destfolder / f"{masterdfname}.csv")
    return masterdf


# filter master list of existing stocks
def filtermasterdfbypullout(destfolder, masterdf, global_params, filterinstructdict):
    # get pulluplib values
    pulloutlib = pd.read_csv(global_params['polibsource'])
    # for each set of instructions
    for filterdict in filterinstructdict:
        # store threshold value
        threshval = pulloutlib[pulloutlib['testday'] == global_params['testday']][filterdict['comparecol']].item()
        # filter according to instruction
        if filterdict['filtermeth'] == 'above':
            masterdf = masterdf[masterdf[filterdict['targetcol']] > threshval].copy()
    # save filtered masterdf
    filterdfname = 'currentmktbeatersummarydf_filtered'
    masterdf.to_csv(index=False, path_or_buf=destfolder / f"{filterdfname}.csv")
    return masterdf


# main pulloutbot function
def mktbeaterfinder_master(trialfolder, global_params, custompool, trialdate):
    # get pullout_beg date
    pullout_beg = str(dt.date.fromisoformat(trialdate) - dt.timedelta(days=global_params['testday']))
    # get existing stocks
    startpool = tickerportal3(pullout_beg, 'common', 2)
    if custompool != []:
        startpool = intersectlists(custompool, startpool)
    # get masterdf of current gains, margins and pulloutpct
    masterdf = getcurrpulloutstats(trialfolder, startpool, global_params, pullout_beg, trialdate)
    # filter master according to instructions
    filterdf = filtermasterdfbypullout(trialfolder, masterdf, global_params, global_params['filterinstructdict'])
    # reset index
    filterdf.reset_index(drop=True, inplace=True)
    # rename stock col
    filterdf.rename(columns={'STOCK': 'stock'}, inplace=True)
    # randomly shuffle df
    filterdf = filterdf.sample(frac=1).reset_index(drop=True)
    return filterdf
