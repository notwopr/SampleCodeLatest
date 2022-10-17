"""
Title: THRESHOLD VALUE OPTIMIZER.
Date Started: ?
Version: 1.1
Version Start: July 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Uses python minimizers to locate best combination of threshold values for given metricpanel profile, using mktbeatpoolpct on testperiod as the measure of success.

VERSIONS
1.1: Update code.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from scipy.optimize import minimize, Bounds
#   LOCAL APPLICATION IMPORTS
from filelocations import create_nonexistent_folder, buildfolders_parent_cresult_cdump, buildfolders_regime_testrun
from ONETIME_MKTBEATPOOL_MASTERfunc import getmktbeatpoolpct, onetime_mktbeatpool_master
from ONETIME_GETSINGLEPASSPOOL import getsinglepasspool
from BACKTEST_GATHERMETHOD_FILTERANDLAYER_FUNCBASE import getmetcolname


def find_best_param_settings_cruncher(x, optimizer_params, parentfolder, subjectpool, exist_date, testlen, benchticker, verbose):
    # ISOLATE PARAMS TO MODIFY
    metrics_to_run = optimizer_params[0]['method_specific_params']['fnlbatches'][0]['batch']
    # MODIFY THRESHOLD VALUES
    for metricitem in metrics_to_run:
        if metricitem['metricname'] in ['allpctdrop_composite']:
            if verbose == 'verbose':
                currentval = metricitem['threshold']
                metcolname = getmetcolname(metricitem)
                print(f'{metcolname} prev thresh: {currentval}')
            metricitem.update({'threshold': x[0]})
            if verbose == 'verbose':
                print(f'{metcolname} new thresh: {x[0]}')
    # ASSIGN TESTNUMBER
    inputstr = str(x)
    characters_to_remove = "[]-+e. "
    for character in characters_to_remove:
        inputstr = inputstr.replace(character, "")
    testnumber = inputstr[:10]
    # BUILD OPTIMIZER TRY DUMP FOLDERS
    tryparent, tryresults, trydump = buildfolders_parent_cresult_cdump(parentfolder, f'optimizertry_{testnumber}')
    # RUN NEW SETTINGS OVER STARTING POOL
    resultpool = getsinglepasspool(optimizer_params, tryresults, trydump, '', exist_date, subjectpool)
    # GET PROPORTION THAT BEAT INDEX
    if len(resultpool) == 0:
        minimizesolution = 1
    else:
        portbeatsumm = getmktbeatpoolpct(exist_date, testlen, resultpool, benchticker)
        minimizesolution = 1 - portbeatsumm
    return minimizesolution


def find_best_param_settings(lbounds, ubounds, initialguess, exist_date, testnumber, todaysdate, testregimeparent, testregimename, preoptfilter_dict, optimizer_params, testlen, benchticker, verbose):
    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(testregimeparent, testnumber, todaysdate, testregimename)
    # BUILD SUBJECT POOL DUMP FOLDER
    subjectpooldump = testrunparent / 'subjectpooldump'
    create_nonexistent_folder(subjectpooldump)
    # GET PRE-OPTIMIZER POOL
    subjectpool = onetime_mktbeatpool_master(subjectpooldump, testnumber, todaysdate, 'subjectpool', exist_date, 'no', benchticker, preoptfilter_dict, testlen)
    # BUILD OPTIMIZER DUMP FOLDER
    optimizer_dump = testrunparent / 'optimizerdump'
    create_nonexistent_folder(optimizer_dump)
    # RUN OPTIMIZER
    bounds = Bounds(lbounds, ubounds)
    res = minimize(
        find_best_param_settings_cruncher,
        x0=initialguess,
        args=(optimizer_params, optimizer_dump, subjectpool, exist_date, testlen, benchticker, verbose),
        bounds=bounds,
        method='Powell'
    )
    print(res)
