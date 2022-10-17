"""
Title: Manual Review Script
Date Started: Nov 5, 2020
Version: 1.0
Version Start Date: Nov 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Record portfolios from final analysis csv.
VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from STOCKLIBRARY_FUNCTIONS import save_stocklist, viewstocklist, constructportlib


def recordportfolios(stratname, existdate, rankascend, rankbatchsize, sourcepath, stocklistdest, archivedest):
    # pull up rankings csv
    rankingsdf = pd.read_csv(sourcepath)
    # get list of colnames to iterate
    itercols = rankingsdf.columns[1:].tolist()
    # for each rankcol:
    for rankcol in itercols:
        # sort by that column
        rankingsdf.sort_values(ascending=rankascend, by=[rankcol], inplace=True)
        # isolate stocklist
        stocklist = rankingsdf['stock'].tolist()[:rankbatchsize]
        # save stocklist
        listname = f'{stratname}_{existdate}_{rankcol}rank_top{rankbatchsize}'
        save_stocklist(listname, stocklistdest, stocklist)
        viewstocklist(listname, stocklistdest)
    # update portfolio csv library
    constructportlib(stocklistdest, archivedest)
