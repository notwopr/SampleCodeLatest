"""
Title: OPTIMAL PARAM FINDER - METRIC PANEL ACCURACY
Date Started: July 21, 2020
Version: 1.01
Version Start: July 22, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given an Ideal Portfolio for given test period, this bot returns portfolio when applying a metricpanel filter to the selection period associated with that ideal portfolio and compares the resulting portfolio with the ideal one.
Versions:
1.01: Added gui for manually entering in thresholds.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import copy
#   THIRD PARTY IMPORTS
import easygui
#   LOCAL APPLICATION IMPORTS
from ONETIME_GETSINGLEPASSPOOL import getsinglepasspool
from tickerportalbot import tickerportal2
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source, tickerlistcommon_source
from filelocations import buildfolders_parent_cresult_cdump


# RETURNS PARAMSETTINGS BASED ON GIVEN IDEAL PORTFOLIO-SELECT-TEST-PERIOD
def getfiltermetricparams(mktbeatstatsummdf, metrics_to_run, num_bounds):

    newmetrics_to_run = []
    for metricitem in metrics_to_run:
        metricname = metricitem['metricname']
        rankdirection = metricitem['rankascending']
        minval = mktbeatstatsummdf[mktbeatstatsummdf['metricname'] == metricname]['stat_min'].item()
        maxval = mktbeatstatsummdf[mktbeatstatsummdf['metricname'] == metricname]['stat_max'].item()
        if rankdirection == 0:
            threshdir = 'a LOWER'
        elif rankdirection == 1:
            threshdir = 'an UPPER'
        # make copy of metricitem dict
        newmetricitem = copy.deepcopy(metricitem)
        # determine whether to set lower or upper threshold or both
        if num_bounds == 'singlebound':
            singlebound = easygui.enterbox(f'Please enter {threshdir} bound:\nMETRICNAME: {metricname}\nMAX: {maxval} \nMIN: {minval}')
            singlebound = float(singlebound)
            # update threshold value
            newmetricitem.update({'threshold': singlebound})
        elif num_bounds == 'doublebound':
            upperbound = easygui.enterbox(f'Please enter an UPPER bound:\nMETRICNAME: {metricname}\nMAX: {maxval} \nMIN: {minval}')
            lowerbound = easygui.enterbox(f'Please enter a LOWER bound:\nMETRICNAME: {metricname}\nMAX: {maxval} \nMIN: {minval}')
            upperbound = float(upperbound)
            lowerbound = float(lowerbound)
            # update threshold value
            newmetricitem.update({'upperthreshold': upperbound})
            newmetricitem.update({'lowerthreshold': lowerbound})
        # add to final object
        newmetrics_to_run.append(newmetricitem)
    return newmetrics_to_run


# RETURNS SCORE HOW WELL TEST POOL MATCHES MODEL POOL
def poolmatchscore(verbose, modelpool, testpool):

    # get number of stocks that are both in modelpool and testpool
    stocks_match = [item for item in testpool if item in modelpool]
    # stocks in modelpool not in testpool
    stocks_miss = [item for item in modelpool if item not in testpool]
    # stocks in testpool not in modelpool
    stocks_xtra = [item for item in testpool if item not in modelpool]
    num_matches = len(stocks_match)
    num_model = len(modelpool)
    num_test = len(testpool)
    num_miss = len(stocks_miss)
    num_xtra = len(stocks_xtra)
    hitscore = num_matches / num_model
    # accuracy when the number of missing stocks and extra stocks is small
    matchscore = 1 - (num_miss + num_xtra) / (num_model + num_test)
    if verbose == 'verbose':
        print(f'modelpool: {modelpool}')
        print(f'testpool: {testpool}')
        print(f'stockmatches: {stocks_match}')
        print(f'stocks missing: {stocks_miss}')
        print(f'excess stocks: {stocks_xtra}')
        print(f'num_matches: {num_matches}')
        print(f'num_model: {num_model}')
        print(f'num_test: {num_test}')
        print(f'num_miss: {num_miss}')
        print(f'num_xtra: {num_xtra}')
        print(f'hitscore: {hitscore}')
        print(f'matchscore: {matchscore}')
    return matchscore


def getmpaccuracy(testrunparent, exist_date, newmetricpanel_params, mktbeaterpool):
    # build mp check folders
    mpcheckparent, mpcheckresults, mpcheckdump = buildfolders_parent_cresult_cdump(testrunparent, 'mpcheckdump')
    # get mpcheckpool from firstpasspool
    fullpool = tickerportal2(exist_date, 'common')
    mpcheckpool = getsinglepasspool(newmetricpanel_params, mpcheckresults, mpcheckdump, '', exist_date, fullpool)
    # run accuracy test
    poolmatchscore('verbose', mktbeaterpool, mpcheckpool)
