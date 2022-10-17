"""
Title: Best Performers Base Script
Date Started: Dec 7, 2019
Version: 2.0
Version Start: September 23, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Functions to return list of best performing stocks given time period
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl, savetopkl, buildfolders_singlechild
from Modules.tickerportalbot import tickerportal2
from file_hierarchy import PRICES, daterangedb_source, tickerlistcommon_source
from Modules.growthcalcbot import get_growthdf
from Modules.referencetools.quickref.GETMETRICVALDF import getallmetricvalsdf
from Modules.dataframe_functions import filtered_single


def bestperformer_cruncher(configdict):

    beg_date = configdict['beg_date']
    end_date = configdict['end_date']

    # GET LIST OF ALL STOCKS EXISTING FOR THAT PERIOD
    allexistingstocks = tickerportal2(daterangedb_source, tickerlistcommon_source, beg_date, 'common')

    # CALCULATE GROWTH
    if len(allexistingstocks) != 0:
        # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
        pricematrixdf = readpkl('allpricematrix_common', PRICES)

        # GET STOCK GROWTH
        sliced = get_growthdf(pricematrixdf, allexistingstocks, beg_date, end_date, False)
        # IF BENCHMARKS REQUESTED, ADD BENCHMARK PERF TO RESULTS
        if 'compare' in configdict['checklist']:
            benchmatrixdf = readpkl('allpricematrix_bench', PRICES)
            benchsliced = get_growthdf(benchmatrixdf, ["^DJI", "^INX", "^IXIC"], beg_date, end_date, False)
            # APPEND TO MAIN DF
            sliced = pd.concat([sliced, benchsliced], ignore_index=True)

        # sort and reset index
        sliced.sort_values(ascending=False, by=[f'GROWTH {beg_date} TO {end_date}'], inplace=True)
        sliced.reset_index(drop=True, inplace=True)

        # annualize if requested
        if 'annualize' in configdict['checklist']:
            num_years = (dt.date.fromisoformat(end_date) - dt.date.fromisoformat(beg_date)).days / 365
            sliced['ANNUALIZED RATE'] = ((sliced[f'GROWTH {beg_date} TO {end_date}'] + 1) ** (1 / num_years)) - 1

        # include only marketbeaters
        if 'beat' in configdict['checklist']:
            # determine best performing index rate
            bestbenchrate = sliced[sliced['STOCK'].isin(["^DJI", "^INX", "^IXIC"])][f'GROWTH {beg_date} TO {end_date}'].max()
            # remove stocks that are less than best benchrate
            sliced = sliced[sliced[f'GROWTH {beg_date} TO {end_date}'] >= bestbenchrate + configdict['marginrate']]

        # add HIP fatscore and maxdd metrics
        for group in ['hip', 'life']:
            if group == 'life':
                metbeg_date = ''
            else:
                metbeg_date = beg_date
            metricsdf = getallmetricvalsdf(metbeg_date, end_date, group, sliced['STOCK'].tolist())
            sliced = sliced.join(metricsdf.set_index('stock'), how="left", on="STOCK")

        # add HIP GRO TO LIFE FAT RATIO
        sliced['hipgrolifefatratio'] = sliced[f'GROWTH {beg_date} TO {end_date}'] / sliced['life_rawbmaxfatscore']

        # filter if requested
        for group in ['hip', 'life']:
            if configdict[f'fatscorecap_{group}'] is not None:
                sliced = filtered_single(sliced, configdict[f'fatscorecap_{group}_filter'], configdict[f'fatscorecap_{group}'], f'{group}_rawbmaxfatscore')
            if configdict[f'maxddcap_{group}'] is not None:
                sliced = filtered_single(sliced, configdict[f'maxddcap_{group}_filter'], configdict[f'maxddcap_{group}'], f'{group}_maxdd')
        if configdict['hipgrolifefatcap'] is not None:
            sliced = filtered_single(sliced, configdict['hipgrolifefatcap_filter'], configdict['hipgrolifefatcap'], 'hipgrolifefatratio')

        # save if requested
        if 'save' in configdict['checklist']:
            savedir = buildfolders_singlechild(configdict['rootdir'], configdict['testregimename'])
            savefilename = f'bestof{beg_date}_to_{end_date}'
            savetopkl(savefilename, savedir, sliced)
            sliced.to_csv(index=False, path_or_buf=savedir / f"{savefilename}.csv")

        # report results
        return sliced
    else:
        return f'No stocks existed on {beg_date}!  Program exiting now...'
