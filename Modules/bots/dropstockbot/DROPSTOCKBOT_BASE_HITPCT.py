"""
Title: DROP STOCK BOT BASE _MATCH MARGIN
Date Started: Dec 8, 2020
Version: 1.00
Version Start: Dec 8, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Finds stocks that match a certain interim marginal gain.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import readpkl, savetopkl
from UPDATEPRICEDATA_FILELOCATIONS import PRICES
from genericfunctionbot import intersectlists, multiprocessorshell
from DROPSTOCKBOT_BASE_IDEALS import getidealslist_single
from DROPSTOCKBOT_BASE_CANDIDATES import getcandidateslist_single


# get hitpct of single trial
def gethitpct_single(dumpfolder, pricematrixdf, benchpricematrixdf, ideal_profile, candidate_profile, trialiter):
    existpool = trialiter['pool']
    existdate = trialiter['existdate']
    interim_date = trialiter['interim_date']
    daysinvested = trialiter['daysinvested']
    end_date = trialiter['end_date']
    trialno = trialiter['trialno']
    benchticker = trialiter['benchticker']
    benchgain = trialiter['benchgain']
    benchgain_curr = trialiter['benchgain_curr']
    benchprice_enddate = trialiter['benchprice_enddate']
    # prep trial summary
    trialsumm = {
        'trialno': trialno,
        'existdate': existdate,
        'end_date': end_date,
        'interim_date': interim_date,
        'daysinvested': daysinvested,
        'benchticker': benchticker,
        'benchgain': benchgain,
        'benchgain_curr': benchgain_curr,
        'benchprice_enddate': benchprice_enddate
    }
    # get pool of ideal stocks
    idealstocks = getidealslist_single(pricematrixdf, existpool, existdate, end_date, benchgain, ideal_profile)
    # if no ideal stocks, then trial doesn't count
    if len(idealstocks) == 0:
        suppdict = {
            'num_hits': None,
            'num_total': None,
            'hitpct': None
        }
        print(f'Trial {trialno} ({existdate} to {end_date}) had no ideal stocks.')
    else:
        # if no qualifications for candidates exist, return full pool
        if not bool(candidate_profile) is True:
            candidatestocks = existpool
        else:
            # filter existpool by candidate qualifications
            candidatestocks = getcandidateslist_single(pricematrixdf, benchpricematrixdf, existpool, existdate, interim_date, benchgain_curr, candidate_profile)
        # if no candidates remain after filtration then trial doesn't count
        if len(candidatestocks) == 0:
            suppdict = {
                'num_hits': None,
                'num_total': None,
                'hitpct': None
            }
            print(f'Trial {trialno} ({existdate} to {interim_date}) had no candidate stocks.')
        else:
            # calculate proportion of candidates that are ideals
            intersecthits = intersectlists(candidatestocks, idealstocks)
            num_hits = len(intersecthits)
            num_total = len(candidatestocks)
            suppdict = {
                'num_hits': num_hits,
                'num_total': num_total,
                'hitpct': num_hits / num_total
            }
    # update trial summary
    trialsumm.update(suppdict)
    # save to file
    savetopkl(f'hitpct_trial{trialno}', dumpfolder, trialsumm)


# run trials to get each trial hitpct
def gethitpct_all(savedir, dumpfolder, ideal_profile, candidate_profile, trialiters, chunksize):
    # load price matrices into RAM
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    if 'beatpct_curr' in candidate_profile.keys():
        benchpricematrixdf = readpkl('allpricematrix_bench', PRICES)
    else:
        benchpricematrixdf = None
    # run multiprocessor
    targetvars = (dumpfolder, pricematrixdf, benchpricematrixdf, ideal_profile, candidate_profile)
    multiprocessorshell(dumpfolder, gethitpct_single, trialiters, 'no', targetvars, chunksize)
    # assemble results
    allmktbeatpcts = []
    for child in dumpfolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        allmktbeatpcts.append(unpickled_raw)
    alltrialsummdf = pd.DataFrame(data=allmktbeatpcts)
    # save
    alltrialsummdf.to_csv(index=False, path_or_buf=savedir / "alltrialsummaries.csv")
    return alltrialsummdf
