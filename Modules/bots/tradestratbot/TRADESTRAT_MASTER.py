"""
Title: TRADE STRAT MASTER
Date Started: Dec 15, 2020
Version: 1.00
Version Start: Dec 15, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Compares end networth of custom strategy and hold strategy over specified investment period on a specific stock.
GLOSSARY:
signaltrigger: the percentage the positive probability needs to be for the prediction signal to be +.  Anything lower is assigned a -.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from TRADESTRAT_BASE import tradestrat_master

bpotysource = r'D:\BOT_DUMP\bpotybot\D20201227T1\besthalf_^IXIC_1971_to_2020.csv'

global_params = {
    'todaysdate': '2020-12-27',
    'testnumber': 40,
    'testregimename': 'tradestrat',
    'ticker': '^IXIC',
    'beg_date': '2010-01-01',
    'end_date': '2020-01-01',
    'lookbackchunks': 1,
    'potydef': '15day',
    'potylen': 15,
    'signaltrigger': 0.02,
    'taxrate': 0.0,
    'cap_start': 1000,
    'buytrigger': 0.40,  # the probability that the timechunk will be positive in growth
    'selltrigger': 0.30,
    'verbose': '',
    'bpotysource': bpotysource

}


if __name__ == '__main__':
    # run multitrials
    tradestrat_master(computerobject.bot_dump, global_params)
    playsound('C:\Windows\Media\Ring03.wav')
