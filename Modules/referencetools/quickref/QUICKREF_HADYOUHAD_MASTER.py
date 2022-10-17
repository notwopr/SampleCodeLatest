"""
Title: Quick Reference - HAD YOU HAD
Date Started: Aug 13, 2021
Version: 1
Version Start: Aug 13, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Quickly give you a summary of portfolio performance.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from QUICKREF_HADYOUHAD_BASE import hadyouhadinvested
from UPDATEPRICEDATA_MASTERSCRIPT import daterangedb_source
from QUICKREFERENCE_QUICKGRAPH_MASTERFUNCTION import runquickgraph

# SET PORTFOLIO
targetportfolio = [
    'ASO',
    'CARR',
    'CDW',
    'CMBM',
    'CRSR',
    'NET',
    'OKTA',
    'RXT'
]

# SET BENCHMARK YOU WANT TO COMPARE
benchmark = '^IXIC'

# SET TIME PERIOD TO TEST
beg_date = '2021-05-01'
end_date = '2021-08-12'

# SET STARTING CAPITAL
startcapital = 100000

if __name__ == '__main__':
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    hadyouhadinvested(startcapital, beg_date, end_date, targetportfolio, benchmark)
    # GRAPH RESULTS
    pricecalibration = 'raw'
    sidebysidecustom = 'no'
    leftgraph = ['raw', 'trueline']
    rightgraph = ['rawtrue']
    sequence = 'no'
    runquickgraph('no', ['raw'], ['raw'], 'no', beg_date, 'fixed', targetportfolio, benchmark, None, None, daterangedb_source, pricecalibration, end_date, 'yes')
    playsound('C:\Windows\Media\Ring03.wav')
