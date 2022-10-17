"""
Title: DROP STOCK BOT BASE
Date Started: Dec 8, 2020
Version: 1.00
Version Start: Dec 8, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Tells you whether to drop a stock based on the current day of the investing period you are in. Uses findings from pulloutbot data.
What I want to answer:
Given
(1) a stock
(2) how long its been held for
(3) length of investment period
(4) current cumulative growth so far,
what is the likelihood that the stock will, by the end of the investment period:
(1) be a marketbeater and
    for each trial: get proportion of stocks with the same cumulative growth that are marketbeaters.
        (a) get all stocks with same cumulative growth
        (b) get list of those stocks that are mktbeaters (intersect list (a) with list of all mktbeaters for the trial)
        (c) proportion = list(b) / list(a)
(2) have a margin over marketbeater of >=X
(3) have gain of >=Y

Alternatively
probability that stock with same cumulative margin over bench on day X will be a marketbeater by day 365
    same as before except get all stocks with same cumulative margin over bench
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from filelocations import buildfolders_singlechild, buildfolders_regime_testrun, savetopkl
from tickerportalbot import tickerportal3
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, tickerlistcommon_source
from timeperiodbot import getrandomexistdate_multiple, alldatewithtestlen
from statresearchbot import stat_profiler
from genericfunctionbot import multiprocessorshell
from DROPSTOCKBOT_BASE_HITPCT import gethitpct_all


# get list of qualifiers
def getedatepool_single(destfolder, trial):
    trialno = trial[0]
    existdate = trial[1]
    # get existpool
    existpool = tickerportal3(existdate, 'common', 2)
    trialdata = {
        'trialno': trialno,
        'existdate': existdate,
        'pool': existpool
    }
    # save to file
    savetopkl(f'edatepool_trial{trialno}', destfolder, trialdata)


# save and return set of dates and pools to be run for this test run
def getedatepool_all(savedir, dumpfolder, dates, testrundate, testnumber, chunksize):
    # run multiprocessor
    targetvars = (dumpfolder,)
    multiprocessorshell(dumpfolder, getedatepool_single, dates, 'yes', targetvars, chunksize)
    # assemble results
    trialrunset = []
    for child in dumpfolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        trialrunset.append(unpickled_raw)
    # save
    mod_date = testrundate.replace("-", "")
    testcode = 'D' + mod_date + 'T' + str(testnumber)
    savetopkl(f'{testcode}_trialrunset', savedir, trialrunset)
    return trialrunset


# add benchgain and end date data to each trial run iterable
def addtoiterable_single(destfolder, investperiod, benchticker, daysinvested, trialiter):
    existdate = trialiter['existdate']
    trialno = trialiter['trialno']
    # get date range
    end_date = str(dt.date.fromisoformat(existdate) + dt.timedelta(days=investperiod))
    # get benchmark prices
    prices = grabsinglehistory(benchticker)
    prices = fill_gaps2(prices, existdate, end_date)
    prices.reset_index(drop=True, inplace=True)
    # calculate gain
    endprice = prices.iat[-1, 1]
    begprice = prices.iat[0, 1]
    benchgain = (endprice - begprice) / begprice
    # get current benchgain
    interim_date = str(dt.date.fromisoformat(existdate) + dt.timedelta(days=daysinvested))
    interimprice = prices.iat[daysinvested, 1]
    benchgain_curr = (interimprice - begprice) / begprice
    # add gain to iter
    trialiter.update({
        'end_date': end_date,
        'interim_date': interim_date,
        'daysinvested': daysinvested,
        'benchticker': benchticker,
        'benchgain': benchgain,
        'benchgain_curr': benchgain_curr,
        'benchprice_enddate': endprice
        })
    # save to file
    savetopkl(f'iterable_trial{trialno}', destfolder, trialiter)


# add benchgain and end_dates to trialrunset
def addtoiterable_all(dumpfolder, investperiod, benchticker, daysinvested, trialrunset, chunksize):
    # run multiprocessor
    targetvars = (dumpfolder, investperiod, benchticker, daysinvested)
    multiprocessorshell(dumpfolder, addtoiterable_single, trialrunset, 'no', targetvars, chunksize)
    # assemble results
    trialrunset = []
    for child in dumpfolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        trialrunset.append(unpickled_raw)
    return trialrunset


# get date-pool-benchgain iterables
def gettrialiterables(savedir, global_params):
    # get trialexistdates
    if len(global_params['existingset']) != 0:
        trialrunset = global_params['existingset']
    else:
        if global_params['trialtype'] == 'random':
            # get trialexistdates
            alltrialexistdates = getrandomexistdate_multiple(global_params['num_trials'], global_params['firstdate'], global_params['latestdate'], global_params['investperiod'], daterangedb_source)
        elif global_params['trialtype'] == 'full':
            alltrialexistdates = alldatewithtestlen(global_params['investperiod'], global_params['firstdate'], global_params['latestdate'], daterangedb_source, 'ascending')
        # save trialrunset
        datepooldump = buildfolders_singlechild(savedir, 'datepooldump')
        trialrunset = getedatepool_all(savedir, datepooldump, alltrialexistdates, global_params['todaysdate'], global_params['testnumber'], global_params['chunksize'])
    # build benchgain folder
    benchgaindump = buildfolders_singlechild(savedir, 'benchgaindump')
    # add benchgain and benchgain_curr to trialrunset
    trialrunset = addtoiterable_all(benchgaindump, global_params['investperiod'], global_params['benchticker'], global_params['daysinvested'], trialrunset, global_params['chunksize'])
    # filter out iterables that do not match the current benchgain
    if global_params['benchgain_currfilter'] == 'yes':
        newtrialrunset = []
        for item in trialrunset:
            if global_params['benchgain_curr'] + global_params['benchgain_err'] > item['benchgain_curr'] and item['benchgain_curr'] > global_params['benchgain_curr'] - global_params['benchgain_err']:
                newtrialrunset.append(item)
        trialrunset = newtrialrunset
    return trialrunset


# get trialsummaries and stats
def getsummariesandstats(parentfolder, trialrunset, global_params):
    # build trial dump folder
    trialdumpparent = buildfolders_singlechild(parentfolder, 'trialdumpparent')
    # get all trial results df
    alltrialsummdf = gethitpct_all(parentfolder, trialdumpparent, global_params['ideal_profile'], global_params['candidate_profile'], trialrunset, global_params['chunksize'])
    # calculate probability that candidate stocks will meet requirements
    statdict = stat_profiler(alltrialsummdf['hitpct'].dropna())
    mktbeatstatdf = pd.DataFrame(data=[statdict])
    mktbeatstatdf.to_csv(index=False, path_or_buf=parentfolder / "hitpctpctstats.csv")
    return statdict


# main consistency function
def dropbot_multitrialcruncher(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # get date-pool-benchgain iterables
    trialrunset = gettrialiterables(testrunparent, global_params)
    # get trialsummaries and stats
    statdict = getsummariesandstats(testrunparent, trialrunset, global_params)
    return statdict
