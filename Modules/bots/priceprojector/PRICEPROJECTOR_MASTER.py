"""
Title: PRICE PROJECTOR - BASE
Date Started: Oct 27, 2020
Version: 1.0
Version Start: Oct 27, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Returns pricedf with projected price col.

VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#   LOCAL APPLICATION IMPORTS
from PRICEPROJECTOR_BASE import projpricecol, getprices, highlight_elbow, getprojdpc_elbow, getprojdpc_standard, getdist_to_br
from computersettings import computerobject
# projected price parameters
stock = '^IXIC'
beg_date = ''
end_date = '2007-01-01'
focuscol = 'oldbareminraw'
avgtype = 'composite'
projtype_elbow = 'slopescore'
projtype_standard = 'full'

# projdpc optimizer parameters
global_params = {
    'todaysdate': '2020-10-28',
    'testnumber': 20,
    'testregimename': 'projdpcoptimizer',
    'lbound': 0.00026,
    'ubound': 0.00028,
    'step': 0.000001
}
if __name__ == '__main__':
    # find best projdpc
    #bestprojdpc = bestprojdpc(computerobject.bot_dump, global_params, stock)

    # get standard projdpc
    projdpc_standard = getprojdpc_standard(stock, beg_date, end_date, focuscol, avgtype, projtype_standard)
    print(f'standard projected dpc: {projdpc_standard}')

    # get elbow projdpc
    projdpc_elbow = getprojdpc_elbow(stock, beg_date, end_date, focuscol, avgtype, projtype_elbow)
    print(f'elbow projected dpc: {projdpc_elbow}')

    # get prices of date range
    prices = getprices(stock, beg_date, end_date, focuscol)
    # get standard projdpc pricecol
    prices = projpricecol(prices, focuscol, projdpc_standard, 'projdpc_standard')
    # get elbow projdpc pricecol
    prices = projpricecol(prices, focuscol, projdpc_elbow, 'projdpc_elbow')
    # highlight elbow date
    prices = highlight_elbow(prices, stock, beg_date, end_date, focuscol)
    # add dist_to_br col
    prices = getdist_to_br(prices, focuscol)
    # get non-optimized projected prices
    #prices = projpricecol(prices, projdpc)
    # add optimized projprices to pricedf
    #opt_prices = getfullprices(stock, focuscol)
    #opt_prices = projpricecol(opt_prices, bestprojdpc)
    #opt_prices.rename(columns={'projprices': 'bestprojprices'}, inplace=True)
    #opt_prices = opt_prices[['date', 'bestprojprices']]
    #prices = prices.join(opt_prices.set_index('date'), how="left", on="date")

    # graph
    ax1 = plt.subplot(1, 2, 1)
    sns.lineplot(data=prices[[stock, focuscol, 'elbow', 'projdpc_elbow', 'projdpc_standard']])

    plt.subplot(1, 2, 2, sharex=ax1)
    sns.lineplot(data=prices[['dist_to_br']])
    plt.show()
