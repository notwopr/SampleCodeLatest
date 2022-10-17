"""
Title: METRIC RANKER BY CLUSTERSCORE
Date Started: Aug 14, 2020
Version: 1.00
Version Start: Aug 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given a rankdf of stocks and metrics and ranks, returns ranking of the metrics used according to how well they cluster the desired stocks from the undesired stocks.  The desired stocks could be those that beat the market for a given period for example.
VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from BACKTEST_GATHERMETHOD_FILTERANDLAYER_FUNCBASE import getmetcolname
from filelocations import savetopkl, readpkl, buildfolders_parent_cresult_cdump
from ONETIME_GETSINGLEPASSPOOL import getsinglepassdf


# converts list of stocks into their corresponding rank numbers
def stocklist_to_ranklist(stocklist, ranksource, rankcol, stockcol):
    ranklist = []
    for stock in stocklist:
        ranking = ranksource[ranksource[stockcol] == stock][rankcol].item()
        ranklist.append(ranking)
    return ranklist


# measure of amount of nonidealsamples in between ideal samples
def getclusterscore(verbose, ideal_list, nonideal_list):
    # sort list
    idealsorted = sorted(ideal_list)
    maxideal = idealsorted[-1]
    minideal = idealsorted[0]
    # calculate noninterior score
    exterior_nonideals = []
    interior_nonideals = []
    for nonideal in nonideal_list:
        if nonideal < minideal or nonideal > maxideal:
            exterior_nonideals.append(nonideal)
        else:
            interior_nonideals.append(nonideal)
    total_nonideals = len(nonideal_list)
    exteriorscore = len(exterior_nonideals) / total_nonideals
    # if interiors exist...
    if len(interior_nonideals) != 0:
        dist_to_middle = (maxideal - minideal) / 2
        if dist_to_middle != 0:
            # divide the interior samples into left and right groups
            left_interior = []
            right_interior = []
            ideal_middle = minideal + dist_to_middle
            for nonideal in interior_nonideals:
                if nonideal < ideal_middle:
                    left_interior.append(nonideal)
                else:
                    right_interior.append(nonideal)
            # calculate leftscore
            if len(left_interior) != 0:
                # closer left_interior is to minideal, the better
                left_center = np.mean(left_interior)
                left_spread = np.std(left_interior)
                leftscore = 1 - (abs(minideal - (left_center + left_spread)) / dist_to_middle)
                if verbose == 'verbose':
                    print(f'left_center {left_center}')
                    print(f'left_spread {left_spread}')
            else:
                leftscore = 1
            # calculate rightscore
            if len(right_interior) != 0:
                # closer right_interior is to maxideal, the better
                right_center = np.mean(right_interior)
                right_spread = np.std(right_interior)
                rightscore = 1 - (abs(maxideal - (right_center - right_spread)) / dist_to_middle)
                if verbose == 'verbose':
                    print(f'right_center {right_center}')
                    print(f'right_spread {right_spread}')
            else:
                rightscore = 1
            left_weight = len(left_interior) / len(interior_nonideals)
            right_weight = len(right_interior) / len(interior_nonideals)
            interiorscore = (leftscore * left_weight) + (rightscore * right_weight)
            if verbose == 'verbose':
                print(f'leftscore {leftscore}')
                print(f'rightscore {rightscore}')
                print(f'dist_to_middle {dist_to_middle}')
                print(f'ideal_middle {ideal_middle}')
                print(f'left_interior {left_interior}')
                print(f'right_interior {right_interior}')
                print(f'left_weight {left_weight}')
                print(f'right_weight {right_weight}')
        else:
            interiorscore = 1
    else:
        interiorscore = 0
    # calculate clusterscore
    clusterscore = exteriorscore + interiorscore * (len(interior_nonideals) / total_nonideals) * 0.90
    if verbose == 'verbose':
        print(f'idealsorted {idealsorted}')
        print(f'nonideal_list {nonideal_list}')
        print(f'maxideal {maxideal}')
        print(f'minideal {minideal}')
        print(f'exterior_nonideals {exterior_nonideals}')
        print(f'interior_nonideals {interior_nonideals}')
        print(f'total_nonideals {total_nonideals}')
        print(f'exteriorscore {exteriorscore}')
        print(f'interiorscore {interiorscore}')
        print(f'clusterscore {clusterscore}')
    return clusterscore


# return dataframe of metrics ranked by how well ideal stocks are clustered together
def clusterscoreranking(ranksourcegenerate, verbose, destfolder, metricparamobject, idealstocklist, nonidealstocklist, ranksourceloc, ranksourcefilename, customname, exist_date):
    # isolate metriclist
    metricbatch = metricparamobject[0]['method_specific_params']['fnlbatches'][0]
    metrics_to_run = metricbatch['batch']
    if ranksourcegenerate == 'yes':
        # GENERATE RANKSOURCE
        # build ranksource folders
        ranksourceparent, ranksourceresults, ranksourcedump = buildfolders_parent_cresult_cdump(destfolder, 'ranksource_dump')
        ranksourcepool = idealstocklist + nonidealstocklist
        ranksource = getsinglepassdf(metricparamobject, ranksourceresults, ranksourcedump, '', exist_date, ranksourcepool)
    else:
        # isolate ranksource
        ranksource = readpkl(ranksourcefilename, ranksourceloc)
    # for each metric, get clusterscore
    clustersummaries = []
    for metricitem in metrics_to_run:
        # get rankcolname
        metcolname = getmetcolname(metricitem)
        weight = metricitem['metricweight']
        # get ranklists
        rankcolname = f'RANK_{metcolname} (w={weight})'
        idealranklist = stocklist_to_ranklist(idealstocklist, ranksource, rankcolname, 'stock')
        nonidealranklist = stocklist_to_ranklist(nonidealstocklist, ranksource, rankcolname, 'stock')
        # get clusterscore for that metric
        clusterscore = getclusterscore(verbose, idealranklist, nonidealranklist)
        # create and append summary
        metricsumm = {'metric': metcolname, 'clusterscore': clusterscore}
        clustersummaries.append(metricsumm)
    # create dataframe of summaries
    clusterdf = pd.DataFrame(data=clustersummaries)
    # sort
    clusterdf['metricrank'] = clusterdf['clusterscore'].rank(ascending=0)
    # re-sort and re-index
    clusterdf.sort_values(ascending=True, by=['metricrank'], inplace=True)
    clusterdf.reset_index(drop=True, inplace=True)
    # archive to file
    filename = f"clusterscoreranks_{customname}"
    savetopkl(filename, destfolder, clusterdf)
    clusterdf.to_csv(index=False, path_or_buf=destfolder / f"{filename}.csv")
    return clusterdf
