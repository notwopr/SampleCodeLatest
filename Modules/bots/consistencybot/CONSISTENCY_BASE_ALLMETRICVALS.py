"""
Title: CONSISTENCY BOT - ALLMETRIC VALUES
Date Started: Dec 30, 2020
Version: 1.00
Version Start: Dec 30, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Same as strattest version except non multiprocessor.

VERSION NOTES

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from filelocations import savetopkl, readpkl
from UPDATEPRICEDATA_FILELOCATIONS import PRICES
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher
from STRATTEST_FUNCBASE import allpctchanges, getmetcolname, priceslicer, alldpcmargins
from genericfunctionbot import removedupes, mmcalibrated


# GET LBSUFFIX FOR MARKETBEATER FUNC
def getlbsuffix(metricitem):
    look_backval = metricitem['look_back']
    lbsuffix = f'_LB{look_backval}'
    return lbsuffix


# PREP BENCHMATRIX FOR MARKETBEATER METRIC USE
def getbenchmatrixchangedf(benchcols):
    # pull bench pricematrix
    benchmatrixdf = readpkl('allpricematrix_bench', PRICES)
    # add daily pct change cols to matrix
    dailychangecols = []
    for item in benchcols:
        benchmatrixdf[f'dpc_{item}'] = benchmatrixdf[item].pct_change(periods=1, fill_method='ffill')
        dailychangecols.append(f'dpc_{item}')
    # delete price columns
    benchmatrixchangesdf = benchmatrixdf[['date'] + dailychangecols].copy()
    return benchmatrixchangesdf


# send summary object and paramsettings to proper metricfunction to calculate results
def metric_shell(metricitem, summary, **metricparams):
    metricfunc = metricitem['metricfunc']
    # run metric
    metricscore = metricfunc(**metricparams)
    # update summary with metric answer
    metricname = metricitem['metricname']
    if metricname == 'marketbeater':
        summary.update(metricscore)
    else:
        metcolname = getmetcolname(metricitem)
        summary.update({metcolname: metricscore})
    return summary


def allmetrics_single(slicedprices, summary, lookbackmetrics_to_run, benchmatrixchangesdf, beg_date, end_date, stock):
    # CATEGORIZE METRICS
    noprepraw_metrics = []
    dpcmargins_metrics = []
    nonzerodpcmargins_metrics = []
    nonzeroraw_metrics = []
    raw_metrics = []
    smoothraw_metrics = []
    squeezeraw_metrics = []
    noprepoldbareminraw_metrics = []
    oldbareminraw_metrics = []
    noprepbaremaxraw_metrics = []
    baremaxraw_metrics = []
    nopreptrueline_metrics = []
    trueline_metrics = []
    for metricitem in lookbackmetrics_to_run:
        metric_calib = metricitem['calibration']
        if metric_calib == 'noprepraw':
            noprepraw_metrics.append(metricitem)
        elif metric_calib == 'dpcmargins':
            dpcmargins_metrics.append(metricitem)
        elif metric_calib == 'nonzerodpcmargins':
            nonzerodpcmargins_metrics.append(metricitem)
        elif metric_calib == 'nonzeroraw':
            nonzeroraw_metrics.append(metricitem)
        elif metric_calib == 'raw':
            raw_metrics.append(metricitem)
        elif metric_calib == 'smoothraw':
            smoothraw_metrics.append(metricitem)
        elif metric_calib == 'squeezeraw':
            squeezeraw_metrics.append(metricitem)
        elif metric_calib == 'noprepoldbareminraw':
            noprepoldbareminraw_metrics.append(metricitem)
        elif metric_calib == 'oldbareminraw':
            oldbareminraw_metrics.append(metricitem)
        elif metric_calib == 'baremaxraw':
            baremaxraw_metrics.append(metricitem)
        elif metric_calib == 'noprepbaremaxraw':
            noprepbaremaxraw_metrics.append(metricitem)
        elif metric_calib == 'nopreptrueline':
            nopreptrueline_metrics.append(metricitem)
        elif metric_calib == 'trueline':
            trueline_metrics.append(metricitem)
    # GET AGE
    lastd = slicedprices.iat[-1, 0]
    firstd = slicedprices.iat[0, 0]
    age = (lastd - firstd).days
    if age > 1:
        # RUN NOPREPRAW METRICS
        for metricitem in noprepraw_metrics:
            metricname = metricitem['metricname']
            metricparams = {'prices': slicedprices, 'stock': stock, 'age': age}
            if metricname.startswith('age_'):
                metricparams = {'prices': slicedprices}
            elif metricname == 'slopescore':
                metricparams = {'prices': slicedprices, 'focuscol': stock}
            elif metricname.startswith('segbackslopescore'):
                metricparams = {'prices': slicedprices, 'focuscol': stock, 'segsback': metricitem['segsback'], 'winlen': metricitem['winlen']}
            elif metricname.startswith('resampledslopescore'):
                metricparams = {'prices': slicedprices, 'resamplefreq': metricitem['resamplefreq'], 'aggtype': metricitem['aggtype']}
            elif metricname.startswith('selectsampfreqslopescore'):
                metricparams = {'prices': slicedprices, 'freqlist': metricitem['freqlist'], 'aggtype': metricitem['aggtype'], 'agg2type': metricitem['agg2type']}
            elif metricname == 'allsampfreqslopescore':
                metricparams = {'prices': slicedprices, 'aggtype': metricitem['aggtype'], 'agg2type': metricitem['agg2type']}
            elif metricname.startswith('changeratetrend'):
                metricparams = {'prices': slicedprices, 'stock': stock, 'changewinsize': metricitem['changewinsize'], 'changetype': metricitem['changetype']}
            elif metricname.startswith('prevalencetrend'):
                metricparams = {'prices': slicedprices, 'stock': stock, 'changewinsize': metricitem['changewinsize'], 'changetype': metricitem['changetype']}
            elif metricname == 'maxdrop' or metricname == 'currentprice' or metricname == 'dollarsperday' or metricname == 'kneescore':
                metricparams = {'prices': slicedprices, 'stock': stock}
            elif metricname == 'marketbeater':
                lbsuffix = getlbsuffix(metricitem)
                metricparams = {'prices': slicedprices, 'stock': stock, 'benchcols': list(metricitem['bweights'].keys()), 'benchmatrixchangesdf': benchmatrixchangesdf, 'lbsuffix': lbsuffix}
            elif metricname == 'marketbeaterv2':
                metricparams = {'prices': slicedprices, 'stock': stock, 'bweights': metricitem['bweights'], 'benchmatrixchangesdf': benchmatrixchangesdf, 'avgtype': metricitem['avgtype'], 'usedev': metricitem['usedev']}
            elif metricname.startswith('posarea') or metricname == 'benchbeatpct':
                metricparams = {'prices': slicedprices, 'stock1': stock, 'stock2': metricitem['benchstock']}
            elif metricname.startswith('fatscore') or metricname.startswith('unifatscore'):
                idealcol = metricitem['idealcol']
                focuscol = metricitem['focuscol']
                if focuscol == 'rawprice':
                    focuscol = stock
                if idealcol == 'rawprice':
                    idealcol = stock
                if metricname.startswith('fatscore'):
                    metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol}
                else:
                    metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol, 'stat_type': metricitem['stat_type']}
            summary = metric_shell(metricitem, summary, **metricparams)

        # RUN DPCMARGIN METRICS
        if len(dpcmargins_metrics) != 0 or len(nonzerodpcmargins_metrics) != 0:
            # PREP DATA
            dpcmargins = alldpcmargins(slicedprices, stock, benchmatrixchangesdf, metricitem['benchticker'])
            if len(nonzerodpcmargins_metrics) != 0:
                posneg_dpcmargins = [item for item in dpcmargins if item != 0]
            # RUN METRICS
            for metricitem in dpcmargins_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('posnegmagratio'):
                    metricparams = {'daily_changes': dpcmargins, 'stat_type': metricitem['stat_type']}
                else:
                    metricparams = {'daily_changes': dpcmargins}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in nonzerodpcmargins_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('psegnegsegratio'):
                    metricparams = {'daily_changes': posneg_dpcmargins, 'stat_type': metricitem['stat_type']}
                else:
                    metricparams = {'daily_changes': posneg_dpcmargins}
                summary = metric_shell(metricitem, summary, **metricparams)
        # IF RAW METRICS EXIST
        if len(nonzeroraw_metrics) != 0 or len(raw_metrics) != 0:
            # PREP DATA
            raw_changes = allpctchanges(slicedprices, stock, 1)
            if len(nonzeroraw_metrics) != 0:
                posneg_samples = [item for item in raw_changes if item != 0]
            # RUN METRICS
            for metricitem in raw_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('statseglen') or metricname.startswith('seglife'):
                    metricparams = {'daily_changes': raw_changes, 'mode': metricitem['mode'], 'stat_type': metricitem['stat_type']}
                elif metricname == 'maxflatlitmus':
                    thresh_maxratio = metricitem['thresh_maxratio']
                    thresh_maxseg = metricitem['thresh_maxseg']
                    metricparams = {'daily_changes': raw_changes, 'age': age, 'thresh_maxratio': thresh_maxratio, 'thresh_maxseg': thresh_maxseg}
                elif metricname == 'flatlinescorelitmus':
                    thresh_flatscore = metricitem['thresh_flatscore']
                    thresh_meanseglen = metricitem['thresh_meanseglen']
                    metricparams = {'daily_changes': raw_changes, 'thresh_flatscore': thresh_flatscore, 'thresh_meanseglen': thresh_meanseglen}
                elif metricname.startswith('posnegscore'):
                    metricparams = {'daily_changes': raw_changes, 'avgmeth': metricitem['avgmeth'], 'devmeth': metricitem['devmeth']}
                elif metricname.startswith('posnegdpcscore'):
                    metricparams = {'daily_changes': raw_changes, 'avgmeth': metricitem['avgmeth']}
                elif metricname.startswith('posnegdevscore'):
                    metricparams = {'daily_changes': raw_changes, 'devmeth': metricitem['devmeth']}
                elif metricname.startswith('posnegprevalence'):
                    metricparams = {'daily_changes': raw_changes, 'changetype': metricitem['changetype']}
                elif metricname.startswith('posnegmag_'):
                    metricparams = {'daily_changes': raw_changes, 'changetype': metricitem['changetype'], 'stat_type': metricitem['stat_type']}
                elif metricname.startswith('posnegmagratio'):
                    metricparams = {'daily_changes': raw_changes, 'stat_type': metricitem['stat_type']}
                else:
                    metricparams = {'daily_changes': raw_changes}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in nonzeroraw_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('statseglen') or metricname.startswith('seglife'):
                    metricparams = {'daily_changes': posneg_samples, 'mode': metricitem['mode'], 'stat_type': metricitem['stat_type']}
                elif metricname.startswith('psegnegsegratio'):
                    metricparams = {'daily_changes': posneg_samples, 'stat_type': metricitem['stat_type']}
                else:
                    metricparams = {'posneg_samples': posneg_samples}
                summary = metric_shell(metricitem, summary, **metricparams)

        # IF baremax/baremin metrics exist
        if len(smoothraw_metrics) != 0 or len(squeezeraw_metrics) != 0 or len(noprepoldbareminraw_metrics) != 0 or len(oldbareminraw_metrics) != 0 or len(baremaxraw_metrics) != 0 or len(nopreptrueline_metrics) != 0 or len(trueline_metrics) != 0 or len(noprepbaremaxraw_metrics) != 0:
            # PREP HISTORY
            allprices = slicedprices[stock].tolist()
            oldbareminrawpricelist = oldbaremin_cruncher(allprices)
            slicedprices['oldbareminraw'] = np.array(oldbareminrawpricelist)
            # add baremaxcol/truelinecol
            if len(squeezeraw_metrics) != 0 or len(baremaxraw_metrics) != 0 or len(nopreptrueline_metrics) != 0 or len(trueline_metrics) != 0 or len(noprepbaremaxraw_metrics) != 0:
                baremaxrawpricelist = baremax_cruncher(allprices)
                slicedprices['baremaxraw'] = np.array(baremaxrawpricelist)
                if len(trueline_metrics) != 0 or len(nopreptrueline_metrics) != 0:
                    slicedprices['trueline'] = ((slicedprices['baremaxraw'] - slicedprices['oldbareminraw']) / 2) + slicedprices['oldbareminraw']
            if len(oldbareminraw_metrics) != 0:
                oldbareminraw_changes = allpctchanges(slicedprices, 'oldbareminraw', 1)
            if len(baremaxraw_metrics) != 0:
                baremaxraw_changes = allpctchanges(slicedprices, 'baremaxraw', 1)
            if len(trueline_metrics) != 0:
                trueline_changes = allpctchanges(slicedprices, 'trueline', 1)
            # RUN METRICS
            for metricitem in noprepoldbareminraw_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('segbackslopescore'):
                    metricparams = {'prices': slicedprices, 'focuscol': 'oldbareminraw', 'segsback': metricitem['segsback'], 'winlen': metricitem['winlen']}
                elif metricname == 'slopescore':
                    metricparams = {'prices': slicedprices, 'focuscol': 'oldbareminraw'}
                elif metricname.startswith('slopeoverloss'):
                    metricparams = {'prices': slicedprices, 'stock': stock, 'stat_type': metricitem['stat_type'], 'combtype': metricitem['combtype']}
                elif metricname.startswith('growthtoloss'):
                    metricparams = {'prices': slicedprices, 'stock': stock, 'groparams': metricitem['groparams'], 'lossparams': metricitem['lossparams'], 'combtype': metricitem['combtype']}
                elif metricname.startswith('rollgrowthtoloss'):
                    metricparams = {'prices': slicedprices, 'stock': stock, 'win_len': metricitem['win_len'], 'agg_type': metricitem['agg_type'], 'groparams': metricitem['groparams'], 'lossparams': metricitem['lossparams'], 'combtype': metricitem['combtype']}
                elif metricname.startswith('fatscore') or metricname.startswith('unifatscore'):
                    idealcol = metricitem['idealcol']
                    focuscol = metricitem['focuscol']
                    if focuscol == 'rawprice':
                        focuscol = stock
                    if idealcol == 'rawprice':
                        idealcol = stock
                    if metricname.startswith('fatscore'):
                        metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol}
                    else:
                        metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol, 'stat_type': metricitem['stat_type']}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in smoothraw_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('smooth'):
                    metricparams = {'prices': slicedprices, 'origpricecol': stock, 'uppercol': stock, 'lowercol': 'oldbareminraw', 'stat_type': metricitem['stat_type']}
                elif metricname.startswith('allpctdrop'):
                    metricparams = {'prices': slicedprices, 'uppercol': stock, 'lowercol': 'oldbareminraw', 'stat_type': metricitem['stat_type']}
                elif metricname.startswith('unis'):
                    metricparams = {'prices': slicedprices, 'uppercol': stock, 'lowercol': 'oldbareminraw', 'stat_type': metricitem['stat_type']}
                elif metricname.startswith('rollingsmooth'):
                    metricparams = {'prices': slicedprices, 'win_len': metricitem['win_len'], 'age': age, 'stat_type': metricitem['stat_type'], 'agg_type': metricitem['agg_type'], 'uppercol': stock, 'lowercol': 'oldbareminraw', 'origpricecol': stock}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in squeezeraw_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('squeeze') or metricname == 'smoothsqueeze_ratio' or metricname == 'roughnessfactor':
                    metricparams = {'prices': slicedprices, 'uppercol': 'baremaxraw', 'lowercol': 'oldbareminraw', 'origpricecol': stock, 'stat_type': metricitem['stat_type']}
                elif metricname.startswith('allpctdrop'):
                    metricparams = {'prices': slicedprices, 'uppercol': 'baremaxraw', 'lowercol': 'oldbareminraw', 'stat_type': metricitem['stat_type']}
                elif metricname.startswith('unis'):
                    metricparams = {'prices': slicedprices, 'uppercol': 'baremaxraw', 'lowercol': 'oldbareminraw', 'stat_type': metricitem['stat_type']}
                elif metricname == 'dipfinder':
                    metricparams = {'prices': slicedprices, 'uppercol': 'baremaxraw', 'lowercol': 'oldbareminraw'}
                elif metricname.startswith('rollingsqueeze'):
                    metricparams = {'prices': slicedprices, 'win_len': metricitem['win_len'], 'age': age, 'stat_type': metricitem['stat_type'], 'agg_type': metricitem['agg_type'], 'uppercol': 'baremaxraw', 'lowercol': 'oldbareminraw', 'origpricecol': stock}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in oldbareminraw_metrics:
                metricname = metricitem['metricname']
                metricparams = {'daily_changes': oldbareminraw_changes}
                if metricname.startswith('statseglen') or metricname.startswith('seglife'):
                    metricparams = {'daily_changes': oldbareminraw_changes, 'mode': metricitem['mode'], 'stat_type': metricitem['stat_type']}
                elif metricname == 'maxbmflatlitmus':
                    thresh_maxratio = metricitem['thresh_maxratio']
                    thresh_maxseg = metricitem['thresh_maxseg']
                    metricparams = {'daily_changes': oldbareminraw_changes, 'age': age, 'thresh_maxratio': thresh_maxratio, 'thresh_maxseg': thresh_maxseg}
                elif metricname == 'bmflatlinescorelitmus':
                    thresh_flatscore = metricitem['thresh_flatscore']
                    thresh_meanseglen = metricitem['thresh_meanseglen']
                    metricparams = {'daily_changes': oldbareminraw_changes, 'thresh_flatscore': thresh_flatscore, 'thresh_meanseglen': thresh_meanseglen}
                elif metricname.startswith('bigjump'):
                    metricparams = {'daily_changes': oldbareminraw_changes, 'bigjumpstrength': metricitem['bigjumpstrength']}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in noprepbaremaxraw_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('segbackslopescore'):
                    metricparams = {'prices': slicedprices, 'focuscol': 'baremaxraw', 'segsback': metricitem['segsback'], 'winlen': metricitem['winlen']}
                elif metricname == 'slopescore':
                    metricparams = {'prices': slicedprices, 'focuscol': 'baremaxraw'}
                elif metricname.startswith('reg1stats'):
                    metricparams = {'prices': slicedprices, 'stock': stock, 'stat_type': metricitem['stat_type']}
                elif metricname == 'reg1reg2ratio' or metricname == 'lastdiplen' or metricname == 'reg1pct':
                    metricparams = {'prices': slicedprices, 'stock': stock}
                elif metricname.startswith('regqualscore'):
                    metricparams = {'prices': slicedprices, 'stock': stock, 'region': metricitem['region']}
                elif metricname.startswith('fatscore') or metricname.startswith('unifatscore'):
                    idealcol = metricitem['idealcol']
                    focuscol = metricitem['focuscol']
                    if focuscol == 'rawprice':
                        focuscol = stock
                    if idealcol == 'rawprice':
                        idealcol = stock
                    if metricname.startswith('fatscore'):
                        metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol}
                    else:
                        metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol, 'stat_type': metricitem['stat_type']}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in baremaxraw_metrics:
                metricparams = {'daily_changes': baremaxraw_changes}
                metricname = metricitem['metricname']
                if metricname.startswith('statseglen') or metricname.startswith('seglife'):
                    metricparams = {'daily_changes': baremaxraw_changes, 'mode': metricitem['mode'], 'stat_type': metricitem['stat_type']}
                elif metricname == 'maxbmaxflatlitmus':
                    thresh_maxratio = metricitem['thresh_maxratio']
                    thresh_maxseg = metricitem['thresh_maxseg']
                    metricparams = {'daily_changes': baremaxraw_changes, 'age': age, 'thresh_maxratio': thresh_maxratio, 'thresh_maxseg': thresh_maxseg}
                elif metricname.startswith('bigjump'):
                    metricparams = {'daily_changes': baremaxraw_changes, 'bigjumpstrength': metricitem['bigjumpstrength']}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in nopreptrueline_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('segbackslopescore'):
                    metricparams = {'prices': slicedprices, 'focuscol': 'trueline', 'segsback': metricitem['segsback'], 'winlen': metricitem['winlen']}
                elif metricname == 'slopescore':
                    metricparams = {'prices': slicedprices, 'focuscol': 'trueline'}
                elif metricname.startswith('fatscore') or metricname.startswith('unifatscore'):
                    idealcol = metricitem['idealcol']
                    focuscol = metricitem['focuscol']
                    if focuscol == 'rawprice':
                        focuscol = stock
                    if idealcol == 'rawprice':
                        idealcol = stock
                    if metricname.startswith('fatscore'):
                        metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol}
                    else:
                        metricparams = {'prices': slicedprices, 'focuscol': focuscol, 'idealcol': idealcol, 'stat_type': metricitem['stat_type']}
                summary = metric_shell(metricitem, summary, **metricparams)
            for metricitem in trueline_metrics:
                metricname = metricitem['metricname']
                if metricname.startswith('bigjump'):
                    metricparams = {'daily_changes': trueline_changes, 'bigjumpstrength': metricitem['bigjumpstrength']}
                else:
                    metricparams = {'daily_changes': trueline_changes}
                summary = metric_shell(metricitem, summary, **metricparams)
    else:
        for metricitem in lookbackmetrics_to_run:
            if metricitem['metricname'] == 'marketbeater':
                lbsuffix = getlbsuffix(metricitem)
                allbcolresults = {}
                for bcol in list(metricitem['bweights'].keys()):
                    bcolresults = {
                        f'{bcol}_pct_pos{lbsuffix}': np.nan,
                        f'{bcol}_pct_neg{lbsuffix}': np.nan,
                        f'{bcol}_avg_pos{lbsuffix}': np.nan,
                        f'{bcol}_avg_neg{lbsuffix}': np.nan
                        }
                    allbcolresults.update(bcolresults)
                summary.update(allbcolresults)
            else:
                metcolname = getmetcolname(metricitem)
                summary.update({metcolname: np.nan})
    return summary


def lookbackshell_single(metrics_to_run, benchmatrixchangesdf, beg_date, end_date, stock):
    # GROUP BATCH ELEMENTS BY LOOKBACK
    lookback_vals = removedupes([item['look_back'] for item in metrics_to_run])
    metric_batches = [{'look_backval': look_backval, 'lookback_batch': [item for item in metrics_to_run if item['look_back'] == look_backval]} for look_backval in lookback_vals]
    # GET PRICE HISTORY
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(drop=True, inplace=True)
    # CREATE MASTER SUMMARY
    summary = {
        'stock': stock,
        'age': len(prices) - 1
        }
    # FOR EACH LOOK_BACK BATCH...
    for lookbackbatch in metric_batches:
        look_back = lookbackbatch['look_backval']
        lookbackmetrics_to_run = lookbackbatch['lookback_batch']
        # SLICE IF LOOK_BACK SETTING EXISTS
        if look_back != 0:
            slicedprices = priceslicer(prices, look_back)
        else:
            slicedprices = prices.copy()
        summary = allmetrics_single(slicedprices, summary, lookbackmetrics_to_run, benchmatrixchangesdf, beg_date, end_date, stock)
    return summary


def allmetricval_cruncher(scriptparams, beg_date, end_date, tickerlist, rankmeth, rankregime):
    # construct masterdf
    masterdf = pd.DataFrame(data={'stock': tickerlist})
    # separate winrate- from nonwinrate- metrics
    nonwinratemetrics_to_run = [metricitem for metricitem in scriptparams if metricitem['metricname'].startswith('winrateranker') is False]
    # get metric vals for all non-winrate metrics
    if len(nonwinratemetrics_to_run) != 0:
        # load marketbeater benchmarkdf if metric chosen
        benchmatrixchangesdf = ''
        for metricitem in nonwinratemetrics_to_run:
            if metricitem['metricname'].startswith('marketbeater') or metricitem['calibration'] == 'nonzerodpcmargins' or metricitem['calibration'] == 'dpcmargins':
                benchmatrixchangesdf = getbenchmatrixchangedf(list(metricitem['bweights'].keys()))
        # get metricvals
        table_results = []
        for stock in tickerlist:
            unpickled_raw = lookbackshell_single(nonwinratemetrics_to_run, benchmatrixchangesdf, beg_date, end_date, stock)
            table_results.append(unpickled_raw)
        nonwinratedf = pd.DataFrame(data=table_results)
        # append df to masterdf
        masterdf = masterdf.join(nonwinratedf.set_index('stock'), how="left", on="stock")
    # RANK DATA
    sumcols = []
    weight_total = 0
    for metricitem in scriptparams:
        # DEFINE RANK PARAMS
        metricweight = metricitem['metricweight']
        metricname = metricitem['metricname']
        metcolname = getmetcolname(metricitem)
        # IF MARKETBEATER, PREPARE RANKCOLUMN
        if metricname == 'marketbeater':
            lbsuffix = getlbsuffix(metricitem)
            mbsumcols = []
            for bcol in list(metricitem['bweights'].keys()):
                for metric in metricitem['mweights'].keys():
                    # RANK EACH COLUMN NEEDED TO BE RANKED
                    colweight = metricitem['bweights'][bcol] * metricitem['mweights'][metric]
                    mbsubjectcolname = f'{bcol}_{metric}{lbsuffix}'
                    mbrankcolname = f'RANK_{mbsubjectcolname} (w={colweight})'
                    if metric == 'pct_neg':
                        rankascend = 1
                    else:
                        rankascend = 0
                    if rankmeth == 'minmax':
                        masterdf[mbrankcolname] = mmcalibrated(masterdf[mbsubjectcolname].to_numpy(), rankascend, rankregime)
                    elif rankmeth == 'standard':
                        masterdf[mbrankcolname] = masterdf[mbsubjectcolname].rank(ascending=rankascend)
                    # GET EACH RANKCOLUMN'S WEIGHTED RANK VALUE
                    masterdf[f'w_{mbrankcolname}'] = (masterdf[mbrankcolname] * colweight)
                    # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
                    mbsumcols.append(f'w_{mbrankcolname}')
            # SUM WEIGHTED RANK VALUES TOGETHER
            masterdf[metcolname] = masterdf[mbsumcols].sum(axis=1, min_count=len(mbsumcols))
        # RANK METRIC DATA COLUMN
        rankcolname = f'RANK_{metcolname} (w={metricweight})'
        subjectcolname = metcolname
        # SET METRIC COLUMN RANK DIRECTION
        if metricname.startswith('winrateranker'):
            if metricitem['rankmeth'] == 'standard':
                rankdirection = 1
            elif metricitem['rankmeth'] == 'minmax' or metricitem['rankmeth'] == 'minmax_nan':
                if metricitem['rankregime'] == '1isbest':
                    rankdirection = 0
                elif metricitem['rankregime'] == '0isbest':
                    rankdirection = 1
        else:
            rankdirection = metricitem['rankascending']
        if rankmeth == 'minmax':
            masterdf[rankcolname] = mmcalibrated(masterdf[subjectcolname].to_numpy(), rankdirection, rankregime)
        elif rankmeth == 'standard':
            masterdf[rankcolname] = masterdf[subjectcolname].rank(ascending=rankdirection)

        # GET EACH RANKCOLUMN'S WEIGHTED RANK VALUE
        wrankcolname = f'w_{rankcolname}'
        masterdf[wrankcolname] = (masterdf[rankcolname] * metricweight)

        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wrankcolname)

        # ADD WEIGHT TO WEIGHT TOTAL
        weight_total += metricweight

    # sum weighted rankcols
    masterwrankcolname = f'MASTER WEIGHTED RANK {weight_total}'
    masterdf[masterwrankcolname] = masterdf[sumcols].sum(axis=1, min_count=len(sumcols))
    # rank overall weighted rankcol
    if rankmeth == 'minmax':
        if rankregime == '1isbest':
            finalrankascend = 0
        elif rankregime == '0isbest':
            finalrankascend = 1
    elif rankmeth == 'standard':
        finalrankascend = 1
    finalrankcolname = f'MASTER FINAL RANK as of {end_date}'
    masterdf[finalrankcolname] = masterdf[masterwrankcolname].rank(ascending=finalrankascend)
    # RE-SORT AND RE-INDEX
    masterdf.sort_values(ascending=True, by=[finalrankcolname], inplace=True)
    masterdf.reset_index(drop=True, inplace=True)
    return masterdf


# FILTER THE ALLMETRIC DF
def filterallmetrics(allmetricsdf, metrics_to_run, beg_date, end_date, rankmeth, rankregime):
    # FILTER EACH METRIC
    for metricitem in metrics_to_run:
        thresholdtype = metricitem['thresholdtype']
        filterdirection = metricitem['filterdirection']
        metcolname = getmetcolname(metricitem)
        # CAPTURE THRESHOLDS
        if filterdirection == 'above' or filterdirection == 'below' or filterdirection == 'equalabove' or filterdirection == 'equalbelow':
            threshval = metricitem['threshold']
        elif filterdirection == 'between':
            upperthresh = metricitem['upperthreshold']
            lowerthresh = metricitem['lowerthreshold']
        # DEFINE FILTER COLUMN
        if thresholdtype == 'pctrank':
            pctrankcol = f'pctrank_{metcolname}'
            filtercol = pctrankcol
        else:
            filtercol = metcolname
        # FILTER OUT STOCKS ACCORDING TO FILTER DIRECTION
        if filterdirection == 'above':
            allmetricsdf = allmetricsdf[allmetricsdf[filtercol] > threshval].copy()
        elif filterdirection == 'equalabove':
            allmetricsdf = allmetricsdf[allmetricsdf[filtercol] >= threshval].copy()
        elif filterdirection == 'below':
            allmetricsdf = allmetricsdf[allmetricsdf[filtercol] < threshval].copy()
        elif filterdirection == 'equalbelow':
            allmetricsdf = allmetricsdf[allmetricsdf[filtercol] <= threshval].copy()
        elif filterdirection == 'between':
            allmetricsdf = allmetricsdf[(allmetricsdf[filtercol] > lowerthresh) & (allmetricsdf[filtercol] < upperthresh)].copy()
        if len(allmetricsdf) == 0:
            return allmetricsdf
    return allmetricsdf
