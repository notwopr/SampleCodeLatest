# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl
from file_hierarchy import DirPaths
from newbacktest.dataframe_operations import DataFrameOperations
'''
Rather than take the entire pricematrix of all stocks in a single dataframe and filter from there, this approach pulls individual stocks as requested, and gives the option of combining them together if needed.
'''


class DataSourceSingle:

    def eodprices_single_raw(self, ticker):
        if ticker in ['^DJI', '^INX', '^IXIC']:
            subdir = DirPaths().eodprices_index
            ticker = ticker[1:]
        else:
            subdir = DirPaths().eodprices_stock
        return readpkl(f"{ticker}_prices", Path(subdir))

    def _add_filler_dates(self, df):
        df.set_index('date', inplace=True)
        df = df.reindex(pd.date_range(df.index[0], df.index[-1]))
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'date'}, inplace=True)
        return df

    def eodprices_single_no_ffill(self, ticker):
        return self._add_filler_dates(self.eodprices_single_raw(ticker))

    def eodprices_single_ffill(self, ticker):
        df = self.eodprices_single_no_ffill(ticker)
        df.ffill(inplace=True)
        return df

    def eodprices_multi_raw(self, tickers):
        '''gets individual dfs then joins them together; no filler dates'''
        lofdfs = [self.eodprices_single_raw(t) for t in tickers]
        return DataFrameOperations().join_matrices('date', lofdfs)

    def eodprices_multi_no_ffill(self, tickers):
        '''gets individual dfs then joins them together dates filled but no forward fill'''
        lofdfs = [self.eodprices_single_no_ffill(t) for t in tickers]
        return DataFrameOperations().join_matrices('date', lofdfs)

    def eodprices_multi_ffill(self, tickers):
        '''gets individual dfs then joins them together, then forward fill then drop all NaN rows'''
        lofdfs = [self.eodprices_single_ffill(t) for t in tickers]
        df = DataFrameOperations().join_matrices('date', lofdfs)
        df.dropna(inplace=True, how='all', subset=tickers)
        return df
