"""
Title: STRATTEST MULTITRIAL BASE LEADERBOARD FUNCTIONS
Date Started: Oct 20, 2020
Version: 3.00
Version Start: Jan 8, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Functions that record leaderboard stats and create leaderboard.
VERSIONS:
2: Revise metrics to pull.
3: Consolidate metric categories.
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
import datetime as dt
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from filelocations import savetopkl
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source


# getstattitle given statkey
def getstattitle(stattype):
    if stattype == 'stat_mean':
        title = 'MEAN'
    elif stattype == 'stat_med':
        title = 'MEDIAN'
    elif stattype == 'stat_min':
        title = 'MIN'
    elif stattype == 'stat_max':
        title = 'MAX'
    elif stattype == 'stat_std':
        title = 'STD'
    elif stattype == 'stat_mad':
        title = 'MAD'
    return title


# record leaderboard dict line for later assembly into leaderboard
def leaderboardsummary(sourcefolder, global_params, strat_panel, statdf):
    # add global_param features
    summarydict = {
        'stratfamily': global_params['metricsetname'],
        'testdate': global_params['todaysdate'],
        'num_trials': global_params['num_trials'],
        'testlen': global_params['testlen'],
        'benchticker': global_params['benchticker'],
        'firstdate': global_params['firstdate'],
        'latestdate': global_params['latestdate']
    }
    # add rankmeth
    if global_params['metricsetname'].startswith('winrateranker'):
        summarydict.update({'rankmeth': strat_panel['Stage 3']['scriptparams'][0]['rankmeth']})
    else:
        summarydict.update({'rankmeth': global_params['rankmeth']})
    # add corrected latestdate to summary
    with open(daterangedb_source, "rb") as targetfile:
        daterangedb = pkl.load(targetfile)
    lastdate_dateobj = daterangedb['last_date'].apply(lambda x: dt.date.fromisoformat(x))
    lastdates = lastdate_dateobj.tolist()
    latestdate = str(np.max(lastdates))
    summarydict.update({'latestdate': latestdate})
    # add strat_panel features
    for key, val in strat_panel.items():
        if key != 'multistageweightmode':
            stagenum = key
            scriptname = val['scriptname']
            summarydict.update({stagenum: scriptname})
    # add misc stats
    for category in [
        'mktbeatpoolpct',
        'poolsize',
        'mktbeatsize',
        'benchperf',
    ]:
        # set type of stats to gather for the category
        if category in ['mktbeatpoolpct', 'poolsize', 'mktbeatsize']:
            if category in ['mktbeatpoolpct']:
                allstattypes = ['AVG', 'DEV']
            else:
                allstattypes = ['AVG']
        elif category in ['benchperf']:
            allstattypes = ['stat_min', 'AVG', 'stat_max']
        # retrieve stats
        for stattype in allstattypes:
            if stattype == 'AVG' or stattype == 'DEV':
                if stattype == 'AVG':
                    stat1 = 'stat_mean'
                    stat2 = 'stat_med'
                elif stattype == 'DEV':
                    stat1 = 'stat_std'
                    stat2 = 'stat_mad'
                val1 = statdf[statdf['category'] == category][stat1].item()
                val2 = statdf[statdf['category'] == category][stat2].item()
                statval = np.mean([val1, val2])
                summarydict.update({f'{stattype}_{category}': statval})
            else:
                title = getstattitle(stattype)
                summarydict.update({f'{title}_{category}': statdf[statdf['category'] == category][stattype].item()})
    # add main stats
    for pooltype in ['pool', 'mktbeat', 'mktfail']:
        # set category list
        if pooltype == 'pool':
            categorylist = [
                'perf',
                'perf_margin',
                'dipscore'
            ]
        elif pooltype == 'mktbeat':
            categorylist = [
                'perf',
                'perf_margin',
                'dipscore'
            ]
        elif pooltype == 'mktfail':
            categorylist = [
                'perf',
                'dipscore'
            ]
        for category in categorylist:
            # set stattypes
            if pooltype == 'pool':
                if category == 'perf':
                    allstattypes = ['MIN', 'AVG', 'MAX', 'DEV']
                elif category == 'perf_margin':
                    allstattypes = ['AVG']
                elif category == 'dipscore':
                    allstattypes = ['ratiodip']
            elif pooltype == 'mktbeat':
                if category == 'dipscore':
                    allstattypes = ['ratiodip']
                else:
                    allstattypes = ['AVG']
            elif pooltype == 'mktfail':
                if category == 'dipscore':
                    allstattypes = ['ratiodip']
                else:
                    allstattypes = ['AVG']
            # retrieve stats
            for stattype in allstattypes:
                if stattype == 'MIN' or stattype == 'MAX':
                    val1 = statdf[statdf['category'] == f'{pooltype}{category}_mean'][f'stat_{stattype.lower()}'].item()
                    val2 = statdf[statdf['category'] == f'{pooltype}{category}_median'][f'stat_{stattype.lower()}'].item()
                    meanval = np.mean([val1, val2])
                    summarydict.update({f'{stattype}_{pooltype}{category}': meanval})
                elif stattype == 'AVG' or stattype == 'DEV' or stattype == 'ratiodip':
                    if stattype == 'AVG' or stattype == 'ratiodip':
                        stat1 = 'stat_mean'
                        stat2 = 'stat_med'
                    elif stattype == 'DEV':
                        stat1 = 'stat_std'
                        stat2 = 'stat_mad'
                    if category == 'perf_margin':
                        cat1 = f'{pooltype}perf_mean_margin'
                        cat2 = f'{pooltype}perf_median_margin'
                    else:
                        cat1 = f'{pooltype}{category}_mean'
                        cat2 = f'{pooltype}{category}_median'
                    val1 = statdf[statdf['category'] == cat1][stat1].item()
                    val2 = statdf[statdf['category'] == cat1][stat2].item()
                    val3 = statdf[statdf['category'] == cat2][stat1].item()
                    val4 = statdf[statdf['category'] == cat2][stat2].item()
                    meanval = np.mean([val1, val2, val3, val4])
                    if stattype == 'ratiodip':
                        meanbenchdipscore = statdf[statdf['category'] == 'benchdipscore']['stat_mean'].item()
                        medianbenchdipscore = statdf[statdf['category'] == 'benchdipscore']['stat_med'].item()
                        denominator = np.mean([meanbenchdipscore, medianbenchdipscore])
                        summarydict.update({f'AVG_{pooltype}{category}/AVG_benchdipscore': meanval / denominator})

                    else:
                        summarydict.update({f'{stattype}_{pooltype}{category}': meanval})
                else:
                    title = getstattitle(stattype)
                    summarydict.update({
                        f'{title}_{category}': statdf[statdf['category'] == category][stattype].item()
                        })
    # save to file
    timestamp = str(dt.datetime.now())
    timestamp = timestamp.replace(".", "_")
    timestamp = timestamp.replace(":", "")
    timestamp = timestamp.replace(" ", "_")
    summfn = f'testsummary_{global_params["metricsetname"]}_{timestamp}'
    savetopkl(summfn, sourcefolder, summarydict)


# create new strattest leaderboard
def create_strattest_leaderboard(sourcefolder, destfolder):
    # assemble all results together
    table_results = []
    for child in sourcefolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    leaderdf = pd.DataFrame(data=table_results)
    # correct order of columns
    allcols = list(leaderdf.columns)
    reordercols = [
        'stratfamily',
        'testdate',
        'num_trials',
        'testlen',
        'benchticker',
        'firstdate',
        'latestdate',
        'Stage 1',
        'Stage 2 Part I',
        'Stage 2 Part II',
        'Stage 3',
        'AVG_poolsize',
        'AVG_mktbeatsize',
        'AVG_mktbeatpoolpct',
        'DEV_mktbeatpoolpct',
        'AVG_pooldipscore/AVG_benchdipscore',
        'AVG_mktbeatdipscore/AVG_benchdipscore',
        'AVG_mktfaildipscore/AVG_benchdipscore',
        'MIN_benchperf',
        'AVG_benchperf',
        'MAX_benchperf',
        'MIN_poolperf',
        'AVG_poolperf',
        'MAX_poolperf',
        'DEV_poolperf',
        'AVG_mktbeatperf',
        'AVG_mktfailperf',
        'AVG_poolperf_margin',
        'AVG_mktbeatperf_margin'
    ]
    remaindercols = [item for item in allcols if item not in reordercols]
    reordercols = reordercols + remaindercols
    leaderdf = leaderdf[reordercols]
    # save leaderboard
    timestamp = str(dt.datetime.now())
    timestamp = timestamp.replace(".", "_")
    timestamp = timestamp.replace(":", "")
    timestamp = timestamp.replace(" ", "_")
    lbfn = f'strattestleaderboard_{timestamp}'
    leaderdf.to_csv(index=False, path_or_buf=destfolder / f"{lbfn}.csv")
