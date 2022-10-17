"""
Title: STRAT TEST SINGLE BASE
Date Started: July 10, 2020
Version: 2
Version Start: Oct 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given an existence date, runs pool thru first pass screening, runs again through given screening method, and returns percentage of resulting pool that beat market during the test period.
VERSIONS:
1.01: Optimize with updated functions.  Allow for more modulatory.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from Modules.metriclibrary.STRATTEST_FUNCBASE_PERFORMANCE import mktbeatpoolstats
from file_functions import buildfolders_singlechild, savetopkl
from Modules.strattester.STRATTEST_SINGLE_BASE_CRUNCHER import stagecruncher
from Modules.bots.beststreak.BESTSTREAK_BASE import beststreak_cruncher
from Modules.price_history import grabsinglehistory
from Modules.price_history_fillgaps import fill_gaps2
from Modules.timeperiodbot import dipdates
from Modules.tickerportalbot import tickerportal3
from Modules.list_functions import intersectlists


# get crash start and end dates
def getreboundcrashdates(exist_date, crashlookbacklen, crashbenchticker):
    # get crashrange beg_date
    lookbackend_date = exist_date
    lookbackbeg_date = str(dt.date.fromisoformat(exist_date) - dt.timedelta(days=crashlookbacklen))
    # pull up benchmark prices
    prices = grabsinglehistory(crashbenchticker)
    prices = fill_gaps2(prices, lookbackbeg_date, lookbackend_date)
    # find crash dates
    peakdate, valleydate = dipdates(prices, crashbenchticker)
    return peakdate, valleydate


# returns pool of stocks that existed pre-crash as well as crash dates; reassign exist date to peak date
def getfirsttimereboundinputs(exist_date, currentpool, stagescript):
    peakdate, valleydate = getreboundcrashdates(exist_date, stagescript['crashlookbacklen'], stagescript['crashbenchticker'])
    exist_date = peakdate
    # make sure the pool includes stocks that existed pre-crash
    peakexistpool = tickerportal3(exist_date, 'common', 2)
    # eliminate stocks that were filtered out by previous stages (like stage 1)
    currentpool = intersectlists(currentpool, peakexistpool)
    setreboundbotdates = 'yes'
    return setreboundbotdates, currentpool, exist_date, peakdate, valleydate


# GET STAGEDF
def getstagedf(verbose, stagescript, exist_date, stageparent, rankmeth, rankregime, currentpool, setreboundbotdates, stagenum, savemode, chunksize):
    if stagescript['scriptname'].startswith('winstreak'):
        beg_date = str(dt.date.fromisoformat(exist_date) - dt.timedelta(days=stagescript['look_back']))
        stagedf = beststreak_cruncher(verbose, beg_date, exist_date, stagescript['benchticker'], stagescript['periodlen'], stagescript['avg_type'], stagescript['avgmarginweight'], stagescript['num_mktbeatweight'], stageparent, rankmeth, rankregime, currentpool)
    else:
        # if running reboundbot
        if stagescript['scriptname'].startswith('reboundbot'):
            if setreboundbotdates == 'no':
                setreboundbotdates, currentpool, exist_date, peakdate, valleydate = getfirsttimereboundinputs(exist_date, currentpool, stagescript)
            if stagescript['scripttype'] == 'ranker':
                # get index of loss component metric item
                lossqualmetricitemlist = stagescript['lossandquality_params']['scriptparams']
                for metricitem in enumerate(lossqualmetricitemlist):
                    if metricitem[1]['metricname'] == 'crasheventloss':
                        losscompindex = metricitem[0]
                # update losscomponent item with crash dates
                stagescript['lossandquality_params']['scriptparams'][losscompindex].update({
                    'eventstart': peakdate,
                    'eventend': valleydate
                })
                # reassign stagescript variable
                stagescript = stagescript['lossandquality_params']
        stagedf = stagecruncher(stageparent, stagenum, stagescript, '', exist_date, currentpool, rankmeth, rankregime, savemode, chunksize)
    return stagedf


# RETURN WEIGHTED RANKING OF A SET OF STAGE RANKINGS
def multistageranking(savemode, savedir, setofstages, tickerlist):
    # create masterdf of all stocks
    masterdf = pd.DataFrame(data={'stock': tickerlist})
    # for each stagedf in set of stages
    sumcols = []
    weight_total = 0
    for stagedfdict in setofstages:
        stagedf = stagedfdict['stagedf']
        stagenum = stagedfdict['stagenum']
        stagename = stagedfdict['stagename']
        stageweight = stagedfdict['stageweight']
        # get stagedf version with stock and last rankcol only
        rankcolname = list(stagedf.columns)[-1]
        stagedfconcise = stagedf[['stock', rankcolname]].copy()
        # rename rankcol
        newrankcolname = f'STAGERANK_{stagenum}:{stagename}'
        stagedfconcise.rename(columns={rankcolname: newrankcolname}, inplace=True)
        # append df to masterdf
        masterdf = masterdf.join(stagedfconcise.set_index('stock'), how="left", on="stock")
        # GET EACH RANKCOLUMN'S WEIGHTED RANK VALUE
        wrankcolname = f'w_{newrankcolname} (w={stageweight})'
        masterdf[wrankcolname] = (masterdf[newrankcolname] * stageweight)
        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wrankcolname)
        # ADD WEIGHT TO WEIGHT TOTAL
        weight_total += stageweight
    # sum weighted rankcols
    masterwrankcolname = f'MASTER WEIGHTED RANK {weight_total}'
    masterdf[masterwrankcolname] = masterdf[sumcols].sum(axis=1, min_count=len(sumcols))
    # rank overall weighted rankcol
    finalrankcolname = 'MASTER FINAL RANK'
    masterdf[finalrankcolname] = masterdf[masterwrankcolname].rank(ascending=1)
    # RE-SORT AND RE-INDEX
    masterdf.sort_values(ascending=True, by=[finalrankcolname], inplace=True)
    masterdf.reset_index(drop=True, inplace=True)
    # save is requested
    filename = "multistagerankings"
    if savemode == 'pkl':
        savetopkl(filename, savedir, masterdf)
    elif savemode == 'csv':
        masterdf.to_csv(index=False, path_or_buf=savedir / f"{filename}.csv")
    return masterdf


# GIVEN STRAT PANEL, EXISTENCE DATE, RETURNS RESULTING DF AND POOL
def getstratdfandpool(verbose, trialdir, exist_date, strat_panel, currentpool, rankmeth, rankregime, savemode, chunksize):
    setreboundbotdates = 'no'
    if strat_panel['multistageweightmode'] == 'yes':
        # for each stage in strat panel, return resulting pool
        setofstages = []
        for stagenum, stagescript in strat_panel.items():
            if stagenum != 'multistageweightmode':
                # build stage folders
                stageparent = buildfolders_singlechild(trialdir, f'{stagenum}_parent')
                # get stagedf
                stagedf = getstagedf(verbose, stagescript, exist_date, stageparent, rankmeth, rankregime, currentpool, setreboundbotdates, stagenum, savemode, chunksize)
                if stagenum.startswith('Stage 2') or stagenum.startswith('Stage 1'):
                    # get stagepool
                    resultpool = stagedf['stock'].tolist()
                    currentpool = resultpool
                    if len(currentpool) == 0:
                        print(f'Stage {stagenum}: All remaining stocks were filtered out.')
                        break
                elif stagenum.startswith('Stage 3'):
                    # collect stage data for multistage weighing
                    setofstages.append({'stagedf': stagedf, 'stageweight': stagescript['scriptweight'], 'stagenum': stagenum, 'stagename': stagescript['scriptname']})
                    # if stage reduces size of pool, adjust poolsize for next stage
                    if len(currentpool) > len(stagedf):
                        currentpool = stagedf['stock'].tolist()
        # get master stagedf
        masterstagedf = multistageranking(savemode, trialdir, setofstages, currentpool)
        # get stagepool
        currentpool = masterstagedf['stock'].tolist()
        if len(currentpool) == 0:
            print(f'Stage {stagenum}: All remaining stocks were filtered out.')
    else:
        # for each stage in strat panel, return resulting pool
        for stagenum, stagescript in strat_panel.items():
            if stagenum != 'multistageweightmode':
                # build stage folders
                stageparent = buildfolders_singlechild(trialdir, f'{stagenum}_parent')
                # get stagedf
                stagedf = getstagedf(verbose, stagescript, exist_date, stageparent, rankmeth, rankregime, currentpool, setreboundbotdates, stagenum, savemode, chunksize)
                # get stagepool
                resultpool = stagedf['stock'].tolist()
                currentpool = resultpool
                if len(currentpool) == 0:
                    print(f'Stage {stagenum}: All remaining stocks were filtered out.')
                    break
    return currentpool


# GIVEN STRAT PANEL, EXISTENCE DATE, RETURNS RESULTING POOL
def getstratpool(verbose, trialdir, exist_date, strat_panel, currentpool, rankmeth, rankregime, savemode, chunksize):
    currentpool = getstratdfandpool(verbose, trialdir, exist_date, strat_panel, currentpool, rankmeth, rankregime, savemode, chunksize)
    return currentpool


# RETURNS PERFORMANCE STATS ON GIVEN POOL, PERIOD, BENCHMARK
def getperfstats(verbose, exist_date, testlen, testpool, benchticker):
    # get test period dates
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    # get test period stats
    perfstatdict = mktbeatpoolstats(verbose, testpool, benchticker, test_beg, test_end)
    return perfstatdict
