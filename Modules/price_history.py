"""
Title: All Price Bot
Date Started: June 7, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the All Price Bot is to retrieve the entire price history of a stock.  It will return all days including non-trading days (filled in with previous last closing price).  Allows for the option to fill in the unavailable rows with Nan or the last available price.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_hierarchy import DirPaths, FileNames
from file_functions import readpkl


# GRAB RAW PRICE HISTORY OF A STOCK (INCLUDES ONLY DAYS IT WAS TRADED)
def grabsinglehistory(symbol):
    # SYNTAX CORRECTION
    if symbol in ["^DJI", "^INX", "^IXIC"]:
        symbol = symbol[1:]
        targetfolder = Path(DirPaths().eodprices_index)
    else:
        targetfolder = Path(DirPaths().eodprices_stock)
    prices = readpkl(f"{symbol}_prices", targetfolder)
    return prices


# same but take from matrix file
def grabsinglehistory_matrixvers(stock):
    # open matrix
    testpm = readpkl(FileNames().fn_pricematrix_common, Path(DirPaths().eodprices))
    # slice out date and stockcol and remove Nans
    df = testpm[['date', stock]].dropna()
    df.reset_index(inplace=True, drop=True)
    # convert date format from pandas timestamp to pydate
    df['date'] = df['date'].dt.to_pydatetime()
    df['date'] = df['date'].apply(lambda x: x.date())
    return df


# GRAB SINGLE STOCK/INDEX PRICE HISTORY DATAFRAME
def grabsinglehistory_fundies(symbol, datatype):
    if datatype == 'marketcap':
        targetfolder = Path(DirPaths().marketcap)
        filescheme = f"{symbol}_marketcaps"
    elif datatype == 'fundies':
        targetfolder = Path(DirPaths().fundies)
        filescheme = f"{symbol}_fundies"
    datadf = readpkl(filescheme, targetfolder)
    return datadf
