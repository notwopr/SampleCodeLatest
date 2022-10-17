"""
Title: TRADE STRAT BASE
Date Started: Dec 15, 2020
Version: 1.00
Version Start: Dec 15, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Compares end networth of custom strategy and hold strategy over specified investment period on a specific stock.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from filelocations import buildfolders_singlechild, buildfolders_regime_testrun
from BPOTYBOT_BASE import getpotynamesandperiods, getbpotychart
from BPOTYBOT_PREDICTOR_BASE import getpredictions, signalcell_predict


# networth reporter
def networthreporter(cash_current, shares_current, price_current, profits_cumulative, taxes_cumulative, stratname):
    networth_current = cash_current + (shares_current * price_current)
    atnetworth_current = networth_current - taxes_cumulative
    summary = {
        f'{stratname}_networth': networth_current,
        f'{stratname}_After-Tax networth': atnetworth_current,
        f'{stratname}_After-Tax Cumulative Profits': profits_cumulative - taxes_cumulative,
        f'{stratname}_Cumulative Profits': profits_cumulative,
        f'{stratname}_Cumulative Taxes': taxes_cumulative
        }
    return summary


# buy or sell transaction
def transaction(action, price_transaction, shares_transacted, cash, shares_owned, stratname, verbose):
    if action == 'buy':
        total = shares_transacted * price_transaction
        cash_after = cash - total
        shares_after = shares_owned + shares_transacted
    if action == 'sell':
        total = shares_transacted * price_transaction
        cash_after = cash + total
        shares_after = shares_owned - shares_transacted
    summary = {
        f'{stratname}_action': action,
        f'{stratname}_shares before': shares_owned,
        f'{stratname}_shares transacted': shares_transacted,
        f'{stratname}_shares after': shares_after,
        f'{stratname}_transaction price': price_transaction,
        f'{stratname}_total transaction': total,
        f'{stratname}_cash before': cash,
        f'{stratname}_cash after': cash_after
        }
    # report transaction
    if verbose == 'verbose':
        print(summary)
    return cash_after, shares_after, summary


# calculate profits and taxes
def profitsandtaxes(shares_sold, price_sold, price_basis, profits_cumulative, taxes_cumulative, taxrate, stratname, verbose):
    profit = shares_sold * (price_sold - price_basis)
    profits_after = profits_cumulative + profit
    if profit > 0:
        taxes = profit * taxrate
    else:
        taxes = 0
    taxes_after = taxes_cumulative + taxes
    summary = {
        f'{stratname}_profit': profit,
        f'{stratname}_profits before': profits_cumulative,
        f'{stratname}_profits after': profits_after,
        f'{stratname}_taxes': taxes,
        f'{stratname}_taxes before': taxes_cumulative,
        f'{stratname}_taxes after': taxes_after,
        }
    # report transaction
    if verbose == 'verbose':
        print(summary)
    return profits_after, taxes_after, summary


# returns signal of the timechunk enclosing the given date
def getsignalbydate(verbose, date, maxchunk, all_periods, predictionsdf, potylen):
    yearcounter = 0
    for year in predictionsdf['YEAR']:
        chunkcounter = 0
        for timechunk in range(1, maxchunk+1):
            # if date within this chunk
            if dt.date.fromisoformat(date) <= dt.date.fromisoformat(all_periods[yearcounter][chunkcounter][1]) and dt.date.fromisoformat(date) >= dt.date.fromisoformat(all_periods[yearcounter][chunkcounter][0]):
                # get prediction of this timechunk
                timechunksignal = predictionsdf[predictionsdf['YEAR'] == year][f'{potylen}-daychunk{timechunk}'].item()
                if verbose == 'verbose':
                    print({
                        'year': year,
                        'timechunk': timechunk,
                        'leftbound': all_periods[yearcounter][chunkcounter][0],
                        'rightbound': all_periods[yearcounter][chunkcounter][1],
                        'inputdate': date,
                        'predictsignal': timechunksignal
                        })
            chunkcounter += 1
        yearcounter += 1
    return timechunksignal


# create slim version of trade df for attaching to master df in the end
def slimifydf(origdf, stratname):
    # convert datecol to pandas date objects
    origdf['date'] = pd.to_datetime(origdf['date'])
    # log only essential columns
    colstokeep = [
        'date',
        f'{stratname}_networth',
        f'{stratname}_After-Tax networth',
        f'{stratname}_After-Tax Cumulative Profits',
        f'{stratname}_Cumulative Profits',
        f'{stratname}_Cumulative Taxes'
        ]
    slimdf = origdf[colstokeep].copy()
    return slimdf


# nonhold strategy
def runstrat_singleday(verbose, daysummary, stratname, iterdate, iterprice, cash_current, shares_current, profits_cumulative, taxes_cumulative, taxrate, price_buy, position_status, stratspecificparams):
    if stratname != 'HOLD':
        # unpack strat specific params
        maxchunk = stratspecificparams[0]
        all_periods = stratspecificparams[1]
        predictionsdf = stratspecificparams[2]
        buytrigger = stratspecificparams[3]
        selltrigger = stratspecificparams[4]
        potylen = stratspecificparams[5]
        # if position closed
        if position_status == 'closed':
            # get timechunk signal
            timechunksignal = getsignalbydate(verbose, iterdate, maxchunk, all_periods, predictionsdf, potylen)
            # if timechunksignal not NAN and exceeds buytrigger, enter position
            if (timechunksignal is None) == False:
                # if signals are in symbols
                if (type(timechunksignal) == str and timechunksignal == buytrigger) or (type(timechunksignal) == float and timechunksignal > buytrigger):
                    price_buy = iterprice
                    shares_buy = cash_current / price_buy
                    cash_current, shares_current, transactsummary = transaction('buy', price_buy, shares_buy, cash_current, shares_current, stratname, verbose)
                    daysummary.update(transactsummary)
                    # update position status
                    position_status = 'open'
        # if position open
        elif position_status == 'open':
            # get timechunk signal
            timechunksignal = getsignalbydate(verbose, iterdate, maxchunk, all_periods, predictionsdf, potylen)
            # if timechunksignal not NAN and exceeds selltrigger, exit position
            if (timechunksignal is None) == False:
                # if signals are in symbols
                if (type(timechunksignal) == str and timechunksignal == selltrigger) or (type(timechunksignal) == float and timechunksignal < selltrigger):
                    price_sell = iterprice
                    shares_sell = shares_current
                    cash_current, shares_current, transactsummary = transaction('sell', price_sell, shares_sell, cash_current, shares_current, stratname, verbose)
                    profits_cumulative, taxes_cumulative, ptsummary = profitsandtaxes(shares_sell, price_sell, price_buy, profits_cumulative, taxes_cumulative, taxrate, stratname, verbose)
                    daysummary.update(transactsummary)
                    daysummary.update(ptsummary)
                    # update position status
                    position_status = 'closed'
    elif stratname == 'HOLD':
        # unpack strat specific params
        earliestdate = stratspecificparams[0]
        latestdate = stratspecificparams[1]
        # if it is the first day, buy shares
        if iterdate == earliestdate:
            price_buy = iterprice
            shares_buy = cash_current / price_buy
            cash_current, shares_current, transactsummary = transaction('buy', price_buy, shares_buy, cash_current, shares_current, stratname, verbose)
            daysummary.update(transactsummary)
            # update position status
            position_status = 'open'
        # if it is the last day, exit shares
        elif iterdate == latestdate:
            price_sell = iterprice
            shares_sell = shares_current
            cash_current, shares_current, transactsummary = transaction('sell', price_sell, shares_sell, cash_current, shares_current, stratname, verbose)
            profits_cumulative, taxes_cumulative, ptsummary = profitsandtaxes(shares_sell, price_sell, price_buy, profits_cumulative, taxes_cumulative, taxrate, stratname, verbose)
            daysummary.update(transactsummary)
            daysummary.update(ptsummary)
            # update position status
            position_status = 'closed'
    daysummary.update({'position_status': position_status})
    return daysummary, cash_current, shares_current, profits_cumulative, taxes_cumulative, price_buy, position_status


# execute stratshell
def stratshell(verbose, stratdfstojoin, savedir, ticker, prices, cap_start, taxrate, stratname, stratspecificparams):
    alldaysummaries = []
    position_status = 'closed'
    cash_current = cap_start
    shares_current = 0
    profits_cumulative = 0
    taxes_cumulative = 0
    price_buy = 0
    # for each day in price range
    for eachday in prices.index:
        # get current date and price
        iterdate = str(prices.iat[eachday, 0].date())
        iterprice = prices.iat[eachday, 1]
        daysummary = {'date': iterdate}
        # run strat on single day
        daysummary, cash_current, shares_current, profits_cumulative, taxes_cumulative, price_buy, position_status = runstrat_singleday(verbose, daysummary, stratname, iterdate, iterprice, cash_current, shares_current, profits_cumulative, taxes_cumulative, taxrate, price_buy, position_status, stratspecificparams)
        # update networth summary
        networthsummary = networthreporter(cash_current, shares_current, iterprice, profits_cumulative, taxes_cumulative, stratname)
        daysummary.update(networthsummary)
        alldaysummaries.append(daysummary)
    # create stratdf
    stratdf = pd.DataFrame(data=alldaysummaries)
    # save stratdf
    filename = f"stratdf{stratname}_{ticker}"
    stratdf.to_csv(index=False, path_or_buf=savedir / f"{filename}.csv")
    # create condensed version
    stratdf = slimifydf(stratdf, stratname)
    # save df to list to join
    stratdfstojoin.append(stratdf)
    return stratdfstojoin


# convert predictiondf to signal version
def getsignalpredictiondf(dumpfolder, predictionsdf, signaltrigger):
    # convert prediction probabilities to signal form
    predictionsdf.iloc[:, 1:] = predictionsdf.iloc[:, 1:].applymap(lambda x: signalcell_predict(x, signaltrigger))
    # save
    predictionsdf.to_csv(index=False, path_or_buf=dumpfolder / "predictionsdfsymbols.csv")
    return predictionsdf


# MASTER FUNCTION: ASSEMBLES PROPORTIONS OF ALL TRIALS
def tradestrat_master(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # FIND EARLIEST AND LATEST DATE AVAILABLE
    rawprices = grabsinglehistory(global_params['ticker'])
    prices = fill_gaps2(rawprices, global_params['beg_date'], global_params['end_date'])
    prices.reset_index(drop=True, inplace=True)
    earliestdate = str(prices.iat[0, 0].date())
    latestdate = str(prices.iat[-1, 0].date())
    # establish object to collect progressiondfs to join to masterdf at end
    stratdfstojoin = []
    # for each strat to run, collect strat results and join to list of strats to report in final masterdf
    for stratname in ['HOLD', f'pastLB{global_params["lookbackchunks"]}']:
        if stratname != 'HOLD':
            # get full price history for making best predictions
            predictprices = fill_gaps2(rawprices, '', '')
            predictprices.reset_index(drop=True, inplace=True)
            predictearliestdate = str(predictprices.iat[0, 0].date())
            predictlatestdate = str(predictprices.iat[-1, 0].date())
            # get all periods, poty names and testyears
            all_periods, poty_names, testyears = getpotynamesandperiods(global_params['verbose'], global_params['potydef'], global_params['potylen'], predictearliestdate, predictlatestdate)
            # get bpotychart
            if global_params['bpotysource'] != '':
                bpotysourcedf = pd.read_csv(global_params['bpotysource'])
            else:
                bpotychartdump = buildfolders_singlechild(testrunparent, 'bpotychartdump')
                bpotysourcedf = getbpotychart(global_params['verbose'], bpotychartdump, global_params['potydef'], testyears, all_periods, predictearliestdate, predictlatestdate, global_params['ticker'], predictprices, poty_names)
            # get maxchunk
            maxchunk = int(bpotysourcedf.columns[-1][11:])
            # get predictions
            predictiondfdump = buildfolders_singlechild(testrunparent, 'predictiondfdump')
            origwithunknowndf, predictionsdf = getpredictions(predictiondfdump, bpotysourcedf, global_params['lookbackchunks'], maxchunk, global_params['potydef'], global_params['potylen'])
            # convert predictiondf to signals if requested
            if global_params['buytrigger'] == "+":
                predictionsdf = getsignalpredictiondf(predictiondfdump, predictionsdf, global_params['signaltrigger'])
            # establish stratspecific params
            stratspecificparams = (maxchunk, all_periods, predictionsdf, global_params['buytrigger'], global_params['selltrigger'], global_params['potylen'])
        else:
            # establish stratspecific params
            stratspecificparams = (earliestdate, latestdate)
        # run strat and save results to list of results to join to masterdf
        stratdfstojoin = stratshell(global_params['verbose'], stratdfstojoin, testrunparent, global_params['ticker'], prices, global_params['cap_start'], global_params['taxrate'], stratname, stratspecificparams)
    # join all strat results to price df
    for elemdf in stratdfstojoin:
        prices = prices.join(elemdf.set_index('date'), how="left", on="date")
    # save finaldf
    filename = f"networthprogress_{global_params['ticker']}"
    prices.to_csv(index=False, path_or_buf=testrunparent / f"{filename}.csv")
