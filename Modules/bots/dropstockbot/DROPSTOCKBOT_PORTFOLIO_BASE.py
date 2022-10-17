"""
Title: DROP STOCK BOT PORTFOLIO MASTER
Date Started: Dec 14, 2020
Version: 1.00
Version Start: Dec 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Runs dropstockbot on multiple stocks and returns dataframe of results.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import copy
import datetime as dt
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import buildfolders_singlechild, buildfolders_regime_testrun, readpkl
from UPDATEPRICEDATA_FILELOCATIONS import PRICES
from growthcalcbot import get_growthdf, getgrowthrate_single
from DROPSTOCKBOT_BASE import gettrialiterables, getsummariesandstats
from QUICKREF_GETBEATPCT_BASE import getbeatpct
from QUICKREF_GETPRICE_BASE import getsingleprice


# return idealcode
def profilecoder(profiledict, mode):
    # make list of keys in profile
    listofdescriptors = list(profiledict.keys())
    profilecode = ''
    if mode == 'ideal':
        if 'mktbeater' in listofdescriptors:
            profilecode += 'B'
        if 'min_gain' in listofdescriptors:
            profilecode += f'G>{profiledict["min_gain"]}'
        if 'min_margin' in listofdescriptors:
            profilecode += f'M>{profiledict["min_margin"]}'
    elif mode == 'candidate':
        if 'growth_curr' in listofdescriptors:
            profilecode += 'G'
        if 'margin_curr' in listofdescriptors:
            profilecode += 'M'
        if 'beatpct_curr' in listofdescriptors:
            profilecode += 'B'
    return profilecode


# create portfoliosourcedf
def createportsource(portfolio, startdate, enddate, benchticker, daysinvested, benchgain_curr):
    # create masterdf
    masterdf = pd.DataFrame(data={'TICKER': portfolio})
    # add days invested column
    masterdf['Days Invested'] = daysinvested
    # add current price
    masterdf['Current Price'] = masterdf['TICKER'].apply(lambda x: getsingleprice(x, enddate))
    # get current gain
    pricematrixdf = readpkl('allpricematrix_common', PRICES)
    growthdf = get_growthdf(pricematrixdf, portfolio, startdate, enddate, False)
    # change column name
    growthdf.rename(columns={'STOCK': 'TICKER', f'GROWTH {startdate} TO {enddate}': 'Current Gain'}, inplace=True)
    # add benchmark ticker
    growthdf['Bench Ticker'] = benchticker
    # get and add benchmark growth
    growthdf['Current Bench Gain'] = benchgain_curr
    # get current margin
    growthdf['Current Margin'] = growthdf['Current Gain'] - benchgain_curr
    # join growthdf to masterdf
    masterdf = masterdf.join(growthdf.set_index('TICKER'), how="left", on="TICKER")
    # get beatpct
    beatpct_params = {
        'portfolio': portfolio,
        'investstart': startdate,
        'investend': enddate,
        'benchticker': benchticker,
        'verbose': ''
    }
    beatpctdf = getbeatpct(beatpct_params)
    # join beatpctdf to masterdf
    masterdf = masterdf.join(beatpctdf.set_index('TICKER'), how="left", on="TICKER")
    # save portsourcedf
    return masterdf


def dropstockbot_portfolio(rootdir, global_params):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(rootdir, global_params['testnumber'], global_params['todaysdate'], global_params['testregimename'])
    # get daysinvested
    daysinvested = (dt.date.fromisoformat(global_params['currinvestdate']) - dt.date.fromisoformat(global_params['investstartdate'])).days
    # get benchgain_curr
    benchgain_curr = getgrowthrate_single(global_params['benchticker'], global_params['investstartdate'], global_params['currinvestdate'])
    # get portsourcedf
    portsourcedf = createportsource(global_params['portfolio'], global_params['investstartdate'], global_params['currinvestdate'], global_params['benchticker'], daysinvested, benchgain_curr)
    # get trial iterables
    global_params.update({
        'daysinvested': daysinvested,
        'benchgain_curr': benchgain_curr
        })
    trialrunset = gettrialiterables(testrunparent, global_params)
    # make modifiable copy of globalparams dict
    modparams = copy.deepcopy(global_params)
    # create candidate profile
    candidate_profile = modparams['candidate_profile']
    candidate_profile.update({'daysinvested': daysinvested})
    # for each stock in portfolio, run dropstockbot to get statdict
    alltickerstats = []
    for ticker in portsourcedf['TICKER']:
        # modify candidate profile
        if 'growth_curr' in candidate_profile.keys():
            growth_curr = portsourcedf[portsourcedf['TICKER'] == ticker]['Current Gain'].item()
            candidate_profile.update({'growth_curr': growth_curr})
        if 'margin_curr' in candidate_profile.keys():
            margin_curr = portsourcedf[portsourcedf['TICKER'] == ticker]['Current Margin'].item()
            candidate_profile.update({'margin_curr': margin_curr})
        if 'beatpct_curr' in candidate_profile.keys():
            beatpct_curr = portsourcedf[portsourcedf['TICKER'] == ticker]['Current Beatpct'].item()
            candidate_profile.update({'beatpct_curr': beatpct_curr})
        # update modifiable global params
        modparams.update({'candidate_profile': candidate_profile})
        # make dumpfolder for this iteration
        dropstockbotdump = buildfolders_singlechild(testrunparent, f'dropstockbotdump_{ticker}')
        # run dropstockbot on this iteration of modparams
        statdict = getsummariesandstats(dropstockbotdump, trialrunset, modparams)
        # establish candidate code
        candidcode = profilecoder(candidate_profile, 'candidate')
        # establish idealcode
        ideal_profile = modparams['ideal_profile']
        idealcode = profilecoder(ideal_profile, 'ideal')
        # pull median, mean, and std from data
        testrunname = f' P(cand({candidcode})=ideal({idealcode}))'
        tickerstats = {
            'TICKER': ticker,
            f'MEAN_{testrunname}': statdict['stat_mean'],
            f'MEDIAN_{testrunname}': statdict['stat_med'],
            f'STD_{testrunname}': statdict['stat_std']
        }
        alltickerstats.append(tickerstats)
    # create df of tickerstats
    tickerstatdf = pd.DataFrame(data=alltickerstats)
    # join to masterdf
    portsourcedf = portsourcedf.join(tickerstatdf.set_index('TICKER'), how="left", on="TICKER")
    # save to file
    filename = 'portfoliogrowthprobabilities'
    portsourcedf.to_csv(index=False, path_or_buf=testrunparent / f"{filename}.csv")
