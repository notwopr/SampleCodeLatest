"""
Title: Best Streaks Base - Current to Next - Multitrials
Date Started: Oct 13, 2020
Version: 1.0
Version Start Date: Oct 13, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Multitrial base functions for the Current to Next Best Streaks Bot.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from BESTSTREAK_BASE_CURRNEXT import curr_to_next
from filelocations import buildfolders_regime_testrun, buildfolders_singlechild, savetopkl
from timeperiodbot import getrandomexistdate_multiple
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source
from statresearchbot import stat_profiler


# returns set of trial dates
def trialdates(num_trials, firstdate, latestdate, currperiodlen, nextperiodlen):

    # get
    alltrialexistdates = getrandomexistdate_multiple(num_trials, firstdate, latestdate, currperiodlen+nextperiodlen, daterangedb_source)
    alltrialdatedicts = []
    for trialdate in alltrialexistdates:
        trialdatedict = {
            'currbeg': trialdate,
            'currend': str(dt.date.fromisoformat(trialdate) + dt.timedelta(days=currperiodlen)),
            'nextbeg': str(dt.date.fromisoformat(trialdate) + dt.timedelta(days=currperiodlen)),
            'nextend': str(dt.date.fromisoformat(trialdate) + dt.timedelta(days=currperiodlen+nextperiodlen))
        }
        alltrialdatedicts.append(trialdatedict)
    return alltrialdatedicts


# get results of multiple trials on beststreakbot
def beststreak_multitrials(verbose, rootdir, globalsettingsdict, trialsettings_dict, sourcefolder):
    # BUILD FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, globalsettingsdict['testnumber'], globalsettingsdict['todaysdate'], globalsettingsdict['testregimename'])
    # get set of trial dates
    alltrialdatedicts = trialdates(globalsettingsdict['num_trials'], globalsettingsdict['firstdate'], globalsettingsdict['latestdate'], globalsettingsdict['currentphase'], globalsettingsdict['nextphase'])
    # create trial parent folder
    trialsparent = buildfolders_singlechild(testrunparent, 'trialsdata_dump')
    # create result parent folder
    resultparent = buildfolders_singlechild(testrunparent, 'trialresults_dump')
    # for each trial
    for trial in enumerate(alltrialdatedicts):
        trialfolder = buildfolders_singlechild(trialsparent, f'trial{trial[0]}_dump')
        # create streakparam_dict
        streakparam_dict = {}
        streakparam_dict.update(trial[1])
        streakparam_dict.update(trialsettings_dict)
        streakparam_dict.update({'trialno': trial[0]})
        # get curr to next proportion
        curr_to_next(verbose, trialfolder, resultparent, streakparam_dict)

    # assemble all results together
    table_results = []
    for child in resultparent.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    alltrialresultsdf = pd.DataFrame(data=table_results)
    # archive trial resultsdf
    alltrialresultsdf.to_csv(index=False, path_or_buf=testrunparent / "alltrialresultsdf.csv")
    # run stat analysis on prop_pct
    allprop_pct = alltrialresultsdf['prop_pct'].tolist()
    propstats = stat_profiler(allprop_pct)
    # create leaderboard summary
    testrunresultsdict = {}
    testrunresultsdict.update(globalsettingsdict)
    testrunresultsdict.update(trialsettings_dict)
    testrunresultsdict.update(propstats)
    # add corrected latestdate to summary
    with open(daterangedb_source, "rb") as targetfile:
        daterangedb = pkl.load(targetfile)
    lastdate_dateobj = daterangedb['last_date'].apply(lambda x: dt.date.fromisoformat(x))
    lastdates = lastdate_dateobj.tolist()
    latestdate = str(np.max(lastdates))
    testrunresultsdict.update({'latestdate': latestdate})
    # save to file
    timestamp = str(dt.datetime.now())
    timestamp = timestamp.replace(".", "_")
    timestamp = timestamp.replace(":", "")
    timestamp = timestamp.replace(" ", "_")
    savetopkl(f'testrunresults_{timestamp}', sourcefolder, testrunresultsdict)
    savetopkl('testrunresults', testrunparent, testrunresultsdict)
    # report results
    for i in testrunresultsdict:
        print(f'{i}: {testrunresultsdict[i]}')


# create new beststreakbotmultitrial leaderboard
def leaderboard_beststreakbot(sourcefolder, destfolder):
    # assemble all results together
    table_results = []
    for child in sourcefolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    leaderdf = pd.DataFrame(data=table_results)
    # correct order of columns
    reordercols = [
        'todaysdate',
        'testnumber',
        'testregimename',
        'currperiodlen',
        'nextperiodlen',
        'currentphase',
        'nextphase',
        'num_trials',
        'latestdate',
        'firstdate',
        'currbenchticker',
        'nextbenchticker',
        'curravg_type',
        'nextavg_type',
        'curr_rankbeg',
        'curr_rankend',
        'next_rankbeg',
        'next_rankend',
        'stat_min',
        'stat_q1',
        'stat_mean',
        'stat_med',
        'stat_q3',
        'stat_max',
        'stat_std',
        'stat_sharpe'
        ]
    leaderdf = leaderdf[reordercols]

    # save leaderboard
    timestamp = str(dt.datetime.now())
    timestamp = timestamp.replace(".", "_")
    timestamp = timestamp.replace(":", "")
    timestamp = timestamp.replace(" ", "_")
    lbfn = f'beststreakbotleaderboard_{timestamp}'
    leaderdf.to_csv(index=False, path_or_buf=destfolder / f"{lbfn}.csv")
