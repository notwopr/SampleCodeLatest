"""
Title: STRAT TESTER SINGLE BASE CRUNCHER - ALLMETRIC VALUES
Date Started: May 15, 2020
Version: 4.00
Version Start: Dec 18, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Running several metrics on the same pool of stocks and running a weighted ranking over all metric outcomes to return an overall ranking.

VERSION NOTES
1.01: Added marketbeater method.
1.02: Added look_back options.
1.03: Split winvol and winrate into separate functions.
1.04: Shift squeeze metrics to mmbm calibration.
1.05: Switch bmflat metrics to oldbareminraw graph instead of bareminraw graph.
1.06: Remove old smooth squeeze function references.  Replaced with new optimized formulas.
2.0: Removed deprecated functions.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS
from filelocations import readpkl
from UPDATEPRICEDATA_FILELOCATIONS import PRICES
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher
from STRATTEST_FUNCBASE import allpctchanges, getmetcolname


# GET LBSUFFIX FOR MARKETBEATER FUNC
def getlbsuffix(metricitem):
    look_backval = metricitem['look_back']
    lbsuffix = f'_LB{look_backval}'
    return lbsuffix


# PREP BENCHMATRIX FOR MARKETBEATER METRIC USE
def getbenchmatrixchangedf():
    # pull bench pricematrix
    benchmatrixdf = readpkl('allpricematrix_bench', PRICES)
    # add daily pct change cols to matrix
    benchpricecols = ['^DJI', '^INX', '^IXIC']
    dailychangecols = [f'dpc_{item}' for item in benchpricecols]
    benchmatrixdf[dailychangecols] = benchmatrixdf[benchpricecols].pct_change(periods=1, fill_method='ffill')
    benchmatrixdf['dpc_average'] = benchmatrixdf[dailychangecols].mean(axis=1)
    # delete price columns
    changecols = dailychangecols + ['dpc_average']
    keepcols = ['date'] + changecols
    benchmatrixchangesdf = benchmatrixdf[keepcols].copy()
    return changecols, benchmatrixchangesdf


# send summary object and paramsettings to proper metricfunction to calculate results
def metric_shell(metricitem, summary, **metricparams):
    metricname = metricitem['metricname']
    metricfunc = metricitem['metricfunc']
    # run metric
    metricscore = metricfunc(**metricparams)
    # update summary with metric answer
    if metricname == 'marketbeater':
        summary.update(metricscore)
    else:
        metcolname = getmetcolname(metricitem)
        summary.update({metcolname: metricscore})
    return summary


def allmetrics_single(slicedprices, summary, lookbackmetrics_to_run, changecols, benchmatrixchangesdf, beg_date, end_date, stock):
    # CATEGORIZE METRICS
    noprepraw_metrics = []
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
            elif metricname.startswith('slopescore'):
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
                metricparams = {'prices': slicedprices, 'stock': stock, 'changecols': changecols, 'benchmatrixchangesdf': benchmatrixchangesdf, 'firstd': firstd, 'lbsuffix': lbsuffix}
            elif metricname == 'marketbeaterv2':
                metricparams = {'prices': slicedprices, 'stock': stock, 'changecols': changecols, 'benchmatrixchangesdf': benchmatrixchangesdf, 'firstd': firstd, 'avgtype': metricitem['avgtype'], 'w_dow': metricitem['w_dow'], 'w_snp500': metricitem['w_snp500'], 'w_nasdaq': metricitem['w_nasdaq'], 'w_average': metricitem['w_average']}
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
                for bcol in changecols:
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


# RANK METRICSDF
def rankmetricsdf(metricsdf, scriptparams):
    # RANK DATA
    sumcols = []
    weight_total = 0
    for metricitem in scriptparams:

        # DEFINE RANK PARAMS
        metricweight = metricitem['metricweight']
        rankdirection = metricitem['rankascending']
        metcolname = getmetcolname(metricitem)

        # RANK METRIC DATA COLUMN
        rankcolname = f'RANK_{metcolname} (w={metricweight})'
        subjectcolname = metcolname
        metricsdf[rankcolname] = metricsdf[subjectcolname].rank(ascending=rankdirection)

        # GET EACH RANKCOLUMN'S WEIGHTED RANK VALUE
        wrankcolname = f'w_{rankcolname}'
        metricsdf[wrankcolname] = (metricsdf[rankcolname] * metricweight)

        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wrankcolname)

        # ADD WEIGHT TO WEIGHT TOTAL
        weight_total += metricweight

    masterwrankcolname = f'WEIGHTED RANK {weight_total}'
    metricsdf[masterwrankcolname] = metricsdf[sumcols].sum(axis=1, min_count=len(sumcols))

    finalrankcolname = 'FINAL RANK'
    metricsdf[finalrankcolname] = metricsdf[masterwrankcolname].rank(ascending=1)

    # RE-SORT AND RE-INDEX
    metricsdf.sort_values(ascending=True, by=[finalrankcolname], inplace=True)
    metricsdf.reset_index(drop=True, inplace=True)
    return metricsdf
