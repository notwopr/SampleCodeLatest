"""
Title: GET SLOPESCORE AVERAGE OF EACH LETTER
Date Started: Dec 28, 2020
Version: 1.00
Version Start: Dec 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Returns aggregate slopescore data by Starting Letter of a stock's name.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from BESTLETTER_BASE import masterbestletter


global_params = {
    'rootdir': computerobject.bot_dump,
    'todaysdate': '2020-12-28',
    'testnumber': 4,
    'testregimename': 'bestletterbot',
    'presentdate': '2020-12-23'
}

if __name__ == '__main__':
    # run multitrials
    masterbestletter(global_params)
    playsound('C:\Windows\Media\Ring03.wav')
