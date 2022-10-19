# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl_fullpath, join_str
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
        # 'eodprices_commonplusbench': [DirPaths().eodprices, f"{FileNames().fn_pricematrix_commonplusbench}.pkl"],
        'fundies': [None, None],
        'marketcap': [None, None]
    }

    def opends(self, datasourcetype):
        if datasourcetype == 'eodprices' or datasourcetype == 'eodprices_bench':
            return readpkl_fullpath(Path(join_str(self._sourcelocs[datasourcetype])))
        elif datasourcetype == 'eodprices_commonplusbench':
            stockdf = readpkl_fullpath(Path(join_str(self._sourcelocs['eodprices'])))
            benchdf = readpkl_fullpath(Path(join_str(self._sourcelocs['eodprices_bench'])))
            return DataFrameOperations().join_matrices('date', [benchdf, stockdf])
