"""
Title: Quickref - Portfolio Volatility - Master
Date Started: Nov 10, 2021
Version: 1
Version Start: Nov 10, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Calculates the volatility of a given portfolio against a given benchmark for a given date range.

VERSIONS:
1:  I compared two methods for finding dropscores of a portfolio of stocks.  First method was by getting the dropscores of each stock separately, then averaging them.  The other method was normalizing all price curves, then getting a composite price curve, and then getting the dropscore on that curve.  Running both methods on a benchmark like NASDAQ, returned the same result.  However, when run on a portfolio of different stocks, it returned two different values.  I am inclined to go with the second method as the more accurate one.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from QUICKREF_PORTVOLATILITY_BASE import get_portpricecurve
from SCRATCHPAPER_GRAPHING import graphdataframe_line
from STRATTEST_FUNCBASE_MMBM import dropscore_single


# SET PORTFOLIO
portfolio = ['CARR', 'TT']

# DO YOU WANT TO COMPARE IT AGAINST A BENCHMARK?
benchticker = '^IXIC'

# SET DATE RANGE IF ANY
beg_date = '2020-04-01'
end_date = '2021-10-15'

if __name__ == '__main__':
    # get price curve for portfolio
    pricedf = get_portpricecurve(portfolio, beg_date, end_date)
    # print dropscore for port price curve
    print(dropscore_single(pricedf, 'baremaxraw', 'portprices', 'avg'))
    # add drops data to joint df for comparison against benchmark
    jointdf = pricedf[['date', 'drops']].copy()
    # graph data
    graphdataframe_line('date', pricedf)
    # get price curve for benchmark
    pricedf = get_portpricecurve(['^IXIC'], beg_date, end_date)
    # get dropscore for benchmark
    print(dropscore_single(pricedf, 'baremaxraw', 'portprices', 'avg'))
    # add benchmark drop data to joint df
    jointdf['drops_bench'] = pricedf['drops'].copy()
    # graph benchmark
    #graphdataframe_setdatecolasindex(pricedf)
    graphdataframe_line('date', pricedf)
    # graph drop comparison
    #graphdataframe_setdatecolasindex(jointdf)
    graphdataframe_line('date', jointdf)
