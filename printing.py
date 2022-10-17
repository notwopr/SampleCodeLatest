import pandas as pd


class Printing:
    def print_df_nicely(self, df, keep_on_one_line=False, displayallrows=None, displayallcols=None, colnamewidth=None, maxcolwidth=None):
        if displayallcols:
            pd.set_option("display.max_columns", None)
        if displayallrows:
            pd.set_option("display.max_rows", None)
        if maxcolwidth:
            pd.set_option('display.max_colwidth', maxcolwidth)
        if keep_on_one_line:
            pd.set_option('expand_frame_repr', False)
        if colnamewidth:
            df.rename(columns=lambda x: x[:colnamewidth], inplace=True)
        print(df)
