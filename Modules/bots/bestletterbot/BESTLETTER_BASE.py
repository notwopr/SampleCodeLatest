"""
Title: RETRIEVE PRICE OF A STOCK ON GIVEN DATE
Date Started: Dec 14, 2020
Version: 1.00
Version Start: Dec 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Returns aggregate slopescore data by Starting Letter of a stock's name.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
from pathlib import Path
#   THIRD PARTY IMPORTS
import pandas as pd
from scipy import stats
import numpy as np
#   LOCAL APPLICATION IMPORTS
from Modules.price_history_slicing import pricedf_daterange
from Modules.metriclibrary.STRATTEST_FUNCBASE_RAW import slopescore_single
from file_hierarchy import FileNames, DirPaths
from file_functions import join_str
from Modules.tickerportalbot import tickerportal4
from Modules.multiprocessing import multiprocessorshell_mapasync_getresults

daterangedb_source = Path(join_str([DirPaths().date_results, f"{FileNames().fn_daterangedb}.pkl"]))


# get stats for one letter
def getletterdata_single(tickerlist, asofdate, letter):
    binofslopescores = [slopescore_single(pricedf_daterange(ticker, '', asofdate)) for ticker in tickerlist if ticker.startswith(letter)]
    num_samples = len(binofslopescores)
    mean = np.mean(binofslopescores)
    median = np.median(binofslopescores)
    stdev = np.std(binofslopescores)
    madev = stats.median_abs_deviation(binofslopescores)
    mean_upper = mean + stdev
    mean_lower = mean - stdev
    median_upper = median + madev
    median_lower = median - madev
    summary = {
        'First Letter': letter,
        f'Number of Tickers (as of {asofdate})': num_samples,
        '% of Total': (num_samples / len(tickerlist))*100,
        'Mean % growth per day': mean*100,
        'Median % growth per day': median*100,
        'Mean Upper Bound (std used)': mean_upper*100,
        'Mean Lower Bound (std used)': mean_lower*100,
        'Median Upper Bound (mad used)': median_upper*100,
        'Median Lower Bound (mad used)': median_lower*100,
        'Spread (Standard Deviation)': stdev*100,
        'Spread (Median Absolute Deviation)': madev*100
        }
    return summary


def masterbestletter(global_params):

    alphabetstr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # get tickers that have atleast two rows of prices
    tickerlist = tickerportal4(global_params['presentdate'], global_params['presentdate'], 'common', 1)
    targetvars = (tickerlist, global_params['presentdate'])
    allsummaries = multiprocessorshell_mapasync_getresults(getletterdata_single, list(alphabetstr), 'no', targetvars, global_params['chunksize'])
    summdf = pd.DataFrame(data=allsummaries)
    return summdf
