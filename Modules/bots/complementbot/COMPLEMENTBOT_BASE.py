"""
Title: Complement Bot - Base
Date Started: Apr 20, 2020
Version: 2
Version Start: Oct 30, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Complement score is a measure of how well two stocks go together, i.e. if one stock goes down, the other goes up, but if one goes up, the other goes up as well.

Versions:
1.01: Add reverse complemtally. Both how X complements Y and Y complements X, and average the two.
2: Two stocks are complementary if
-the proportion of times they deviate from each other is
-the proportion where they both fall on the same day is low.
-the proportion where they both rise on the same day is high.
There will be days when they go down.  So, then the question is are they on the same day?
If their lives are populated by instances where they rise together, that's great but the bigger concern is what happens on falling days.  We should not be concerned with the proportion of their common lives are rising days because the complement bot is a last stage research tool, and by then we would have already found our pool of great performing stocks which would have already accounted for their growth quality.  Complement bot has to be concerned with just the falling days.  So, the question becomes, of those days when either stock is falling, what proportion of those days are instances where they are both falling?
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
from itertools import combinations
import pickle as pkl
import os
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from filelocations import savetopkl, create_nonexistent_folder, readpkl_fullpath
from filetests import count_file, checknum_multilevel
from computersettings import computerobject
from UPDATEPRICEDATA_MASTERSCRIPT import tickerlistcommon_source, tickerlistall_source
from genericfunctionbot import multiprocessorshell


preamble = "There will be days when a stock falls.  The complement bot is designed to measure how well two stocks offset the falling days of the other.  Specifically, on the days where one of them falls, what is the other stock doing?  Is it also falling or staying flat or rising?  In other words, out of all the days where one of the two stocks is falling, what is the proportion of those days where the other one is also falling?  The lower this proportion, the better these two stocks complement one another or offset each other's down days."


# CALCULATES COMPLEMENT SCORE OF A PAIR OF TICKERS
def complement_pair(destfolder, existdate, target, candidate, verbose, savemode):

    # GET PRICE HISTORIES OF EACH
    s1hist = grabsinglehistory(target)
    s2hist = grabsinglehistory(candidate)

    # GET AGE
    age1 = len(s1hist) - 1
    age2 = len(s2hist) - 1

    # COMBINE PRICE HISTORIES TOGETHER
    mdf = s1hist.join(s2hist.set_index("date"), how="inner", on="date")

    # SLICE OUT DATES IF REQUESTED
    if existdate != '':
        mdf = mdf[mdf['date'] <= dt.date.fromisoformat(existdate)]

    # RE-INDEX
    mdf.reset_index(drop=True, inplace=True)

    # DAILY RETURNS
    mdf[[target, candidate]] = mdf[[target, candidate]].pct_change(periods=1, fill_method="ffill")

    # REMOVE NAN ROW
    mdf = mdf.loc[1:]
    mdf['At least one falling'] = (mdf[target] < 0) | (mdf[candidate] < 0)
    mdf['Both falling'] = (mdf[target] < 0) & (mdf[candidate] < 0)

    # SAVE TO FILE
    if savemode == "yes":
        mdf.to_csv(index=False, path_or_buf=destfolder / f"{target}and{candidate}.csv")
    return mdf, age1, age2


def targetcandidateanalysis_single(verbose, signature, summary, tcdf, targetage, candidateage, target, candidate):
    # ANALYSIS
    num_commondays = len(tcdf)
    num_comparisons = num_commondays-1
    num_atleastonefalling = tcdf['At least one falling'].sum()
    num_atleastonefalling_pct = num_atleastonefalling / num_comparisons
    num_bothfalling = tcdf['Both falling'].sum()
    num_bothfalling_pct = num_bothfalling / num_comparisons
    badpairingrate = num_bothfalling / num_atleastonefalling
    complementscore = 1-badpairingrate

    # SAVE STATS
    summary.update({
        f'target ({signature})': target,
        f'candidate ({signature})': candidate,
        f'targetage ({signature})': targetage,
        f'candidateage ({signature})': candidateage,
        f'num_comparisons ({signature})': num_comparisons,
        f'num_atleastonefalling ({signature})': num_atleastonefalling,
        f'num_atleastonefalling_pct ({signature})': num_atleastonefalling_pct,
        f'num_bothfalling ({signature})': num_bothfalling,
        f'badpairingrate ({signature})': badpairingrate,
        f'complementscore ({signature})': complementscore
        })

    # REPORT FINDINGS
    if verbose == 'yes':
        print(preamble)
        # TARGET CANDIDATE ANALYSIS
        print(f"{target} age: {targetage} | {candidate} age: {candidateage}")
        print(f'They share {num_commondays} days in common (since we are comparing daily price movement, the number of comparisons we are making is one less than that, or {num_comparisons})')
        print(f'Of the {num_comparisons} comparisons made, the number of days where at least one of the them was falling is {num_atleastonefalling} ({num_atleastonefalling_pct * 100}) %.')
        print(f'The number of days where both were falling is {num_bothfalling} ({num_bothfalling_pct * 100}) %.')
        print(f'Therefore, out of all the days where at least one of them was falling, both of them were falling {badpairingrate * 100} % of the time.')
        print(f'In conclusion, {candidate} receives a complement score of {complementscore * 100} % in being a complement to target {target}.')
        print('\n')
    return summary


def fullcomplementanalysis_single(summaryfolder, dfdumpfolder, existdate, verbose, target, benchmark, savemode, candidate):
    summary = {}

    # GET TARGET AND CANDIDATE ANALYSIS
    tcdf, targetage, candidateage = complement_pair(dfdumpfolder, existdate, target, candidate, verbose, savemode)
    signature = 'target_candidate'  # ESTABLISH SIGNATURE SO NO OVERWRITING OF DICT KEY VAL PAIRS
    summary = targetcandidateanalysis_single(verbose, signature, summary, tcdf, targetage, candidateage, target, candidate)
    if benchmark in ["^DJI", "^IXIC", "^INX"]:
        # GET BENCHMARK / TARGET ANALYSIS
        signature = 'benchmark_target'
        btdf, benchage, targetage = complement_pair(dfdumpfolder, existdate, benchmark, target, verbose, savemode)
        summary = targetcandidateanalysis_single(verbose, signature, summary, btdf, benchage, targetage, benchmark, target)
        # GET BENCHMARK / CANDIDATE ANALYSIS
        signature = 'benchmark_candidate'
        bcdf, benchage, candidateage = complement_pair(dfdumpfolder, existdate, benchmark, candidate, verbose, savemode)
        summary = targetcandidateanalysis_single(verbose, signature, summary, bcdf, benchage, candidateage, benchmark, candidate)
    # SAVE SUMMARY
    summfn = f'complementsummary_{target}_{candidate}_{benchmark}'
    savetopkl(summfn, summaryfolder, summary)


# RANKS ALL CANDIDATES AGAINST TARGET STOCK AND BENCHMARK
def complement_ranker(resultfolder, summaryfolder, dfdumpfolder, existdate, pool, target, rankweights, benchmark, verbose, savemode, chunksize):

    # REMOVE TARGET FROM CANDIDATE POOL TO AVOID ERROR
    pool = [item for item in pool if item != target]

    # RUN MULTIPROCESSOR
    multiprocessorshell(summaryfolder, fullcomplementanalysis_single, pool, '', (summaryfolder, dfdumpfolder, existdate, verbose, target, benchmark, savemode), chunksize)

    # ASSEMBLE DATA
    table_results = [readpkl_fullpath(child) for child in summaryfolder.iterdir()]
    complementdf = pd.DataFrame(data=table_results)

    # GET RANKINGS FOR NUM_COMPARISONS, NUM_ATLEASTONEFALLING_PCT, AND COMPLEMENTSCORE
    # RANK DATA
    sumcols = []
    weight_total = 0
    # FOR EACH COLUMN TO BE RANKED
    for metcolname, metricweight in rankweights.items():
        # SET NAME FOR RANK COLUMN
        rankcolname = f'RANK_{metcolname} (w={metricweight})'
        # SET RANK COLUMN RANK DIRECTION
        if metcolname in ['num_comparisons (target_candidate)', 'complementscore (target_candidate)']:
            rankdirection = 0
        else:
            rankdirection = 1
        # CREATE RANK COLUMN
        complementdf[rankcolname] = complementdf[metcolname].rank(ascending=rankdirection)
        # GET RANK COLUMN'S WEIGHTED RANK VALUE
        wrankcolname = f'w_{rankcolname}'
        complementdf[wrankcolname] = (complementdf[rankcolname] * metricweight)
        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wrankcolname)
        # ADD WEIGHT TO WEIGHT TOTAL
        weight_total += metricweight

    # sum weighted rankcols
    masterwrankcolname = f'MASTER COMPLEMENT WEIGHTED RANK {weight_total}'
    complementdf[masterwrankcolname] = complementdf[sumcols].sum(axis=1, min_count=len(sumcols))
    # rank overall weighted rankcol
    finalrankcolname = 'MASTER COMPLEMENT FINAL RANK'
    complementdf[finalrankcolname] = complementdf[masterwrankcolname].rank(ascending=1)
    # RE-SORT AND RE-INDEX
    complementdf.sort_values(ascending=True, by=['MASTER COMPLEMENT FINAL RANK'], inplace=True)
    complementdf.reset_index(drop=True, inplace=True)

    # ARCHIVE TO FILE
    filename = f"complementscore_ranks_existdate_{existdate}"
    complementdf.to_csv(index=False, path_or_buf=resultfolder / f"{filename}.csv")

    return complementdf
