# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from newbacktest.multiprocessor import MultiProcessor


class DataFrameOperations:

    def filtered_double(self, df, filtertype, lowerbound, upperbound, targetcol):
        '''double bounded filtering df'''
        if filtertype == '>=<=':
            return df[(df[targetcol] >= lowerbound) & (df[targetcol] <= upperbound)]
        elif filtertype == '>=<':
            return df[(df[targetcol] >= lowerbound) & (df[targetcol] < upperbound)]
        elif filtertype == '><=':
            return df[(df[targetcol] > lowerbound) & (df[targetcol] <= upperbound)]
        elif filtertype == '><':
            return df[(df[targetcol] > lowerbound) & (df[targetcol] < upperbound)]

    def filtered_single(self, df, filtertype, bound, targetcol):
        '''single bounded filtering df'''
        if filtertype == '>':
            return df[df[targetcol] > bound]
        elif filtertype == '>=':
            return df[df[targetcol] >= bound]
        elif filtertype == '<':
            return df[df[targetcol] < bound]
        elif filtertype == '<=':
            return df[df[targetcol] <= bound]

    def filter_column(self, df, listofcols):
        return df[listofcols]

    def filter_bycolandrow_single(self, df, filtertype, bound, targetcol, listofcols):
        return self.filter_column(self.filtered_single(df, filtertype, bound, targetcol), listofcols)

    def filter_bycolandrow_double(self, df, filtertype, lowerbound, upperbound, targetcol, listofcols):
        return self.filter_column(self.filtered_double(df, filtertype, lowerbound, upperbound, targetcol), listofcols)

    # sets df's chosen column as the index
    def dfindexcolprep(self, colname, df):
        df.set_index(colname, inplace=True)
        return df

    # joins multiple dataframes in a list together that share a column
    def join_matrices(self, sharedcolname, lofdfs):
        resultlist = [self.dfindexcolprep(sharedcolname, d) for d in lofdfs]
        # join all stock dfs together
        mdf = pd.concat(resultlist, ignore_index=False, axis=1)
        # sort by shared col
        mdf.sort_values(by=sharedcolname, inplace=True)
        # add index col and reinstate shared col
        mdf.reset_index(inplace=True)
        mdf.rename(columns={'index': sharedcolname}, inplace=True)
        return mdf
