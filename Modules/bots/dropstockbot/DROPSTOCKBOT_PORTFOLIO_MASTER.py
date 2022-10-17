"""
Title: DROP STOCK BOT MASTER
Date Started: Dec 8, 2020
Version: 1.00
Version Start: Dec 8, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Runs dropstockbot on multiple stocks and returns dataframe of results.
benchgain_currfilter = only runs trials on those where the bench gain is comparable to the current state.
For each stock in the chosen portfolio, it runs dropstockbot.  Dropstockbot runs several trials.  For each trial, it finds the pool of ideal stocks.  Then it finds the probability that stocks that fit a given profile (growth, margin, beatpct as of a certain investment date) will be an ideal stock at the end of the investment period.  This portfolio version instead of taking a custom candidate profile, takes the profile of the stock in the portfolio it is examining.  E.g. it is day 35 of investing in stock X.  It currently has a gain of Y%.  That becomes its profile for the growth part of the profile.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
from memory_profiler import profile
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from DROPSTOCKBOT_PORTFOLIO_BASE import dropstockbot_portfolio
from filelocations import readpkl
from tickerportalbot import tickerportal4
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, tickerlistcommon_source


fndatepoolset = 'D20201217T1_trialrunset'
datepoolsetdir = r'D:\BOT_DUMP'
trialrunset = readpkl(fndatepoolset, Path(datepoolsetdir))
portfolio = [
    'ASO',
    'CARR',
    'CDW',
    'CMBM',
    'CRSR',
    'NET',
    'OKTA',
    'RXT'
        ]


global_params = {
    'todaysdate': '2021-08-17',
    'testnumber': 1,
    'testregimename': 'dropbot',
    'candidate_profile': {
        'growth_curr': 0,
        'growth_err': 0.03,
        #'margin_curr': 0,
        #'margin_err': 0.03,
        #'beatpct_curr': 0,
        #'beatpct_err': 0.03,
        'benchticker': '^IXIC'
        },
    'ideal_profile': {
        #'mktbeater': 'yes',
        'min_gain': 0.70,
        # 'min_margin': 0.30
        },
    'trialtype': 'random',
    'benchgain_currfilter': 'no',
    'benchgain_err': 0.05,
    'num_trials': 100,
    'investperiod': 365,
    'portfolio': portfolio,
    'investstartdate': '2021-05-01',
    'currinvestdate': '2021-08-12',
    'benchticker': '^IXIC',
    'latestdate': '',
    'firstdate': '1990-01-01',
    'existingset': [],#trialrunset
    'chunksize': 5
}


#@profile
#def runmemprof():
    #dropstockbot_portfolio(computerobject.bot_dump, global_params)


if __name__ == '__main__':
    #runmemprof()
    dropstockbot_portfolio(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
