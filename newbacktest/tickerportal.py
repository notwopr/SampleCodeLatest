# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl_fullpath
from file_hierarchy import DirPaths, FileNames
from file_functions import join_str


class TickerPortal:

    def get_tickerlist(self, mode):
        '''
        returns list of ticker symbols given mode
        MODES:
        'common' = all common shares of NYSE and NASDAQ US
        'all' = all shares on NYSE and NASDAQ US
        'bench' = DOW, S&P500, and NASDAQ indices
        'common+bench' = 'common' and 'bench'
        'all+bench' = 'all' and 'bench'
        '''
        b = ["^DJI", "^INX", "^IXIC"]
        if mode == 'bench':
            return b
        if mode == 'common+bench' or mode == 'all+bench':
            mode = mode[:-6]
        else:
            b = []
        sourcepath = Path(join_str([DirPaths().tickers, f'tickerlist_{mode}.pkl']))
        return b + readpkl_fullpath(sourcepath)['symbol'].tolist()

    def tickers_possible(self, date_left, date_right):
        '''returns the first and last date dataframe filtered by a given date constraint (optional).  The dataframe contains the first and last dates of all NYSE and NASDAQ US tickers plus Dow S&P500 and NASDAQ indices'''
        sourcepath = Path(f'{join_str([DirPaths().date_results, FileNames().fn_daterangedb])}.pkl')
        all_startdates = readpkl_fullpath(sourcepath)
        if date_left and date_right:
            return all_startdates[(all_startdates['first_date'] <= date_left) & (all_startdates['last_date'] >= date_right)]
        if date_left:
            return all_startdates[all_startdates['first_date'] <= date_left]
        if date_right:
            return all_startdates[all_startdates['last_date'] >= date_right]
        return all_startdates

    def existing_tickers(self, date, pool):
        '''
        returns a list of all the tickers that existed on a given date out of a given pool
        '''
        pool = pool if type(pool) == list else self.get_tickerlist(pool)
        valid_rows = self.tickers_possible(date, date)
        return valid_rows[valid_rows['stock'].isin(pool)]['stock'].tolist()
