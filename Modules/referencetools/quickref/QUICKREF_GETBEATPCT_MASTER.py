"""
Title: GET BEATPCT BOT MASTER
Date Started: Dec 12, 2020
Version: 1.00
Version Start: Dec 12, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given list of stocks and a benchmark and investment period, return the list with their beatpct against the benchmark. Beatpct is the proportion of days the stock's normalized graph exceeded the benchmark's.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from QUICKREF_GETBEATPCT_BASE import getbeatpct


global_params = {
    'portfolio': [
            'NET',
            'RXT',
            'SITM',
            'ASO',
            'OKTA',
            'CDW',
            'ARVL',
            'CRSR',
            'CMBM',
            'CARR'
        ],
    'investstart': '2021-01-01',
    'investend': '2021-08-12',
    'benchticker': '^IXIC',
    'verbose': 'verbose'
}


if __name__ == '__main__':
    getbeatpct(global_params)
    playsound('C:\Windows\Media\Ring03.wav')
