"""
Title: WINNER THRESHOLD FINDER BASE
Date Started: Jan 28, 2021
Version: 1.00
Version Start: Jan 28, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Over several trials, finds the metricvalue ranges of winning stocks.

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
#   THIRD PARTY IMPORTS
import numpy as np
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_singlechild, readpkl, buildfolders_regime_testrun, savetopkl
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, PRICES
from timeperiodbot import getrandomexistdate_multiple
from genericfunctionbot import multiprocessorshell
from WINNERTHRESHOLDFINDER_BASE_GETWINNERSLOSERS import getwinners_singletrial
from WINNERTHRESHOLDFINDER_BASE_GETMETRICVALS import getallwinnermetricvals_single


# get winner metric ranges for single trial
def getwinnermetricranges_singletrial(winnerpoolsdir, metricvalsavedir, trialsummdictsavedir, metricscript, rankmeth, rankregime, savemode, chunksize, trial):
    trialno = trial[0]
    exist_date = trial[1]
    # get winners data file
    winnersdict = readpkl(f'winners_trial{trialno}', winnerpoolsdir)
    # create master stat objects
    trialsummary = {'trialno': trialno, 'exist_date': exist_date, 'test_beg': winnersdict['test_beg'], 'test_end': winnersdict['test_end'], 'testlen': winnersdict['testlen']}
    if len(winnersdict['winnerpool']) != 0:
        # parse stage script
        scriptname = metricscript['scriptname']
        scriptparams = metricscript['scriptparams']
        # get df of metric vals for all winners in pool
        metricvaltrialdump = buildfolders_singlechild(metricvalsavedir, f'trialno{trialno}_edate{exist_date}')
        winnermetricvalsdf = getallwinnermetricvals_single(metricvaltrialdump, scriptname, scriptparams, '', exist_date, winnersdict['winnerpool'], rankmeth, rankregime, savemode, chunksize)
        # get list of metricval column names
        metcolnamelist = list(winnermetricvalsdf.columns)[1:]
        # remove stock col
        justvaldf = winnermetricvalsdf[metcolnamelist].copy()
        # store min and max val dfs
        minvaldfdict = justvaldf.min().to_dict()
        maxvaldfdict = justvaldf.max().to_dict()
        for metcol in metcolnamelist:
            for stat_type in ['MIN', 'MAX']:
                if stat_type == 'MIN':
                    sourcedict = minvaldfdict
                elif stat_type == 'MAX':
                    sourcedict = maxvaldfdict
                trialsummary.update({f'{stat_type}_{metcol}': sourcedict[metcol]})
    # save trialsummary
    savetopkl(f'summary_trial{trialno}', trialsummdictsavedir, trialsummary)


# get all winners (to save RAM for loading pricematrices)
def getallwinners_shell(winnerpretestfilterdumpdir, winnerpoolsdir, global_params, alltrialexistdates):
    # load price matrices into RAM
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    # if doesn't contain pretestfilters, use multiprocessor
    if 'addlpretestfilters' in global_params['winnerdefined'].keys():
        for trial in enumerate(alltrialexistdates):
            getwinners_singletrial(winnerpretestfilterdumpdir, winnerpoolsdir, pricematrixdf, benchpricematrixdf, global_params['benchticker'], global_params['testlen'], global_params['winnerdefined'], global_params['loserdefined'], global_params['minimumage'], global_params['rankmeth'], global_params['rankregime'], global_params['savemode'], global_params['chunksize'], trial)
    else:
        # download npdf data
        targetvars = (winnerpretestfilterdumpdir, winnerpoolsdir, pricematrixdf, benchpricematrixdf, global_params['benchticker'], global_params['testlen'], global_params['winnerdefined'], global_params['loserdefined'], global_params['minimumage'], global_params['rankmeth'], global_params['rankregime'], global_params['savemode'], global_params['chunksize'])
        multiprocessorshell(winnerpoolsdir, getwinners_singletrial, alltrialexistdates, 'yes', targetvars, global_params['chunksize'])


# master function
def winnerthreshfinder_master(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    trialsummdictsavedir = buildfolders_singlechild(testrunparent, 'trialsummdictsavedir')
    metricvalsavedir = buildfolders_singlechild(testrunparent, 'metricvalsavedir')

    # get trialexistdates
    if len(global_params['statictrialexistdates']) != 0:
        if len(global_params['statictrialexistdates']) == global_params['num_trials']:
            alltrialexistdates = global_params['statictrialexistdates']
        else:
            print('The static trial exist dates you want to use do not equal the number of trials you want to run.  Exiting...')
            exit()
    else:
        alltrialexistdates = getrandomexistdate_multiple(global_params['num_trials'], global_params['firstdate'], global_params['latestdate'], global_params['testlen'], daterangedb_source)
        # save dates
        savetopkl('trialdatedata', testrunparent, alltrialexistdates)
    # get winners for each trial
    if len(global_params['statictrialexistdates']) != 0:
        winnerpoolsdir = global_params['statictrialbaseloc'] / 'winnerpoolsdir'
    else:
        winnerpoolsdir = buildfolders_singlechild(testrunparent, 'winnerpoolsdir')
        winnerpretestfilterdumpdir = buildfolders_singlechild(testrunparent, 'winnerpretestfilterdumpdir')
        getallwinners_shell(winnerpretestfilterdumpdir, winnerpoolsdir, global_params, alltrialexistdates)
    # get min max metricvals of all trials
    for trial in enumerate(alltrialexistdates):
        getwinnermetricranges_singletrial(winnerpoolsdir, metricvalsavedir, trialsummdictsavedir, global_params['metricscript'], global_params['rankmeth'], global_params['rankregime'], global_params['savemode'], global_params['chunksize'], trial)
    # construct mastertrialdf
    table_results = []
    for child in trialsummdictsavedir.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    overallstatsdf = pd.DataFrame(data=table_results)
    # save df
    overallstatsdf.to_csv(index=False, path_or_buf=testrunparent / "overallstats_alltrialsummaries.csv")
    # get stats
    nonmetricolnames = ['trialno', 'exist_date', 'test_beg', 'test_end', 'testlen']
    metricolnames = [item for item in list(overallstatsdf.columns) if item not in nonmetricolnames]
    masteroverallstatdata = []
    currcatname = ''
    statdict = {}
    for category in metricolnames:
        # create finalcategory name
        newcatname = category[4:]
        prefix = category[:3]
        # if new category, append old statdict and wipe statdict clean
        if newcatname != currcatname:
            if len(statdict) != 0:
                masteroverallstatdata.append(statdict)
            currcatname = newcatname
            statdict = {'category': currcatname}
        # for each prefix
        if prefix == 'MIN':
            alltrialval = np.min(overallstatsdf[category].dropna().to_numpy())
        elif prefix == 'MAX':
            alltrialval = np.max(overallstatsdf[category].dropna().to_numpy())
        # update statdict
        statdict.update({f'{prefix}ofalltrials': alltrialval})
        # if category is last then append to list
        if category == metricolnames[-1]:
            masteroverallstatdata.append(statdict)
    # save final df
    masteroverallstats = pd.DataFrame(data=masteroverallstatdata)
    masteroverallstats.to_csv(index=False, path_or_buf=testrunparent / "masteroverallstats.csv")
