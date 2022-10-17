"""
Title: Update Data Bot - Price Matrix Download
Date Started: Dec 11, 2020
Version: 1
Version Date: Dec 11, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Create PRice Matrix Files Only.

Versions:

"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
import os
#   THIRD PARTY IMPORTS
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from UPDATEPRICEDATA_BASE_PRICEMATRIX import allprice_matrix
from UPDATEPRICEDATA_FILELOCATIONS import STOCKPRICES, INDEXPRICES, tickerlistcommon_source, PRICES

if __name__ == '__main__':

    '''CREATE PRICE HISTORY MATRIX (DEPENDENT ON STOCK PRICE DOWNLOAD)'''
    #allprice_matrix(tickerlistall_source, STOCKPRICES, PRICES)
    allprice_matrix(tickerlistcommon_source, STOCKPRICES, PRICES)
    #allprice_matrix('faang', STOCKPRICES, PRICES)
    allprice_matrix('bench', INDEXPRICES, PRICES)
    playsound('C:\Windows\Media\Ring03.wav')
