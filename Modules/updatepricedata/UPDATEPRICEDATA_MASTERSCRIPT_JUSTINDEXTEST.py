
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import time
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from filelocations import delete_create_folder
from UPDATEPRICEDATA_BASE_PRICEMATRIX import allprice_matrix
from UPDATEPRICEDATA_BASE import store_allprices
from UPDATEPRICEDATA_FILELOCATIONS import STOCKPRICES, tickerlistall_source, tickerlistcommon_source, PRICES

chunksize = 5
if __name__ == '__main__':

    delete_create_folder(STOCKPRICES)
    start = time.time()

    # DOWNLOAD STOCK PRICES
    store_allprices(STOCKPRICES, tickerlistall_source, "", chunksize)

    end = time.time()
    print(f'Elapsed Time for storing all stock prices (seconds): {end-start}')
    #exit()
    # TEST MATRIX SPEED
    startm = time.time()

    # create matrix
    allprice_matrix(tickerlistcommon_source, STOCKPRICES, PRICES)

    endm = time.time()
    print(f'Elapsed Time for building matrix (seconds): {endm-startm}')
