"""
Title: STRATTEST MULTITRIAL BASE - TRIAL RUN SET FUNCTIONS
Date Started: Mar 4, 2021
Version: 1.00
Version Start: Mar 4, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Functions for creating a multitrial run set of date-pool iterables.
VERSIONS:
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_singlechild, savetopkl
from tickerportalbot import tickerportal4, tickerportal6
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, tickerlistcommon_source, daterangedb_source_fundies
from timeperiodbot import getrandomexistdate_multiple, alldatewithtestlen
from genericfunctionbot import multiprocessorshell


# get list of qualifiers
def getedatepool_single(destfolder, fundycompatpools, agemin, fundyagemin, lastfundyreportage, trial):
    trialno = trial[0]
    existdate = trial[1]
    # get existpool
    if fundycompatpools == 'yes':
        startpool = tickerportal6(daterangedb_source_fundies, existdate, existdate, 'common', agemin, fundyagemin, lastfundyreportage)
    else:
        startpool = tickerportal4(existdate, existdate, 'common', agemin)
    trialdata = {
        'trialno': trialno,
        'existdate': existdate,
        'startpool': startpool
    }
    # save to file
    savetopkl(f'edatepool_trial{trialno}', destfolder, trialdata)


# get date-pool-benchgain iterables
def gettrialiterables(savedir, global_params):
    # get trialexistdates
    if len(global_params['existingset']) != 0:
        trialrunset = global_params['existingset']
    else:
        if global_params['trialtype'] == 'random':
            # get trialexistdates
            alltrialexistdates = getrandomexistdate_multiple(global_params['num_trials'], global_params['firstdate'], global_params['latestdate'], global_params['testlen'], daterangedb_source)
        elif global_params['trialtype'] == 'full':
            alltrialexistdates = alldatewithtestlen(global_params['testlen'], global_params['firstdate'], global_params['latestdate'], daterangedb_source, 'ascending')
        # build dump folder
        datepooldump = buildfolders_singlechild(savedir, 'datepooldump')
        # run multiprocessor
        targetvars = (datepooldump, global_params['fundycompatpools'], global_params['minimumage'], global_params['fundyagemin'], global_params['lastfundyreportage'])
        multiprocessorshell(datepooldump, getedatepool_single, alltrialexistdates, 'yes', targetvars, global_params['chunksize'])
        # assemble results
        trialrunset = []
        for child in datepooldump.iterdir():
            with open(child, "rb") as targetfile:
                unpickled_raw = pkl.load(targetfile)
            trialrunset.append(unpickled_raw)
        # save trialrunset
        mod_date = global_params['todaysdate'].replace("-", "")
        testcode = 'D' + mod_date + 'T' + str(global_params['testnumber'])
        savetopkl(f'{testcode}_trialrunset', savedir, trialrunset)
    return trialrunset
