"""
Title: STRAT TEST SINGLE BASE
Date Started: Feb 23, 2022
Version: 3
Version Start: Feb 23, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Single run of strategy on date returns resulting df.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from Modules.tickerportalbot import tickerportal4
from Modules.strattester.STRATTEST_SEQUENTIAL_BASE import stagecruncher
from file_functions import buildfolders_regime_testrun


# GIVEN STRAT PANEL, EXISTENCE DATE, RETURNS RESULTING DF AND POOL
def getstratdfandpool(bp):
    # build folders
    testregimeparent, testrunparent = buildfolders_regime_testrun(bp['rootdir'], bp['testnumber'], bp['todaysdate'], bp['testregimename'])
    currentpool = tickerportal4(bp['exist_date'], bp['exist_date'], 'common', bp['minimumage'])
    for stagenum, stagescript in bp['strat_panel']['stages'].items():
        stagename = f'{stagenum}_{stagescript["scriptname"]}'
        stagedf = stagecruncher(stagenum, stagescript, '', bp['exist_date'], currentpool, bp['rankmeth'], bp['rankregime'], bp['chunksize'])
        currentpool = stagedf['stock'].tolist()
        if len(currentpool) == 0:
            print(f'Stage {stagenum}: All remaining stocks were filtered out.')
            break
    finalistfn = f"{stagename}_finalists_as_of_{bp['exist_date']}"
    stagedf.to_csv(index=False, path_or_buf=testrunparent / f"{finalistfn}.csv")
    return stagedf
