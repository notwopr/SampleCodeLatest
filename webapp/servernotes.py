"""
Title: Server Stats
Date Started: Jan 22, 2022
Version: 1.00
Version Start: Jan 22, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Server stat info.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
import datetime as dt
from pathlib import Path
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS
from file_hierarchy import DirPaths, FileNames
from file_functions import readpkl
from Modules.price_history import grabsinglehistory
from Modules.numbers import formalnumber_integer
from globalvars import benchmarks

PRICES = Path(DirPaths().eodprices)
DATE_RESULTS = Path(DirPaths().date_results)
TICKERS = Path(DirPaths().tickers)
daterangedb_name = FileNames().fn_daterangedb
tickerlistcommon_name = FileNames().fn_tickerlistcommon


def getlastmodified(folder, filename):
    modtime_since_epoc = os.path.getmtime(folder / filename)
    modtime = dt.datetime.fromtimestamp(modtime_since_epoc).strftime('%Y-%m-%d %H:%M:%S')
    return modtime


def getstockdata():
    daterangefile = readpkl(daterangedb_name, DATE_RESULTS)
    # limit to common stock
    tickerlist_common = readpkl(tickerlistcommon_name, TICKERS)
    daterangefile = daterangefile[daterangefile['stock'].isin(tickerlist_common['symbol'])]
    # shift latest date by one to account for tiingo data sync idiosyncracy
    return {
        'earliest': np.min(daterangefile['first_date']),
        'latest': str(dt.date.fromisoformat(np.max(daterangefile['last_date'])) - dt.timedelta(days=1)),
        'numtickers': len(tickerlist_common['symbol'])
        }


# get benchmark earliest and latestdate
def getbenchdates(benchmarks):
    for k, v in benchmarks.items():
        benchprices = grabsinglehistory(v['ticker'])
        benchmarks[k].update({
            'earliestdate': benchprices.iloc[0]['date'],
            'latestdate': benchprices.iloc[-1]['date']
        })
    return benchmarks


# SERVER STATS


def gen_serverstat():
    server_stats = {
        'Stock data available': 'All common shares traded on the United States NASDAQ and NYSE exchanges.',
        'Types of pricing data available': 'End of Day prices only.',
        'Number of ticker symbols available': f'{formalnumber_integer(getstockdata()["numtickers"])}',
        'Stock price data last updated': f'{getlastmodified(PRICES, "allpricematrix_common.pkl")}',
        'Benchmark price data last updated': f'{getlastmodified(PRICES, "allpricematrix_bench.pkl")}',
        'Dates available for stock price data': f'{getstockdata()["earliest"]} to {getstockdata()["latest"]}'
        }
    for v in getbenchdates(benchmarks).values():
        server_stats.update(
            {f'Dates available for the {v["name"]} price data': f'{v["earliestdate"]} to {v["latestdate"]}'}
            )
    return server_stats
