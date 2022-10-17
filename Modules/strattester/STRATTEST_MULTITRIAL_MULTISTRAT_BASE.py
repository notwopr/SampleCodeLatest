"""
Title: STRATTEST MULTITRIAL MULTISTRAT BASE
Date Started: July 10, 2020
Version: 2.00
Version Start: Oct 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given an existence date, runs pool thru first pass screening, runs again through given screening method, and returns percentage of resulting pool that beat market during the test period.
VERSIONS:
1.01: Optimize with updated functions.  Allow for more modulatory.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import importlib
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from STRATTEST_MULTITRIAL_BASE import strattest_multitrial, setpreconfigsamples
from STRATTEST_MULTITRIAL_BASE_LEADERBOARD import leaderboardsummary


# modify stratpanel stage2
def stage2stratpanelmodifier(s2setup, strat_panel):
    if s2setup == 'fundyonly':
        dictiters = ['SCREENPARAMS_STAGE2_psloperevplusfcf_FILTER']
    elif s2setup == 'fundys2v2':
        dictiters = ['SCREENPARAMS_STAGE2_psloperevplusfcf_FILTER', 'SCREENPARAMS_STAGE2v2']
    elif s2setup == 'fundys2v2a':
        dictiters = ['SCREENPARAMS_STAGE2_psloperevplusfcf_FILTER', 'SCREENPARAMS_STAGE2v2a']
    elif s2setup == 'fundys2v2b':
        dictiters = ['SCREENPARAMS_STAGE2_psloperevplusfcf_FILTER', 'SCREENPARAMS_STAGE2v2b']
    # for each stage 2 strat to run, add to strat panel
    counter = 'I'
    for iterable in dictiters:
        # pull up script params
        iterparamname = f'Screenparams.{iterable}'
        itermodule = importlib.import_module(iterparamname)
        iterparams = itermodule.stage2_params
        # update strat_panel
        strat_panel.update({f'Stage 2 Part {counter}': iterparams})
        counter += 'I'
    return strat_panel


# RUN MULTITRIALS ON MULTIPLE DIFFERENT STRAT PANELS
def stage3scriptloader(iterableprefix, iterable):
    # pull up script params
    iterparamname = f'{iterableprefix}{iterable}'
    itermodule = importlib.import_module(iterparamname)
    iterparams = itermodule.stage3_params
    return iterparams


# RUN MULTITRIALS ON MULTIPLE DIFFERENT STRAT PANELS
def stratpanelmodifier(iterableprefix, iterable, strat_panel):
    # pull up script params
    iterparamname = f'{iterableprefix}{iterable}'
    itermodule = importlib.import_module(iterparamname)
    iterparams = itermodule.stage3_params
    # update strat_panel
    strat_panel.update({'Stage 3': iterparams})
    return strat_panel


# RUN MULTITRIALS ON MULTIPLE DIFFERENT STRAT PANELS
def multistrat_multitrials(iternum, rootdir, sourcefolder, global_params, strat_panel):
    # pull up script params
    iterparamname = f'Screenparams.SCREENPARAMS_STAGE3_WINRATERANKERv{iternum}'
    itermodule = importlib.import_module(iterparamname)
    iterparams = itermodule.stage3_params
    # update strat_panel
    strat_panel.update({'Stage 3': iterparams})
    # run multitrials
    multitrialstatsdf = strattest_multitrial(rootdir, global_params, strat_panel)
    # create leaderboard summary
    leaderboardsummary(sourcefolder, global_params, strat_panel, multitrialstatsdf)
    # update testnumber
    testnumber = global_params['testnumber'] + 1
    global_params.update({'testnumber': testnumber})


# RUN MULTITRIALS ON MULTIPLE DIFFERENT STRAT PANELS
def multistrat_multitrials_winrateranker(rootdir, sourcefolder, global_params, strat_panel, sourcetype, stat_type, rankmeth, winlen_ceiling):
    # pull up basescript params
    iterparamname = 'Screenparams.SCREENPARAMS_STAGE3_WINRATERANKERv22'
    itermodule = importlib.import_module(iterparamname)
    iterparams = itermodule.stage3_params
    # update scriptname
    #   create new scriptname
    #       add source
    if sourcetype == 'oldbareminraw':
        scriptcode = 'bmin'
    elif sourcetype == 'trueline':
        scriptcode = 'true'
    elif sourcetype == 'rawprice':
        scriptcode = 'raw'
    elif sourcetype == 'baremaxraw':
        scriptcode = 'bmax'
    elif sourcetype == 'straight':
        scriptcode = 'straight'
    #       add stat
    if stat_type == 'mean':
        scriptcode += 'mn'
    elif stat_type == 'median':
        scriptcode += 'med'
    else:
        scriptcode += stat_type
    #       add rankmeth
    if rankmeth == 'standard':
        scriptcode += 'Rs'
    elif rankmeth == 'minmax':
        scriptcode += 'Rmm'
    elif rankmeth == 'minmax_nan':
        scriptcode += 'Rmmn'
    iterparams.update({
        'scriptname': f'WRR{scriptcode}WLC{winlen_ceiling}'
    })
    # update stattype, sourcetype, winlenceiling, rankmeth, metricname
    iterparams['scriptparams'][0].update({
        'stat_type': stat_type,
        'sourcetype': sourcetype,
        'winlen_ceiling': winlen_ceiling,
        'rankmeth': rankmeth
    })
    # update rawvalrankdirection
    if stat_type in ['std', 'mad', 'dev']:
        iterparams['scriptparams'][0].update({
            'rawvalrankdirection': 1
        })
    elif stat_type in ['mean', 'median', 'avg']:
        iterparams['scriptparams'][0].update({
            'rawvalrankdirection': 0
        })
    # update global param rankmeth
    if rankmeth == 'standard':
        global_params.update({'rankmeth': rankmeth})
    elif rankmeth == 'minmax' or rankmeth == 'minmax_nan':
        global_params.update({'rankmeth': 'minmax'})

    # update strat_panel
    strat_panel.update({'Stage 3': iterparams})
    # set preconfigured trial samples
    preconfigsamples = setpreconfigsamples(global_params)
    # run multitrials
    multitrialstatsdf = strattest_multitrial(rootdir, global_params, preconfigsamples, strat_panel)
    # create leaderboard summary
    leaderboardsummary(sourcefolder, global_params, strat_panel, multitrialstatsdf)
    # update testnumber
    testnumber = global_params['testnumber'] + 1
    global_params.update({'testnumber': testnumber})


# MODIFY PARAMSCRIPT
def paramscriptmodifier(strat_panel, lbperiod, age_type):
    iterparams = strat_panel['Stage 3']
    # update scriptname
    iterparams.update({
        'scriptname': f'slopescoreplus{age_type}_LB{lbperiod}'
    })
    # for each metricitem in script
    for metricitem in iterparams['scriptparams']:
        if metricitem['metricname'] == 'slopescore':
            iterparams['scriptparams']
            metricitem.update({
                'look_back': lbperiod
            })
        if metricitem['metricname'].startswith('age'):
            if age_type == 'age_younger':
                rankdir = 1
            elif age_type == 'age_older':
                rankdir = 0
            iterparams['scriptparams']
            metricitem.update({
                'metricname': age_type,
                'rankascending': rankdir
            })
    # update strat_panel
    strat_panel.update({'Stage 3': iterparams})
    return strat_panel
