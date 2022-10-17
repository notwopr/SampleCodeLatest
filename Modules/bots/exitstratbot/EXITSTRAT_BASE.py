"""
Title: EXIT STRAT BASE
Date Started: Dec 1, 2020
Version: 1.00
Version Start: Dec 1, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Trying to figure out whether it is good to take out small profits along the way or keep 100% exposed until end of term?
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import pickle as pkl
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from tickerportalbot import tickerportal3
from timeperiodbot import getrandomexistdate_multiple
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source
from filelocations import buildfolders_singlechild, savetopkl, buildfolders_regime_testrun, buildfolders_parent_cresult_cdump, readpkl
#from STRATTEST_SINGLE_BASE_CRUNCHER import stagecruncher
from STRATTEST_FUNCBASE_RAW import slopescore_single, unifatshell_single
from correlationresearch import twolistcorr
from filetests import checknum
from computersettings import computerobject


# GIVEN STRAT PANEL, EXISTENCE DATE, RETURNS RESULTING DF AND POOL
'''
def getstratpool(verbose, trialdir, beg_date, end_date, strat_panel, currentpool, rankmeth, rankregime):
    # for each stage in strat panel, return resulting pool
    for stagenum, stagescript in strat_panel.items():
        # build stage folders
        stageparent, stageresults, stagedump = buildfolders_parent_cresult_cdump(trialdir, f'{stagenum}_parent')
        # get stagedf
        stagedf = stagecruncher(stageresults, stagedump, stagenum, stagescript, beg_date, end_date, currentpool, rankmeth, rankregime)
        # get stagepool
        resultpool = stagedf['stock'].tolist()
        currentpool = resultpool
        if len(currentpool) == 0:
            print(f'Stage {stagenum}: All remaining stocks were filtered out.')
            break
    return currentpool
'''


# report comparison of HOLD to STRAT
def reporter(stratdesc, stratname, cash_final, profits_final, taxes_final, global_params):
    networth_change = cash_final - global_params["cap_start"]
    atnetworth_change = (cash_final - taxes_final) - global_params["cap_start"]
    print('\n')
    print(f'{stratdesc}, you would have the following:')
    print(f'{stratname} networth change {networth_change} ({(networth_change / global_params["cap_start"]) * 100}) %')
    print(f'{stratname} aftertax networth change {atnetworth_change} ({(atnetworth_change / global_params["cap_start"]) * 100}) %')
    print({
        'start cap': global_params['cap_start'],
        f'{stratname} networth': cash_final,
        f'{stratname} After-Tax networth': cash_final - taxes_final,
        f'{stratname} Cumulative Profits': profits_final,
        f'{stratname} After-Tax Cumulative Profits': profits_final - taxes_final,
        f'{stratname} Total Tax Bill': taxes_final
        }
    )


# buy or sell transaction
def transaction(action, price_transaction, shares_transacted, cash, shares_owned, verbose):
    if action == 'buy':
        total = shares_transacted * price_transaction
        cash_after = cash - total
        shares_after = shares_owned + shares_transacted
    if action == 'sell':
        total = shares_transacted * price_transaction
        cash_after = cash + total
        shares_after = shares_owned - shares_transacted
    # report transaction
    if verbose == 'verbose':
        print({
            'action': action,
            'shares before': shares_owned,
            'shares transacted': shares_transacted,
            'shares after': shares_after,
            'transaction price': price_transaction,
            'total transaction': total,
            'cash before': cash,
            'cash after': cash_after
            })
    return cash_after, shares_after


# calculate profits and taxes
def profitsandtaxes(shares_sold, price_sold, price_basis, profits_cumulative, taxes_cumulative, taxrate, verbose):
    profit = shares_sold * (price_sold - price_basis)
    profits_after = profits_cumulative + profit
    if profit > 0:
        taxes = profit * taxrate
    else:
        taxes = 0
    taxes_after = taxes_cumulative + taxes
    if verbose == 'verbose':
        print({
            'profit': profit,
            'profits before': profits_cumulative,
            'profits after': profits_after,
            'taxes': taxes,
            'taxes before': taxes_cumulative,
            'taxes after': taxes_after,
            })
    return profits_after, taxes_after


# run strat on each day
def executestrat(strat, fullprices, shares_owned, cash, global_params):
    firstprice = fullprices.iat[0, 1]
    profits_cumulative = 0
    taxes_cumulative = 0
    for eachday in fullprices.index:
        if eachday > 0:
            # get pre-action state
            price_curr = fullprices.iat[eachday, 1]
            stockval_curr = shares_owned * price_curr
            exposure_curr = stockval_curr
            exposure_excess = (exposure_curr - global_params['cap_start']) / global_params['cap_start']
            if global_params['verbose'] == 'verbose':
                print(f'Current Exposure as of {fullprices.iat[eachday, 0]}: {exposure_curr}. Exposure in excess of {global_params["cap_start"]}: {exposure_excess}')
            # sell if total exposure exceeds startcap by X%
            if exposure_excess >= global_params['selltrigger']:
                if strat == 'shave':
                    # sell amount of shares such that value of shares remaining equals start capital
                    shares_sell = (stockval_curr - global_params['cap_start']) / price_curr
                    cash_after, shares_after = transaction('sell', price_curr, shares_sell, cash, shares_owned, global_params['verbose'])
                    # calculate profit and taxes
                    profits_cumulative, taxes_cumulative = profitsandtaxes(shares_sell, price_curr, firstprice, profits_cumulative, taxes_cumulative, global_params['taxrate'], global_params['verbose'])
                elif strat == 'reset':
                    # exit entire position and repurchase back amount equal to starting cap
                    shares_sell = shares_owned
                    cash_after, shares_after = transaction('sell', price_curr, shares_sell, cash, shares_owned, global_params['verbose'])
                    # calculate profit and taxes
                    profits_cumulative, taxes_cumulative = profitsandtaxes(shares_sell, price_curr, firstprice, profits_cumulative, taxes_cumulative, global_params['taxrate'], global_params['verbose'])
                    # repurchase shares
                    shares_repurchase = global_params['cap_start'] / price_curr
                    cash_after, shares_after = transaction('buy', price_curr, shares_repurchase, cash_after, shares_after, global_params['verbose'])
                    firstprice = price_curr
                shares_owned = shares_after
                cash = cash_after
            else:
                cash_after = cash
                shares_after = shares_owned
    return firstprice, cash_after, shares_after, profits_cumulative, taxes_cumulative


# sell all shares owned
def exitsale(firstprice, lastprice, shares_owned, cash, profits_cumulative, taxes_cumulative, global_params):
    # sell transaction
    cash_after, shares_after = transaction('sell', lastprice, shares_owned, cash, shares_owned, global_params['verbose'])
    # calculate profit and taxes
    profits_cumulative, taxes_cumulative = profitsandtaxes(shares_owned, lastprice, firstprice, profits_cumulative, taxes_cumulative, global_params['taxrate'], global_params['verbose'])
    return cash_after, shares_after, profits_cumulative, taxes_cumulative


# MASTER FUNCTION: ASSEMBLES PROPORTIONS OF ALL TRIALS
def exitstrat_master(trialresultparent, trialno, beg_date, end_date, global_params, stock):
    # establish trialsummary
    trialsummary = {
        'trialno': trialno,
        'testlen': global_params['testlen'],
        'stock': stock,
        'test_beg': beg_date,
        'test_end': end_date
        }
    # get all prices
    fullprices = grabsinglehistory(stock)
    fullprices = fill_gaps2(fullprices, beg_date, end_date)
    # reset index
    fullprices.reset_index(drop=True, inplace=True)
    lastprice = fullprices.iat[-1, 1]
    # enter position
    price_enter = fullprices.iat[0, 1]
    shares_enter = global_params['cap_start'] / price_enter
    cash_afterenter, shares_afterenter = transaction('buy', price_enter, shares_enter, global_params['cap_start'], 0, global_params['verbose'])
    # get hold stats
    hold_cash, hold_shares, hold_profits, hold_taxes = exitsale(price_enter, lastprice, shares_afterenter, cash_afterenter, 0, 0, global_params)
    # execute strat and report results
    for strat in ['hold', 'shave', 'reset']:
        if strat != 'hold':
            # execute strat
            firstprice, cash_after, shares_after, profits_cumulative, taxes_cumulative = executestrat(strat, fullprices, shares_afterenter, cash_afterenter, global_params)
            # final sale
            cash_final, shares_final, profits_final, taxes_final = exitsale(firstprice, lastprice, shares_after, cash_after, profits_cumulative, taxes_cumulative, global_params)
            # update trialsummary
            if hold_taxes != 0:
                trialsummary.update({
                    f'diff_taxes ({strat} vs HOLD) (%)': ((taxes_final - hold_taxes) / hold_taxes) * 100,
                    f'diff_networth ({strat} vs HOLD) (%)': ((cash_final - hold_cash) / hold_cash) * 100,
                    f'diff_atnetworth ({strat} vs HOLD) (%)': (((cash_final - taxes_final) - (hold_cash - hold_taxes)) / (hold_cash - hold_taxes)) * 100
                    })
            else:
                trialsummary.update({
                    f'diff_taxes ({strat} vs HOLD) (%)': np.inf,
                    f'diff_networth ({strat} vs HOLD) (%)': ((cash_final - hold_cash) / hold_cash) * 100,
                    f'diff_atnetworth ({strat} vs HOLD) (%)': (((cash_final - taxes_final) - (hold_cash - hold_taxes)) / (hold_cash - hold_taxes)) * 100
                    })
        # report
        if global_params['verbose'] == 'verbose':
            if strat == 'hold':
                stratdesc = 'If you held your position for the entire investment period without selling'
                stratname = 'HOLD'
            elif strat == 'shave':
                stratdesc = 'If you sold periodically during the investment period to maintain a constant exposure'
                stratname = 'SHAVE'
            elif strat == 'reset':
                stratdesc = 'If you sold periodically during the investment period to maintain a constant exposure, but you exited the entire position and repurchased instead'
                stratname = 'RESET'
            if strat == 'hold':
                reporter(stratdesc, stratname, hold_cash, hold_profits, hold_taxes, global_params)
            else:
                reporter(stratdesc, stratname, cash_final, profits_final, taxes_final, global_params)
    # create master stat objects
    slopescore = slopescore_single(fullprices)
    unifatscore = unifatshell_single(fullprices, 'straight', stock, 'avg')
    # update trialsummary
    trialsummary.update({
        'slopescore': slopescore,
        'unifatscore_rawstraight_avg': unifatscore
        })
    # save stats
    savetopkl(f'trialsumm{trialno}', trialresultparent, trialsummary)
    # report differences
    if global_params['verbose'] == 'verbose':
        print('\n')
        print(trialsummary)


# single exitstrat trial
def gettargetstock(stockdictsfolder, global_params, trial):
    trialno = trial[0]
    exist_date = trial[1]
    # build folders for trial
    #trialparent = buildfolders_singlechild(trialdumpparent, f'trialno{trialno}_edate{exist_date}')
    # get existing stocks
    startpool = tickerportal3(exist_date, 'common', 2)
    # get testperiod
    beg_date = exist_date
    end_date = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=global_params['testlen']))
    # further filter stocks by params
    #startpool = getstratpool('', trialparent, beg_date, end_date, global_params['filterpanel'], startpool, global_params['rankmeth'], global_params['rankregime'])
    # use first stock in list
    stock = startpool[0]
    stockdict = {
        'stock': stock,
        'trialno': trialno,
        'beg_date': beg_date,
        'end_date': end_date
        }
    savetopkl(f'stockdict_trial{trialno}', stockdictsfolder, stockdict)


# get target stock multiprocessor
def targetstock_master(stockdictsfolder, global_params, alltrialexistdates):
    # run multitrial processor to process strategies
    fn = partial(gettargetstock, stockdictsfolder, global_params)
    pool = Pool(processes=computerobject.use_cores)
    pool.map(fn, enumerate(alltrialexistdates), 1)
    pool.close()
    pool.join()
    # wait for all files to download
    correct = len(alltrialexistdates)
    downloadfinish = checknum(stockdictsfolder, correct, '')
    while downloadfinish is False:
        downloadfinish = checknum(stockdictsfolder, correct, '')


# multiprocessor shell for exit strat
def exitstratshell(stockdictsfolder, trialresultparent, global_params, trial):
    trialno = trial[0]
    # open stockdict
    stockdict = readpkl(f'stockdict_trial{trialno}', stockdictsfolder)
    # run exitstrat
    exitstrat_master(trialresultparent, trialno, stockdict['beg_date'], stockdict['end_date'], global_params, stockdict['stock'])


# exit strat multiprocessor master
def exitstrat_processormaster(trialresultparent, stockdictsfolder, global_params, alltrialexistdates):
    # run multitrial processor to process strategies
    fn = partial(exitstratshell, stockdictsfolder, trialresultparent, global_params)
    pool = Pool(processes=computerobject.use_cores)
    pool.map(fn, enumerate(alltrialexistdates), 1)
    pool.close()
    pool.join()
    # wait for all files to download
    correct = len(alltrialexistdates)
    downloadfinish = checknum(trialresultparent, correct, '')
    while downloadfinish is False:
        downloadfinish = checknum(trialresultparent, correct, '')


# MULTITRIAL
def exitstrat_multitrial(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # build stage folders
    #trialdumpparent = buildfolders_singlechild(testrunparent, 'trialdumpparent')
    trialresultparent = buildfolders_singlechild(testrunparent, 'trialresultparent')
    stockdictsfolder = buildfolders_singlechild(testrunparent, 'stockdicts')
    # get trialexistdates
    alltrialexistdates = getrandomexistdate_multiple(global_params['num_trials'], global_params['firstdate'], global_params['latestdate'], global_params['testlen'], daterangedb_source)
    # for each trialdate get stockname, dates, and trialno
    #for trial in enumerate(alltrialexistdates):
        #gettargetstock(trialdumpparent, stockdictsfolder, global_params, trial)
    targetstock_master(stockdictsfolder, global_params, alltrialexistdates)
    # run exitstrat calculations
    exitstrat_processormaster(trialresultparent, stockdictsfolder, global_params, alltrialexistdates)
    # construct mastertrialdf
    table_results = []
    for child in trialresultparent.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    alltrialsummdf = pd.DataFrame(data=table_results)
    # sort by trial number
    alltrialsummdf.sort_values(by='trialno', ascending=True, inplace=True)
    alltrialsummdf.reset_index(inplace=True, drop=True)
    # save results
    dfname = "exitstrat_multitrial_summary"
    alltrialsummdf.to_csv(index=False, path_or_buf=testrunparent / f"{dfname}.csv")
    dfname = "exitstrat_multitrial_summary"
    alltrialsummdf = pd.read_csv(testrunparent / f"{dfname}.csv")
    # CALCULATE CORRELATIONS
    # drop rows that contain infs
    alltrialsummdf.drop(alltrialsummdf[alltrialsummdf.isin([np.inf]).any(axis=1)].index.tolist(), inplace=True)
    compdict = {}
    for strat in ['shave', 'reset']:
        compdict.update({
            f'{strat}_taxes': f'diff_taxes ({strat} vs HOLD) (%)',
            f'{strat}_networth': f'diff_networth ({strat} vs HOLD) (%)',
            f'{strat}_atnetworth': f'diff_atnetworth ({strat} vs HOLD) (%)'
        })
    maindict = {
        'slopescore': 'slopescore',
        'unifatscore': 'unifatscore_rawstraight_avg'
    }
    corrdict = {}
    for key, val in maindict.items():
        for key1, val1 in compdict.items():
            corrdict.update({
                f'{key}_{key1} corr': twolistcorr(alltrialsummdf[val].tolist(), alltrialsummdf[val1].tolist(), 'pearson')
            })
    # get column averages
    for key1, val1 in compdict.items():
        corrdict.update({
            f'{val1} median': alltrialsummdf[val1].median()
        })
    corrdf = pd.DataFrame(data=[corrdict])
    # transpose df
    corrdf = corrdf.transpose()
    corrdf.reset_index(inplace=True)
    corrdf.rename(columns={'index': 'category', 0: 'value'}, inplace=True)
    # save corr results
    corrdf.to_csv(index=False, path_or_buf=testrunparent / "corrvals.csv")
