"""
Title: Best Part of the Year (BPOTY) Bot Master Script
Date Started: Nov 4, 2019
Version: 3.0
Version Start Date: Dec 15, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Define a timechunk (week, month, custom), and rank each such part over a given range of years to find how well each time chunk does in a random year.
Versions:
3: Allow for single tickers to be examined instead of pooltypes.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from BPOTYBOT_BASE import get_poty_average

globalparams = {
    # DEFINE 'PART OF THE YEAR'
    'potydef': 'half',
    'potylen': 20,
    # SET DATE AND TEST NUMBER
    'todaysdate': '2020-12-27',
    'testnumber': 3,
    # SET TEST REGIME NAME
    'testregimename': 'bpotybot',
    # PICK TIME PERIOD
    'beg_date': '',
    'end_date': '',
    # DETERMINE POOL OF STOCKS TO SAMPLE FOR EACH POTY AVERAGE GROWTH
    'ticker': '^IXIC',
    # VERBOSE PRINTING
    'verbose': 'verbose'
}


if __name__ == '__main__':
    '''GET GROWTH RATES FOR EVERY TIMECHUNK OF EVERY TEST YEAR'''
    get_poty_average(globalparams)
    playsound('C:\Windows\Media\Ring03.wav')
