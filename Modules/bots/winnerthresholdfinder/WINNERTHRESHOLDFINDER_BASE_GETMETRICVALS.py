"""
Title: WINNER THRESHOLD FINDER BASE - GET METRICVALS
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
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import savetopkl, buildfolders_singlechild
from STRATTEST_FUNCBASE import getmetcolname
from genericfunctionbot import multiprocessorshell
from STRATTEST_SINGLE_BASE_CRUNCHER_ALLMETRICVALS import lookbackshell_single, recoverybotshell_single, winraterankershell, getbenchmatrixchangedf


def getallwinnermetricvals_single(savedir, scriptname, scriptparams, beg_date, end_date, tickerlist, rankmeth, rankregime, savemode, chunksize):

    # construct masterdf
    masterdf = pd.DataFrame(data={'stock': tickerlist})
    # separate winrate- from nonwinrate- metrics
    winratemetrics_to_run = [metricitem for metricitem in scriptparams if metricitem['metricname'].startswith('winrateranker') is True]
    nonwinratemetrics_to_run = [metricitem for metricitem in scriptparams if metricitem['metricname'].startswith('winrateranker') is False]

    # get metric vals for all non-winrate metrics
    if len(nonwinratemetrics_to_run) != 0:
        nonwinratedump = buildfolders_singlechild(savedir, 'nonwinrate_dumpfiles')
        # load marketbeater benchmarkdf if metric chosen
        benchmatrixchangesdf = ''
        for metricitem in nonwinratemetrics_to_run:
            if metricitem['metricname'].startswith('marketbeater') or metricitem['data'] == 'margindpc_nonzero' or metricitem['data'] == 'margindpc':
                # get tickers
                if metricitem['metricname'].startswith('marketbeater'):
                    benchtickers = list(metricitem['bweights'].keys())
                else:
                    benchtickers = ['^IXIC']
                benchmatrixchangesdf = getbenchmatrixchangedf(benchtickers)
        # run metricsval multiprocessor
        mpfunc = lookbackshell_single
        if scriptname.startswith('recoverybot'):
            mpfunc = recoverybotshell_single
        multiprocessorshell(nonwinratedump, mpfunc, tickerlist, 'no', (nonwinratedump, nonwinratemetrics_to_run, benchmatrixchangesdf, beg_date, end_date), chunksize)
        # construct metricsdf
        table_results = []
        for child in nonwinratedump.iterdir():
            with open(child, "rb") as targetfile:
                unpickled_raw = pkl.load(targetfile)
            table_results.append(unpickled_raw)
        nonwinratedf = pd.DataFrame(data=table_results)
        # append df to masterdf
        masterdf = masterdf.join(nonwinratedf.set_index('stock'), how="left", on="stock")

    # run winrate metrics if any
    if len(winratemetrics_to_run) != 0:
        # for each winratemetric..
        for winratemetricitem in winratemetrics_to_run:
            metcolname = getmetcolname(winratemetricitem)
            # create winratemetric folders
            metric_dumpfolder = buildfolders_singlechild(savedir, f'{metcolname}_dumpfiles')
            wrprepdf = winraterankershell(savedir, metric_dumpfolder, metcolname, winratemetricitem, beg_date, end_date, tickerlist, rankmeth, rankregime, savemode)
            # append df to masterdf
            masterdf = masterdf.join(wrprepdf.set_index('stock'), how="left", on="stock")

    # ARCHIVE TO FILE
    filename = f"allmetricvals_as_of_{end_date}"
    if savemode == 'pkl':
        savetopkl(filename, savedir, masterdf)
    elif savemode == 'csv':
        masterdf.to_csv(index=False, path_or_buf=savedir / f"{filename}.csv")
    return masterdf
