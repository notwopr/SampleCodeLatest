"""
Title: Best Part of the Year Predictor Bot
Date Started: Dec 13, 2020
Version: 1.0
Version Start: Dec 13, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Takes an existing BPOTY chart, and given predictor strat, returns prediction accuracy results.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import math
#   THIRD PARTY IMPORTS
import numpy as np
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_regime_testrun, buildfolders_singlechild
from BPOTYBOT_BASE import get_poty_average


# return code for cell
def signalcell(x):
    if np.isnan(x) == True:
        return None
    elif x > 0:
        return '+'
    elif x < 0:
        return '-'
    else:
        return '0'


# return code for cell
def signalcell_predict(x, signaltrigger):
    if np.isnan(x) == True:
        return None
    elif x > signaltrigger:
        return '+'
    elif x < signaltrigger:
        return '-'
    else:
        return '0'


# check that none of the lookbackchunks are nan
def checknanvalues(calculatedf, lookbackchunks, chunkC, year, potydef, potylen):
    lbchunkvals_all = []
    for offsetindex in reversed(range(1, lookbackchunks+1)):
        if potydef != 'year':
            lbchunk = chunkC - offsetindex
            colname = f'{potylen}-daychunk{lbchunk}'
            lbchunkval = calculatedf[calculatedf['YEAR'] == year][colname].item()
        else:
            colname = f'year{-offsetindex}'
            lbchunkval = calculatedf[calculatedf['YEAR'] == year][colname].item()
        lbchunkvals_all.append(lbchunkval)
    # check that none of the lookback values are Nan
    lbchunknanstate = 'no nans exist'
    for elem in lbchunkvals_all:
        if np.isnan(elem) == True:
            lbchunknanstate = 'contains nan'
    return lbchunknanstate


# filter df for same signage pattern in lookbackchunks
def filterdfbysignpattern(calculatedf, year, chunkC, offsetindex, potydef, potylen):
    if potydef != 'year':
        lbchunk = chunkC - offsetindex
        colname = f'{potylen}-daychunk{lbchunk}'
    else:
        colname = f'year{-offsetindex}'
    # get lookbackchunk's value
    colval = calculatedf[calculatedf['YEAR'] == year][colname].item()
    # translate value into positive or negative sign
    if colval > 0:
        colsign = 'pos'
    elif colval < 0:
        colsign = 'neg'
    else:
        colsign = 'zero'
    # filter df by signage
    if colsign == 'pos':
        calculatedf = calculatedf[calculatedf[colname] > 0].copy()
    elif colsign == 'neg':
        calculatedf = calculatedf[calculatedf[colname] < 0].copy()
    else:
        calculatedf = calculatedf[calculatedf[colname] == 0].copy()
    return calculatedf


# calculate pos_prob of df
def calculatepos_prob(calculatedf, year, chunkC, potydef, potylen):
    if potydef != 'year':
        colname = f'{potylen}-daychunk{chunkC}'
    else:
        colname = 'wholeyear'
    # if result not empty...
    if len(calculatedf) != 0:
        # remove current and future year rows
        calculatedf = calculatedf[calculatedf['YEAR'] < year].copy()
        # if rows still remain...
        if len(calculatedf) != 0:
            # convert predictor samples to boolean (whether they are pos or neg) then get average boolean
            chunkCbools = calculatedf[colname] > 0
            pos_prob = chunkCbools.mean()
        else:
            pos_prob = None
    else:
        pos_prob = None
    return pos_prob


# get and assign prediction value
def getandassignpredictionvalue_singlecell(origwithunknowndf, predictionsdf, analysisdf, lookbackchunks, chunkC, year, potydef, potylen):
    # make copy for calculating probability
    calculatedf = analysisdf.copy()
    # check that none of the lookbackchunks are nan
    lbchunknanstate = checknanvalues(calculatedf, lookbackchunks, chunkC, year, potydef, potylen)
    if lbchunknanstate == 'contains nan':
        pos_prob = None
    else:
        # for each lookbackchunk
        for offsetindex in reversed(range(1, lookbackchunks+1)):
            calculatedf = filterdfbysignpattern(calculatedf, year, chunkC, offsetindex, potydef, potylen)
        # get proportion that predictive samples were positive
        pos_prob = calculatepos_prob(calculatedf, year, chunkC, potydef, potylen)
    # assign value to predictions df
    if potydef != 'year':
        colname = f'{potylen}-daychunk{chunkC}'
    else:
        colname = 'wholeyear'
    predictionsdf.loc[predictionsdf['YEAR'] == year, colname] = pos_prob
    # modify original df only if prediction is unknown
    if pos_prob is None:
        origwithunknowndf.loc[predictionsdf['YEAR'] == year, colname] = pos_prob
    return origwithunknowndf, predictionsdf


# make predictions
def getpredictions(testrunparent, bpotysourcedf, lookbackchunks, maxchunk, potydef, potylen):
    # make copy for analysis use
    analysisdf = bpotysourcedf.copy()
    # make copy for predictions
    predictionsdf = bpotysourcedf.copy()
    # make copy for making original with unknownvalues
    origwithunknowndf = bpotysourcedf.copy()
    # add spillover columns
    for offsetindex in reversed(range(1, lookbackchunks+1)):
        if potydef != 'year':
            phase = math.ceil(offsetindex / (maxchunk - 1)) - 1
            realindex = maxchunk-offsetindex + ((maxchunk - 1) * phase)
            analysisdf[f'{potylen}-daychunk{1-offsetindex}'] = analysisdf[f'{potylen}-daychunk{realindex}'].shift(periods=phase+1)
        else:
            analysisdf[f'year{-offsetindex}'] = analysisdf['wholeyear'].shift(periods=offsetindex)
    # save offset df
    analysisdf.to_csv(index=False, path_or_buf=testrunparent / "offsetdf.csv")
    # for every year
    for year in analysisdf['YEAR']:
        if potydef != 'year':
            # for every timechunk in every year row
            for chunkC in range(1, maxchunk+1):
                origwithunknowndf, predictionsdf = getandassignpredictionvalue_singlecell(origwithunknowndf, predictionsdf, analysisdf, lookbackchunks, chunkC, year, potydef, potylen)
        else:
            chunkC = ''
            origwithunknowndf, predictionsdf = getandassignpredictionvalue_singlecell(origwithunknowndf, predictionsdf, analysisdf, lookbackchunks, chunkC, year, potydef, potylen)
    # save
    origwithunknowndf.to_csv(index=False, path_or_buf=testrunparent / "origwithunknowndf.csv")
    predictionsdf.to_csv(index=False, path_or_buf=testrunparent / "predictions.csv")
    return origwithunknowndf, predictionsdf


# replace Falses with Nan where prediction was unknown
def replacefalsewithunknown(predictionsdf, origwithunknowndf, maxchunk, potydef, potylen):
    for year in predictionsdf['YEAR']:
        for chunkC in range(1, maxchunk+1):
            if potydef != 'year':
                colname = f'{potylen}-daychunk{chunkC}'
            else:
                colname = 'wholeyear'
            cellval = predictionsdf.loc[predictionsdf['YEAR'] == year, colname].item()
            if cellval is None:
                origwithunknowndf.loc[origwithunknowndf['YEAR'] == year, colname] = None
    return origwithunknowndf


# compare predictions to actual to get accuracy score
def getaccuracyscores(testrunparent, lookbackchunks, maxchunk, predictionsdf, origwithunknowndf, potydef, potylen, signaltrigger):
    # get number of unknown predictions
    num_unknowns = predictionsdf.iloc[:, 1:].values.tolist()
    unknownlist = [item for nestedelem in num_unknowns for item in nestedelem if np.isnan(item) == True]
    num_unknowns = len(unknownlist)
    # take orig df and make signal version
    origwithunknowndf.iloc[:, 1:] = origwithunknowndf.iloc[:, 1:].applymap(lambda x: signalcell(x))
    # save
    origwithunknowndf.to_csv(index=False, path_or_buf=testrunparent / "booleanorigdf.csv")
    # convert prediction probabilities to signal form
    predictionsdf.iloc[:, 1:] = predictionsdf.iloc[:, 1:].applymap(lambda x: signalcell_predict(x, signaltrigger))
    # save
    predictionsdf.to_csv(index=False, path_or_buf=testrunparent / "predictionsdfsymbols.csv")
    # get accuracy of predictions
    origwithunknowndf.iloc[:, 1:] = origwithunknowndf.iloc[:, 1:] == predictionsdf.iloc[:, 1:]
    # replace falses with Nones where they are supposed to be
    origwithunknowndf = replacefalsewithunknown(predictionsdf, origwithunknowndf, maxchunk, potydef, potylen)
    # save
    origwithunknowndf.to_csv(index=False, path_or_buf=testrunparent / "accuracydf.csv")
    allscores = origwithunknowndf.iloc[:, 1:].values.tolist()
    # convert nested list to flat list
    allscores = [item for nestedelem in allscores for item in nestedelem]
    # calculate number of correct predictions and number of total predictions
    correctlist = [item for item in allscores if item == 1]
    num_correct = len(correctlist)
    num_total = len(allscores) - num_unknowns
    print(f'Prediction method: predicts whether next time chunk growth will be positive or negative based on previous {lookbackchunks} chunks.')
    print(f'Total samples: {len(allscores)}')
    print(f'Total possible predictions: {num_total}')
    print(f'Total samples not possible to predict (either not enough data or missing data): {num_unknowns}')
    if num_total == 0:
        print('Total correct: Unknown.')
    else:
        print(f'Total correct: {num_correct} ({(num_correct / num_total) * 100} %)')
    # get accuracy by Year
    origwithunknowndf[f'accuracybyyear_LB{lookbackchunks}'] = origwithunknowndf.iloc[:, 1:].mean(axis=1)
    # save
    origwithunknowndf.to_csv(index=False, path_or_buf=testrunparent / "accuracybyear.csv")
    return origwithunknowndf


# strat that predictions future cell based on X previous cells; take samples of all prior years with same pos-neg pattern of X previous cells and returns proportion that was positive
def lookbackpredictions(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # load bpotysource
    if global_params['bpotysource'] != '':
        bpotysourcedf = pd.read_csv(global_params['bpotysource'])
    else:
        bpotydump = buildfolders_singlechild(testrunparent, 'bpotydump')
        bpotysourcedf = get_poty_average(global_params['verbose'], global_params['beg_date'], global_params['end_date'], global_params['potydef'], global_params['potylen'], global_params['ticker'], bpotydump)
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
