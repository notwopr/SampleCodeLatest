"""
Title: Quick Reference - QUICKGRAPH - MASTER
Date Started: Feb 26, 2019
Version: 1.3
Version Start: July 11, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Quickly graph stocklist.

VERSIONS
1.2:  Add growthrates by X period.  use geometric formula.
1.3: Reorganized functions and master script.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from QUICKREFERENCE_QUICKGRAPH_MASTERFUNCTION import runquickgraph, rankreview_sidebysidegraph
from filelocations import readpkl, readcsv
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source


# SET PRICE CALIBRATION
# calibration types are: 'rawsingle', 'raw', 'normbaremin', 'bareminraw', 'minmaxbaremin', 'squeezefactor', 'rawsqueezefactorsingle', 'oldbareminraw'
pricecalibration = 'raw'
sidebysidecustom = 'no'
# graph types: f'{focuscolname}_straightline', f'{focuscolname}_kneeline', f'{focuscolname}_dpc'
leftgraph = ['raw', 'trueline']
rightgraph = ['rawtrue']
# SET LOCATION OF STOCKLIST TO GRAPH
#resultfileloc = Path(r'D:\BOT_DUMP\strattest_singles\D20210107T3\Stage2_parent')
#resultfilename = 'Stage2_scratchparams_finalists_as_of_2020-10-01'
#resultdf = readcsv(resultfilename, resultfileloc)
#resultdf.sort_values(ascending=False, by=['drop_mag_max'], inplace=True)
#fullstocklist = resultdf[(resultdf['age'] <= 2300)]['stock'].tolist()# & (resultdf['age'] <= 360*13)]['stock'].tolist()
#fullstocklist = resultdf['stock'].tolist()

fullstocklist = [
    'ADBE',
    'WST',
    'MSFT',
    'POOL',
    'KEYS',
    'MASI',
    'CSWI',
    'CSGP'
]

# SET BENCHMARK YOU WANT TO COMPARE LIST TO
benchmark = ''# '^IXIC'

# SET DISPLAY FORMAT: IN SEQUENCE OR ALL AT ONCE
sequence = 'yes'  # yeswithbench = show bench with single stock
beg_stock_index = None  # None if you want to review all in list
end_stock_index = None  # None if you want to review all in list

# SET DATES
beg_date = ''
beg_date_type = 'youngest'
end_date = '2021-10-29'
graph_portfolio_line = 'no'

'''EXECUTE'''
runquickgraph(sidebysidecustom, leftgraph, rightgraph, sequence, beg_date, beg_date_type, fullstocklist, benchmark, beg_stock_index, end_stock_index, daterangedb_source, pricecalibration, end_date, graph_portfolio_line)
#rankreview_sidebysidegraph(fullstocklist, pricecalibration, beg_date, beg_date_type, end_date, daterangedb_source)
