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
from filelocations import readpkl
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source


# SET DATES
beg_date = ''
end_date = '2015-10-01'

# SET LOCATION OF SOURCE OF PORTFOLIO LIST
#resultfileloc = Path(r'F:\BOT_DUMP\strattest_singles\D20201029T3\Stage3_parent\resultfiles')
#resultfilename = 'Stage3_scratch_finalists_as_of_2015-10-09'
#resultdf = readpkl(resultfilename, resultfileloc)
#resultdf.sort_values(ascending=True, by=['MASTER FINAL RANK as of 2020-09-16'], inplace=True)
#fullstocklist = resultdf[(resultdf['age'] <= 2300)]['stock'].tolist()# & (resultdf['age'] <= 360*13)]['stock'].tolist()

# SET BENCHMARK YOU WANT TO COMPARE LIST TO
benchmark = '^IXIC'

# FOR EACH PORTFOLIO NAME

# PULL PORTFOLIO PRICES


'''EXECUTE'''
runquickgraph(sidebysidecustom, leftgraph, rightgraph, sequence, beg_date, beg_date_type, fullstocklist, benchmark, beg_stock_index, end_stock_index, daterangedb_source, pricecalibration, end_date, graph_portfolio_line)
#rankreview_sidebysidegraph(fullstocklist, pricecalibration, beg_date, beg_date_type, end_date, daterangedb_source)
