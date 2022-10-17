from Modules.price_history import grabsinglehistory
from file_functions import readpkl, readpkl_fullpath
from file_hierarchy import tickerlistall_name, TICKERS, PRICES, pricematrix_common_name, STOCKPRICES
from Modules.codetesting.Debuggingbot import runtime_logger
from Modules.updatepricedata.UPDATEPRICEDATA_BASE_PRICEMATRIX import allprice_matrix_modin, allprice_matrix2, allprice_matrix
import time
#pd.set_option("display.max_rows", None, "display.max_columns", None)
# get list of tickers
#alltickers = readpkl(tickerlistcommon_name, TICKERS)['symbol'].tolist()

tlname = tickerlistall_name
tickerlistfolder = TICKERS
pricedatafolder = STOCKPRICES
destfolder = ''
if __name__ == "__main__":
    # regular Version
    name = 'orig'
    start = time.time()
    odf = allprice_matrix(tlname, tickerlistfolder, pricedatafolder, destfolder)
    end = time.time()
    print(f'Method: {name}')
    print(f'elapsed: {end-start} secs')
    #print(matrixmethdf)

    # updated Version
    # modin version
    name = 'updated'
    start = time.time()
    df = allprice_matrix2(tlname, tickerlistfolder, pricedatafolder, destfolder)
    end = time.time()
    print(f'Method: {name}')
    print(f'elapsed: {end-start} secs')
    #print(matrixmethdf)

    # check if alternate method produced identical results
    if odf.equals(df) is False:
        print('WARNING: RESULTING DFs did not match!!')

    # updated Version
    # modin version
    name = 'modin'
    start = time.time()
    df = allprice_matrix_modin(tlname, tickerlistfolder, pricedatafolder, destfolder)
    end = time.time()
    print(f'Method: {name}')
    print(f'elapsed: {end-start} secs')
    #print(matrixmethdf)

    # check if alternate method produced identical results
    if odf.equals(df) is False:
        print('WARNING: RESULTING DFs did not match!!')
