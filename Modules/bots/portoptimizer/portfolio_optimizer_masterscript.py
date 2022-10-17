"""
Title: Portfolio Optimizer - Master Script
Date Started: May 20, 2020
Version: 1.01
Vers Start Date: May 22, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Calculates the marginal increase in growth rate against marginal increase in volatility for an additional stock added to a portfolio.
    The portfolio_optimizer_ranker function returns a ranked list of the stocks in the portfolio given that best increase growth while minimizing increases in volatility.
    portfolio_optimizer calculates change in growth per change in volatility of each additional stock in a given portfolio over a shared date range

Version Notes:
1.01: Multiprocessor version.
"""

# IMPORT TOOLS
#   Standard library imports
from pathlib import Path
#   Third party imports
#   Local application imports
from PORTFOLIO_OPTIMIZER import portfolio_optimizer, portfolio_optimizer_allpermutations, candidate_challenger
from computersettings import computerobject
from genericfunctionbot import removedupes
from filelocations import buildfolders_regime_testrun, buildfolders_parent_cresult_cdump, readpkl

# SET BASE PORTFOLIO
stocklist = [
    'PLMR',
    'TEAM',
    'FRHC',
    'SITM',
    'TSLA'
]
# DEFINE CANDIDATE LIST
#candidatefolder = Path(r'F:\BOT_DUMP\ONETIMETESTS\fnlmethod\D20200613T3\rankfiles')
#candidatesourcefilename = '1_1_filterandlayer_finalists_as_of_2019-06-01'
#candidatedf = readpkl(candidatesourcefilename, candidatefolder)
#candidatelist = candidatedf['stock'].tolist()
#candidatelist = removedupes(candidatelist)
#candidatelist = [item for item in candidatelist if item not in stocklist]

# SET DATE RANGE
beg_date = ''
end_date = '2020-09-16'

# which volmethod to use: dailyvolscore_single ('old') or unifatshell regime?
volmeth = 'new'

# PLOT RESULTS?
plot = 'no'

# SET TRIAL PARAMS
todaysdate = '2020-10-11'
testnumber = 9

# SET TEST REGIME NAME
testregimename = 'portoptimizer'


if __name__ == '__main__':
    # RETURNS SORTED DATAFRAME OF STOCKS AND HOW ITS ADDITION TO THE PORTFOLIO CHANGES OVERALL GROWTH AND VOLATILITY OF THE PORTFOLIO GIVEN A PORTFOLIO AND DATE RANGE
    #print(portfolio_optimizer(plot, beg_date, end_date, stocklist, volmeth))
    # RETURNS RANKED LIST OF STOCKS IN GIVEN PORTFOLIO THAT BEST INCREASE PORTFOLIO GROWTH WHILE DECREASING VOLATILITY PERMUTATION VERSION
    testregimeparent = computerobject.bot_dump
    # BUILD TESTREGIME PARENT AND TESTRUN PARENT FOLDERS
    testregimeparent, testrunparent = buildfolders_regime_testrun(testregimeparent, testnumber, todaysdate, testregimename)
    # BUILD FIRSTPASS DUMP FOLDERS
    portoptrankerparent, portoptrankerresults, portoptrankerdump = buildfolders_parent_cresult_cdump(testrunparent, 'portoptimizer_ranker')
    portfolio_optimizer_allpermutations(plot, portoptrankerdump, portoptrankerresults, beg_date, end_date, volmeth, stocklist)
    # TAKES BASE PORTFOLIO, replaces worst with one from candidates, repeat
    #candidate_challenger(plot, testrunparent, stocklist, candidatelist, beg_date, end_date, volmeth)
