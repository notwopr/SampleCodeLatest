# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl_fullpath, join_str, savetopkl_fullpath
from file_hierarchy import DirPaths, FileNames
from newbacktest.dataframe_operations import DataFrameOperations


class DataSource:
    '''
    Use this to access data sources such as company fundamentals, marketcap histories, price histories.
    This class assumes the data source is a dataframe data type.
    '''
    _sourcelocs = {
        'eodprices': [DirPaths().eodprices, f"{FileNames().fn_pricematrix_common}.pkl"],
        'eodprices_bench': [DirPaths().eodprices, f"{FileNames().fn_pricematrix_bench}.pkl"],
        'eodprices_commonplusbench': [DirPaths().eodprices, f"{FileNames().fn_pricematrix_commonplusbench}.pkl"],
        'fundies': [None, None],
        'marketcap': [None, None]
    }

    def opends(self, datasourcetype):
        return readpkl_fullpath(Path(join_str(self._sourcelocs[datasourcetype])))

    def eodprices_tickers_noffill(self, tickers):
        '''takes full pricematrix of all tickers including bench, and removes unwanted ticker columns. It keeps all dates however.  As a result, you may have rows that are just full of NaNs'''
        return DataFrameOperations().filter_column(self.opends('eodprices_commonplusbench'), ['date']+tickers).copy()

    def eodprices_tickers_ffill(self, tickers):
        '''this not only filters out unwanted ticker columns, it forward fills nans and removes rows where none of the remaining tickers have data.'''
        df = self.eodprices_tickers_noffill(tickers)
        df.ffill(inplace=True)
        df.dropna(inplace=True, how='all', subset=tickers)
        return df
