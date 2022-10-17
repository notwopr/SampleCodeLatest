"""
Title: Best Part of the Year Predictor Bot Multi Accuracy Collation
Date Started: Dec 14, 2020
Version: 1.0
Version Start: Dec 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Takes a set of lookbackchunks and runs accuracy tests on each and returns dataframe with all accuracy test results.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import copy
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_regime_testrun, buildfolders_singlechild, savetopkl
from BPOTYBOT_PREDICTOR_BASE import getpredictions, getaccuracyscores
from genericfunctionbot import multiprocessorshell
from BPOTYBOT_BASE import get_poty_average


def lookbackpredictions(rootdir, global_params, bpotysourcedf):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # get maxchunk
    if global_params['potydef'] == 'year':
        maxchunk = 1
    else:
        maxchunk = int(bpotysourcedf.columns[-1][11:])
    # get predictions
    origwithunknowndf, predictionsdf = getpredictions(testrunparent, bpotysourcedf, global_params['lookbackchunks'], maxchunk, global_params['potydef'], global_params['potylen'])
    # get accuracy scores
    origwithunknowndf = getaccuracyscores(testrunparent, global_params['lookbackchunks'], maxchunk, predictionsdf, origwithunknowndf, global_params['potydef'], global_params['potylen'], global_params['signaltrigger'])
    return origwithunknowndf


def getaccuracydf_single(savedir, testrunparent, global_params, bpotysourcedf, lbvalue):
    # create dumpfolder
    lbstrengthdump = buildfolders_singlechild(testrunparent, f'lbstrengthdump_{lbvalue}')
    # add lbchunk to globalparams
    modparams = copy.deepcopy(global_params)
    modparams.update({'lookbackchunks': lbvalue})
    accuracydf = lookbackpredictions(lbstrengthdump, modparams, bpotysourcedf)
    # save to savedir
    savetopkl(f'accuracydf_LB{lbvalue}', savedir, accuracydf)


def lookbackpredictions_multi(rootdir, global_params, lbvalues):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # get bpotysource
    if global_params['bpotysource'] != "":
        bpotysourcedf = pd.read_csv(global_params['bpotysource'])
    else:
        bpotysourcedf = get_poty_average(global_params['verbose'], global_params['beg_date'], global_params['end_date'], global_params['potydef'], global_params['potylen'], global_params['ticker'], testrunparent)
    # create masterdf
    masterdf = bpotysourcedf[['YEAR']].copy()
    # create dumpfolder for all accuracydfs
    accuracydfresults = buildfolders_singlechild(testrunparent, 'allaccuracydfs')
    # for each lbchunk, get accuracy df by year
    targetvars = (accuracydfresults, testrunparent, global_params, bpotysourcedf)
    multiprocessorshell(accuracydfresults, getaccuracydf_single, lbvalues, 'no', targetvars, global_params['chunksize'])
    # for each accuracydf in accuracydfs results folder...
    for child in accuracydfresults.iterdir():
        # open accuracydf
        with open(child, "rb") as targetfile:
            accuracydf = pkl.load(targetfile)
        # reduce accuracy df to just year and accuracy rate columns
        accuracyratecolname = accuracydf.columns[-1]
        accuracydf = accuracydf[['YEAR', accuracyratecolname]].copy()
        # and join to masterdf
        masterdf = masterdf.join(accuracydf.set_index('YEAR'), how="left", on="YEAR")
    # save masterdf
    filename = f'multiLBchunkaccuracies_potylen{global_params["potylen"]}_signaltrigger{global_params["signaltrigger"]}'
    masterdf.to_csv(index=False, path_or_buf=testrunparent / f"{filename}.csv")
