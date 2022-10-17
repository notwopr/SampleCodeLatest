"""
Title: STRATTEST MULTITRIAL BASE
Date Started: July 10, 2020
Version: 3.00
Version Start: Dec 31, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given an existence date, runs pool thru first pass screening, runs again through given screening method, and returns percentage of resulting pool that beat market during the test period.
VERSIONS:
1.01: Optimize with updated functions.  Allow for more modulatory.
2: modify leaderboard metrics
Growth Rate
    Meanperf
    Medianperf
    avgperf
Reliability
    Meanperf_std
    Medianperf_std
    Avgperf_std
    Meanperf_mad
    Medianperf_mad
    Avgperf_mad
Turmoil
    Prevalence of dips
    Magnitude of dips
    Maxdip is low
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
from functools import partial
from multiprocessing import Pool
from pathlib import Path
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filetests import checknum
from filelocations import buildfolders_singlechild, readpkl, buildfolders_regime_testrun, savetopkl
from tickerportalbot import tickerportal3
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, tickerlistcommon_source
from statresearchbot import stat_profilerv2
from STRATTEST_SINGLE_BASE import getstratpool, getperfstats
from computersettings import computerobject
from STRATTEST_MULTITRIAL_BASE_TRIALRUNSET import gettrialiterables


# set preconfigured trial samples
def setpreconfigsamples(global_params):
    # configure fixed sample data
    # if source contains both dates and starting pools use "singlesource"
    if global_params['preconfigsamps'] == 'singlesource':
        staticdatesandpools = global_params['existingset']
        preconfigsamples = {
            'staticdatesandpools': staticdatesandpools
            }
    else:
        # if just dates then use 'justdates'; if want dates and pools but using old method of calling 'datesandpools'
        staticdatesource = r'D:\BOT_DUMP\multitrials\D20201010T3\mktbeatpoolpctalltrialmasterdf_2018methodversions.csv'
        stocklistdf = pd.read_csv(staticdatesource)
        statictrialexistdates = stocklistdf['existdate'].to_list()
        if global_params['preconfigsamps'] == 'justdates':
            preconfigsamples = {
                'statictrialexistdates': statictrialexistdates}
        elif global_params['preconfigsamps'] == 'datesandpools':
            preconfigsamples = {
                'statictrialexistdates': statictrialexistdates,
                'subtrialfolderpath': r'\Stage 1_dump\resultfiles',
                'testrunparentpath': r'D:\BOT_DUMP\multitrials\D20201010T3',
                'basepoolfntemplate': 'SCREENER_firstpass_finalists_as_of_'
                }
        else:
            preconfigsamples = ''
    return preconfigsamples


# GIVEN LIST OF FILTERS, EXISTENCE DATE, RETURNS RESULTING POOL AND MKTBEATPCT IF REQUESTED
def getperfstats_single(trialparent, finalpoolsetdump, trialno, exist_date, strat_panel, startpool, verbose, trimsize, createfinalpoolset, testlen, benchticker, rankmeth, rankregime, savemode, chunksize):
    if len(startpool) == 0:
        print('Basepool contained no stocks.')
        perfstatdict = {}
    else:
        # GET FINAL STRAT POOL
        finalstratpool = getstratpool(verbose, trialparent, exist_date, strat_panel, startpool, rankmeth, rankregime, savemode, chunksize)
        # SAVE FINAL POOL IF FINAL POOL RUN SET REQUESTED
        if createfinalpoolset == 'yes':
            finalpooldata = {
                'trialno': trialno,
                'existdate': exist_date,
                'startpool': finalstratpool
            }
            # save to file
            savetopkl(f'finalpool_trial{trialno}', finalpoolsetdump, finalpooldata)
        # GET TEST PERIOD PERFORMANCE STATS OF FINAL STRAT POOL
        if len(finalstratpool) != 0:
            if trimsize != '':
                finalstratpool = finalstratpool[:trimsize]
            perfstatdict = getperfstats(verbose, exist_date, testlen, finalstratpool, benchticker)
        else:
            perfstatdict = {}
    return perfstatdict


# get perfstatdict and save
def getperfstatdictandsave(trialdumpparent, trialresultparent, finalpoolsetdump, trialno, existdate, global_params, strat_panel, startpool):
    # get mktbeatsummary for that existence date
    trialsumm = {'trialno': trialno, 'existdate': existdate}
    # build folders for trial
    trialparent = buildfolders_singlechild(trialdumpparent, f'trialno{trialno}_edate{existdate}')
    # get strat_panel perf summary
    perfstatdict = getperfstats_single(trialparent, finalpoolsetdump, trialno, existdate, strat_panel, startpool, global_params['verbose'], global_params['trimsize'], global_params['createfinalpoolset'], global_params['testlen'], global_params['benchticker'], global_params['rankmeth'], global_params['rankregime'], global_params['savemode'], global_params['chunksize'])
    trialsumm.update(perfstatdict)
    # save to file
    savetopkl(f'perfstatdict_{existdate}', trialresultparent, trialsumm)
    return trialsumm


# run single trial of stratpanel - basepoolsinglefilesource version
def runstratpanel_singletrial_singlesource(trialdumpparent, trialresultparent, finalpoolsetdump, global_params, strat_panel, trial):
    trialno = trial['trialno']
    existdate = trial['existdate']
    startpool = trial['startpool']
    trialsumm = getperfstatdictandsave(trialdumpparent, trialresultparent, finalpoolsetdump, trialno, existdate, global_params, strat_panel, startpool)
    return trialsumm


# run single trial of stratpanel; justdates or datesandpool (old) preset trialiterables
def runstratpanel_singletrial_preset(trialdumpparent, trialresultparent, global_params, strat_panel, preconfigsamples, trial):
    trialno = trial[0]
    existdate = trial[1]
    # get startpool
    if global_params['preconfigsamps'] == 'datesandpools':
        trialfolder = f'\\trialno{trialno}_edate{existdate}'
        trialpath = trialfolder + preconfigsamples['subtrialfolderpath']
        fullbasepoolpath = preconfigsamples['testrunparentpath'] + trialpath
        basepoolfilename = preconfigsamples['basepoolfntemplate'] + existdate
        basepooldf = readpkl(basepoolfilename, Path(fullbasepoolpath))
        startpool = basepooldf['stock'].tolist()
    elif global_params['preconfigsamps'] == 'justdates':
        startpool = tickerportal3(existdate, 'common', 2)
    trialsumm = getperfstatdictandsave(trialdumpparent, trialresultparent, trialno, existdate, global_params, strat_panel, startpool)
    return trialsumm


# run single trial of stratpanel: no preset trial iterables
def runstratpanel_singletrial(trialdumpparent, trialresultparent, global_params, strat_panel, trial):
    trialno = trial[0]
    existdate = trial[1]
    # get startpool
    startpool = tickerportal3(existdate, 'common', 2)
    trialsumm = getperfstatdictandsave(trialdumpparent, trialresultparent, trialno, existdate, global_params, strat_panel, startpool)
    return trialsumm


# create final pool trial run set if requested
def createfinalpooltrialrunset(global_params, strat_panel, savedir, sourcedump):
    # assemble results
    finalpooltrialrunset = []
    for child in sourcedump.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        finalpooltrialrunset.append(unpickled_raw)
    # save trialrunset
    mod_date = global_params['todaysdate'].replace("-", "")
    testcode = 'D' + mod_date + 'T' + str(global_params['testnumber'])
    # get stagefilters used
    stagefiltername = ''
    for keyname in strat_panel.keys():
        # get scriptname for each stage
        if keyname.startswith('Stage 1') or keyname.startswith('Stage 2'):
            stagefiltername += strat_panel[keyname]['scriptname']
    savetopkl(f'{testcode}_{stagefiltername}_finalpooltrialrunset', savedir, finalpooltrialrunset)


def strattest_multitrial(rootdir, global_params, preconfigsamples, strat_panel):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # build stage folders
    trialdumpparent = buildfolders_singlechild(testrunparent, 'trialdumpparent')
    trialresultparent = buildfolders_singlechild(testrunparent, 'trialresultparent')
    # if requested build dump folder for finalpoolset
    if global_params['createfinalpoolset'] == 'yes':
        finalpoolsetdump = buildfolders_singlechild(testrunparent, 'finalpooltrialrunsetdump')
    else:
        finalpoolsetdump = ''
    # define dates, iterables, iterfunc, noniterparams, filecheck count
    if global_params['preconfigsamps'] == 'singlesource':
        iterables = preconfigsamples['staticdatesandpools']
        iterfunc = runstratpanel_singletrial_singlesource
        noniterparams = (trialdumpparent, trialresultparent, finalpoolsetdump, global_params, strat_panel)
        correct = len(iterables)
    else:
        if global_params['preconfigsamps'] == 'justdates' or global_params['preconfigsamps'] == 'datesandpools':
            alltrialexistdates = preconfigsamples['statictrialexistdates']
            if len(alltrialexistdates) != global_params['num_trials']:
                print('The static trial exist dates you want to use do not equal the number of trials you want to run.  Exiting...')
                exit()
            iterfunc = runstratpanel_singletrial_preset
            noniterparams = (trialdumpparent, trialresultparent, global_params, strat_panel, preconfigsamples)
            iterables = enumerate(alltrialexistdates)
            correct = len(alltrialexistdates)
        else:
            # get date-pool-benchgain iterables
            iterables = gettrialiterables(testrunparent, global_params)
            iterfunc = runstratpanel_singletrial_singlesource
            noniterparams = (trialdumpparent, trialresultparent, finalpoolsetdump, global_params, strat_panel)
            correct = len(iterables)

    # for each trialdate get trial performance summary
    alltrialresults = []
    if global_params['usemultiprocessor'] == 'yes':
        # run multiprocessor on stratpanel
        fn = partial(iterfunc, *noniterparams)
        pool = Pool(processes=computerobject.use_cores)
        pool.map(fn, iterables, 1)
        pool.close()
        pool.join()
        # wait for all files to download
        downloadfinish = checknum(trialresultparent, correct, '')
        while downloadfinish is False:
            downloadfinish = checknum(trialresultparent, correct, '')
        # construct metricsdf
        for child in trialresultparent.iterdir():
            with open(child, "rb") as targetfile:
                unpickled_raw = pkl.load(targetfile)
            alltrialresults.append(unpickled_raw)
    else:
        for trial in iterables:
            trialsumm = iterfunc(*noniterparams, trial)
            alltrialresults.append(trialsumm)
    # FINAL CREATING FINALPOOL TRIAL RUN SET IF REQUESTED
    if global_params['createfinalpoolset'] == 'yes':
        createfinalpooltrialrunset(global_params, strat_panel, testrunparent, finalpoolsetdump)
    # CREATE MASTERDF
    masterdf = pd.DataFrame(data=alltrialresults)
    # ARCHIVE MASTERDF
    mdfn = f"alltrialperfstatmasterdf_{global_params['metricsetname']}"
    if global_params['savemode'] == 'pkl':
        savetopkl(mdfn, testrunparent, masterdf)
    elif global_params['savemode'] == 'csv':
        masterdf.to_csv(index=False, path_or_buf=testrunparent / f"{mdfn}.csv")
    # get stat summary
    statcols = [
        'mktbeatpoolpct',
        'mktfailpoolpct',
        'poolsize',
        'mktbeatsize',
        'fsize',
        'benchperf',
        'benchdipprev',
        'benchdipmag',
        'benchdipscore',
        'benchdipmax'
        ]
    for pooltype in ['pool', 'mktbeat', 'mktfail']:
        statcols += [
            f'{pooltype}perf_mean',
            f'{pooltype}perf_median',
            f'{pooltype}perf_mean_margin',
            f'{pooltype}perf_median_margin',
            f'{pooltype}dipprev_mean',
            f'{pooltype}dipprev_median',
            f'{pooltype}dipmag_mean',
            f'{pooltype}dipmag_median',
            f'{pooltype}dipscore_mean',
            f'{pooltype}dipscore_median',
            f'{pooltype}dipmax_mean',
            f'{pooltype}dipmax_median'
        ]
    allstatdicts = []
    for statcol in statcols:
        datarr = masterdf[statcol].dropna().to_numpy()
        if len(datarr) >= 2:
            statdict = stat_profilerv2(datarr)
        else:
            statdict = {}
        statdict.update({'category': statcol})
        allstatdicts.append(statdict)
    # CREATE STATDF
    statdf = pd.DataFrame(data=allstatdicts)
    # save results
    statsfn = f"mktbeatpoolpctalltrialstats_metricset_{global_params['metricsetname']}"
    if global_params['savemode'] == 'pkl':
        savetopkl(statsfn, testrunparent, statdf)
    elif global_params['savemode'] == 'csv':
        statdf.to_csv(index=False, path_or_buf=testrunparent / f"{statsfn}.csv")
    return statdf
