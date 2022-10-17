"""
Title: REBOUND BASE
Date Started: Nov 12, 2020
Version: 1
Version Start: Nov 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Find stocks that have greatest promise for rebound.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from filelocations import readpkl, savetopkl, buildfolders_singlechild, buildfolders_parent_cresult_cdump
from tickerportalbot import tickerportal3
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES, daterangedb_source, tickerlistcommon_source
from growthcalcbot import get_growthdf
from STRATTEST_SINGLE_BASE_CRUNCHER import stagecruncher
from BESTSTREAK_BASE import beststreak_cruncher
from genericfunctionbot import mmcalibrated, intersectlists


# GIVEN STRAT PANEL, EXISTENCE DATE, RETURNS RESULTING STRATDF
def getstratdf(verbose, trialdir, exist_date, strat_panel, currentpool, rankmeth, rankregime):
    # for each stage in strat panel, return resulting pool
    for stagenum, stagescript in strat_panel.items():
        # build stage folders
        stageparent, stageresults, stagedump = buildfolders_parent_cresult_cdump(trialdir, f'{stagenum}_parent')
        # get stagedf
        if stagescript['scriptname'].startswith('winstreak'):
            beg_date = str(dt.date.fromisoformat(exist_date) - dt.timedelta(days=stagescript['look_back']))
            stagedf = beststreak_cruncher(verbose, beg_date, exist_date, stagescript['benchticker'], stagescript['periodlen'], stagescript['avg_type'], stagedump)
        else:
            stagedf = stagecruncher(stageresults, stagedump, stagenum, stagescript, '', exist_date, currentpool, rankmeth, rankregime)
        # get stagepool
        resultpool = stagedf['stock'].tolist()
        currentpool = resultpool
        if len(currentpool) == 0:
            print(f'Stage {stagenum}: All remaining stocks were filtered out.')
            break
    return stagedf


# returns ranking of stocks by worst loss for given time period
def rankworstloss(allexistingstocks, beg_date, end_date):
    # CALCULATE GROWTH
    if len(allexistingstocks) != 0:
        # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
        pricematrixdf = readpkl('allpricematrix_common', PRICES)
        # GET STOCK GROWTH
        sliced = get_growthdf(pricematrixdf, allexistingstocks, beg_date, end_date, True)
    else:
        print(f'No stocks existed on {beg_date}!  Program exiting now...')
        exit()
    return sliced


# COMBINE WORSTLOSS WITH QUALITY RANKS
def rebound_single_event(parentdir, global_params, custompool):
    # build subfolders for trial
    lossdump = buildfolders_singlechild(parentdir, 'worstlossdump')
    qualdump = buildfolders_singlechild(parentdir, 'qualityrankdump')
    # get startpool
    allexistingstocks = tickerportal3(global_params['eventstart'], 'common', 2)
    if custompool != []:
        allexistingstocks = intersectlists(custompool, allexistingstocks)
    # get worstloss ranking
    worstlossdf = rankworstloss(allexistingstocks, global_params['eventstart'], global_params['eventend'])
    # rename 'STOCK' column to 'stock'
    worstlossdf.rename(columns={'STOCK': 'stock'}, inplace=True)
    # save ranking
    worstlossdf.to_csv(index=False, path_or_buf=lossdump / f'worstloss_eventbeg{global_params["eventstart"]}_eventend{global_params["eventend"]}.csv')
    # set rank vars
    rankmeth = global_params['rankmeth']
    rankregime = global_params['rankregime']
    # get pre-event quality ranking
    qualityrankdf = getstratdf(global_params['verbose'], qualdump, global_params['eventstart'], global_params['qualitystratpanel'], allexistingstocks, rankmeth, rankregime)
    # create rankcols
    if rankmeth == 'minmax':
        if rankregime == '1isbest':
            worstlossrankascend = 1
        elif rankregime == '0isbest':
            worstlossrankascend = 0
        worstlossdf['rank_loss'] = mmcalibrated(worstlossdf[f'GROWTH {global_params["eventstart"]} TO {global_params["eventend"]}'].to_numpy(), worstlossrankascend, rankregime)
        finalqualcol = list(qualityrankdf.columns)[-2]
        qualityrankdf['rank_quality'] = qualityrankdf[finalqualcol]
    elif rankmeth == 'standard':
        worstlossdf['rank_loss'] = worstlossdf[f'GROWTH {global_params["eventstart"]} TO {global_params["eventend"]}'].rank(ascending=1)
        finalqualcol = list(qualityrankdf.columns)[-1]
        qualityrankdf['rank_quality'] = qualityrankdf[finalqualcol].rank(ascending=1)
    # join dfs
    worstlossdf = worstlossdf.join(qualityrankdf.set_index('stock'), how="left", on="stock")
    # get final rank
    sumcols = []
    weight_total = 0
    for (colname, colweight) in zip(['rank_loss', 'rank_quality'], [global_params['weight_loss'], global_params['weight_quality']]):
        wcolname = f'w_{colname} (w={colweight})'
        worstlossdf[wcolname] = (worstlossdf[colname] * colweight)
        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wcolname)
        # ADD WEIGHT TO WEIGHT TOTAL
        weight_total += colweight
    masterwrankcolname = f'WEIGHTED RANK w={weight_total}'
    worstlossdf[masterwrankcolname] = worstlossdf[sumcols].sum(axis=1, min_count=len(sumcols))
    # rank overall weighted rankcol
    if rankmeth == 'minmax':
        if rankregime == '1isbest':
            finalrankascend = 0
        elif rankregime == '0isbest':
            finalrankascend = 1
    elif rankmeth == 'standard':
        finalrankascend = 1
    finalrankcolname = f'FINAL REBOUND RANK eventbeg{global_params["eventstart"]}_eventend{global_params["eventend"]}'
    worstlossdf[finalrankcolname] = worstlossdf[masterwrankcolname].rank(ascending=finalrankascend)
    # RE-SORT AND RE-INDEX
    worstlossdf.sort_values(ascending=True, by=[finalrankcolname], inplace=True)
    worstlossdf.reset_index(drop=True, inplace=True)
    # ARCHIVE TO FILE
    filename = f'rebound_ranks_eventbeg{global_params["eventstart"]}_eventend{global_params["eventend"]}'
    savetopkl(filename, parentdir, worstlossdf)
    worstlossdf.to_csv(index=False, path_or_buf=parentdir / f"{filename}.csv")
    return worstlossdf
