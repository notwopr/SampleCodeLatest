from filelocations import readpkl
from UPDATEPRICEDATA_FILELOCATIONS import PRICES
from SCRATCHPAPER_GRAPHING import graphdataframe_setdatecolasindex


def graphlistoftickers(tickerlist, normalizeprice):
    # OPEN PRICE MATRIX
    pricedf = readpkl("allpricematrix_common", PRICES)
    # SLICE out other stocks and uncommon dates
    pricedf = pricedf[['date'] + tickerlist].dropna(how="any")
    # reset index
    pricedf.reset_index(inplace=True, drop=True)
    if normalizeprice == 'yes':
        # normalize
        firstp = pricedf.loc[0, tickerlist]
        pricedf[tickerlist] = (pricedf[tickerlist] - firstp) / firstp
    # graph
    graphdataframe_setdatecolasindex(pricedf)


# enter tickers you want to graph in a list
tickerlist = ['HCTI']
graphlistoftickers(tickerlist, 'no')
