"""
Title: TWO SIGMA FORMATTER
Date Started: Sept 7, 2021
Version: 1
Version Start: Sept 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Once you have created all stock rankings, then run this on that parent folder.  Used to format CSV files to fit 2 Sigma's requirements and view performance.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from QUICKREF_HADYOUHAD_BASE import hadyouhadinvested, getrawbenchrate


# given dates, rank range, beginning capital, beginning benchcapital, returns endcapital benchendcapital, and periodsummary
def createperiodsummary(resultdf, allinvestdates, testind, rankstart, rankend, endcapital, benchendcapital, benchmark, savetimesheet, allperiodsummaries):
    fullstocklist = resultdf['stock'].tolist()
    # get rank batch
    portfolio = fullstocklist[rankstart:rankend]
    # set dates
    enterdate = allinvestdates[testind]
    exitdate = allinvestdates[testind+1]
    # print performance report
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    endcapital = hadyouhadinvested(endcapital, enterdate, exitdate, portfolio, benchmark)

    # calc benchendcapital
    rawbenchrate = getrawbenchrate(enterdate, exitdate, benchmark)
    benchendcapital = round(benchendcapital * (1 + rawbenchrate), 2)
    # record if requested
    if savetimesheet == 'yes':
        periodsummary = {
            'holdingperiod': testind + 1,
            'enterdate': enterdate,
            'exitdate': exitdate,
            'portfolio': portfolio
        }
        # append summary to all summaries object
        allperiodsummaries.append(periodsummary)
    return allperiodsummaries, endcapital, benchendcapital
