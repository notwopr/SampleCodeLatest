import pandas as pd


class DataTableOperations:
    # sort table
    def sort_datatable(self, sortinput, targetdf):
        if len(sortinput):
            return targetdf.sort_values(
                by=sortinput[0]['column_id'],
                ascending=sortinput[0]['direction'] == 'asc',
                inplace=False
                )
        else:
            return targetdf

    def return_sortedtable(self, sort_by, callback_context, finalchart, source):
        if finalchart and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
            df = pd.DataFrame.from_records(finalchart)
            finalchartdf = self.sort_datatable(sort_by, df)
        elif finalchart or source:
            finalchartdf = pd.DataFrame.from_records(source)
        else:
            finalchartdf = pd.DataFrame(data=[])
        return finalchartdf

    def _table_type(self, df_column):
        if isinstance(df_column.dtype, pd.DatetimeTZDtype):
            return 'datetime',
        elif (isinstance(df_column.dtype, pd.StringDtype) or
                isinstance(df_column.dtype, pd.BooleanDtype) or
                isinstance(df_column.dtype, pd.CategoricalDtype) or
                isinstance(df_column.dtype, pd.PeriodDtype)):
            return 'text'
        elif (isinstance(df_column.dtype, pd.SparseDtype) or
                isinstance(df_column.dtype, pd.IntervalDtype) or
                isinstance(df_column.dtype, pd.Int8Dtype) or
                isinstance(df_column.dtype, pd.Int16Dtype) or
                isinstance(df_column.dtype, pd.Int32Dtype) or
                isinstance(df_column.dtype, pd.Int64Dtype)):
            return 'numeric'
        else:
            return 'any'

    def hide_or_not(self, df, hideable):
        columns = [
            {'name': i, 'id': i, 'type': self._table_type(df[i]), 'hideable': hideable} for i in df.columns
        ]
        return columns

    def return_sortedtable_and_makecolhideable(self, sort_by, callback_context, finalchart, source):
        finalchartdf = self.return_sortedtable(sort_by, callback_context, finalchart, source)
        columns = self.hide_or_not(finalchartdf, True) if len(finalchartdf) != 0 else None
        return finalchartdf.to_dict('records'), columns

    def sort_and_makecolhideable(self, sort_by, sourcetable):
        df = pd.DataFrame.from_records(sourcetable)
        df = self.sort_datatable(sort_by, df)
        columns = self.hide_or_not(df, True)
        return df.to_dict('records'), columns
