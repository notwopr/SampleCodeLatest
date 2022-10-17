"""
Title: Strat Tester
Date Started: Feb 15, 2022
Version: 1.00
Version Start: Feb 15, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import time
import importlib
import copy
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from Modules.dates import plusminusdays
from webapp.botclasses import BotParams
from webapp.os_functions import get_currentscript_filename
from webapp.botrun_parambuilder import brpb_base
from webapp.routers.strattester_helper_stratpanels import stratlib
from webapp.routers.strattester_helper_leaderboard import savetestrun
from Modules.strattester.STRATTEST_SEQUENTIAL import run_strat_sequential
from file_functions import delete_folder, getbotsinglerunfolder, getobject_byvarname
from Modules.timeperiodbot import random_dates
from webapp.common_resources import staticmaxdate


bp = BotParams(
    get_currentscript_filename(__file__),
    'Strategy Tester',
    "Given a stock screening strategy, report how your portfolio would perform if you use the strategy for a given date range.",
    None
)


def calc_currenddate(p, n, s):
    return dt.date.fromisoformat(s) + dt.timedelta(days=p*n)


def modifymin_preath_age(stagemetrics, min_preath_age):
    for i in stagemetrics['scriptparams']:
        if 'min_preath_age' in i.keys():
            i['min_preath_age'] = min_preath_age
    return stagemetrics


def strattest_singlerun(period, num_periods, start_date, min_age, rankend, strat):
    brp = {**brpb_base(bp.botid, 1), **{
        'strat_name': strat,
        'investperiod': period,
        'startdate': start_date,
        'enddate': str(calc_currenddate(period, num_periods, start_date)),
        'minimumage': min_age,
        'startcapital': 1000,
        'benchmark': '^IXIC',
        'rankstart': 0,
        'rankend': rankend,
        'rankmeth': 'standard',
        'rankregime': '1isbest'
    }}
    # retrieve panel data
    libsourcecopy = copy.deepcopy(stratlib[strat])
    metriclist = getobject_byvarname(libsourcecopy['stages']['Stage 3'][0], libsourcecopy['stages']['Stage 3'][1])
    libsourcecopy['stages']['Stage 3'] = metriclist
    brp['strat_panel'] = libsourcecopy
    #brp['strat_panel']['stages']['Stage 3'] = modifymin_preath_age(brp['strat_panel']['stages']['Stage 3'], min_preath_age)
    start = time.time()
    endcapital, endcapital_bench, allperiodstatdf, numperiods, stockperfdfreports = run_strat_sequential(brp)
    end = time.time()
    savetestrun(brp, allperiodstatdf, num_periods, end-start)
    delete_folder(getbotsinglerunfolder(brp['rootdir'], brp['testregimename'], brp['todaysdate'], brp['testnumber']))


if __name__ == '__main__':
    rankend = 6
    min_age = 180
    period = 30
    num_periods = 20#(360 // period) * 5
    #for rankend in [6, 8, 10, 15]:
    version = 'RBv9'
    for mpa in [2, 360, 720]:
        for start_date in ['2008-10-16']:
            for occur in ['first', 'last']:
                # 2008-10-16 best date for orig RBv9
                # 1997-04-24 worst date for orig RBv9
                # 2001-01-01 date where bench was negative and orig RBv9 was good
                # 2006-12-19 date where bench was negative and orig RBv9 was bad
                #newmaxdate = plusminusdays(staticmaxdate, (period * num_periods), 'subtract')
                #start_date = random_dates('1995-01-01', newmaxdate, 1)[0]
                strattest_singlerun(period, num_periods, start_date, min_age, rankend, f'S3_{version}_{occur}_mpa{mpa}')
    '''
    for mpa in [2, 360, 720]:
        for start_date in ['1997-04-24', '2001-01-01', '2006-12-19']:
            for occur in ['first', 'last']:
                # 2008-10-16 best date for orig RBv9
                # 1997-04-24 worst date for orig RBv9
                # 2001-01-01 date where bench was negative and orig RBv9 was good
                # 2006-12-19 date where bench was negative and orig RBv9 was bad
                #newmaxdate = plusminusdays(staticmaxdate, (period * num_periods), 'subtract')
                #start_date = random_dates('1995-01-01', newmaxdate, 1)[0]
                strattest_singlerun(period, num_periods, start_date, min_age, rankend, f'S3_{version}_{occur}_mpa{mpa}')
    for version in ['RBv10a', 'RBv10d']:
        for mpa in [3, 360, 720]:
            for start_date in ['2008-10-16', '1997-04-24', '2001-01-01', '2006-12-19']:
                for occur in ['first', 'last']:
                    # 2008-10-16 best date for orig RBv9
                    # 1997-04-24 worst date for orig RBv9
                    # 2001-01-01 date where bench was negative and orig RBv9 was good
                    # 2006-12-19 date where bench was negative and orig RBv9 was bad
                    #newmaxdate = plusminusdays(staticmaxdate, (period * num_periods), 'subtract')
                    #start_date = random_dates('1995-01-01', newmaxdate, 1)[0]
                    strattest_singlerun(period, num_periods, start_date, min_age, rankend, f'S3_{version}_{occur}_mpa{mpa}')
    '''
