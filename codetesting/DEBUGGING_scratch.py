
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import time
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from filelocations import delete_create_folder, readpkl, readpkl_fullpath
from UPDATEPRICEDATA_BASE_PRICEMATRIX import allprice_matrix
from UPDATEPRICEDATA_BASE import store_allprices
from UPDATEPRICEDATA_FILELOCATIONS import STOCKPRICES, tickerlistall_source, tickerlistcommon_source, PRICES, INDEXPRICES
import pandas as pd
import pickle as pkl
from computersettings import computerobject
chunksize = 5
if __name__ == '__main__':

    targetfolder = computerobject.bot_dump / 'complement_bot' / 'D20211031T7' / 'summaries'
    start = time.time()

    # construct metricsdf
    table_results = []
    for child in targetfolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
        table_results.append(unpickled_raw)
    resultdf = pd.DataFrame(data=table_results)
    end = time.time()
    print(resultdf)
    print(f'Elapsed Time for regular assembly (seconds): {end-start}')
    #reset for next trial
    table_results = []
    # TEST MATRIX SPEED
    startm = time.time()

    # ASSEMBLE DATA
    table_results = [readpkl_fullpath(child) for child in targetfolder.iterdir()]
    complementdf = pd.DataFrame(data=table_results)

    endm = time.time()
    print(resultdf)
    print(f'Elapsed Time for assembly via list comprehension (seconds): {endm-startm}')
