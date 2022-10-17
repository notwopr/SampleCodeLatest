# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS


class CurveType:
    '''
    takes a Series, either removes all nans, or ffills and removes leadings nans, and then transforms it into a different curvetype
    '''
    def baremax_cruncher(self, series):
        currmax = None
        for i, v in series.items():
            if np.isnan(v):
                pass
            elif not currmax or v > currmax:
                currmax = v
            else:
                series.at[i] = currmax
        return series

    def baremin_cruncher(self, series):
        '''allows leading nans, but assumes no NaNs afterwards'''
        currmin = None
        for i, v in series[::-1].items():
            # iterate thru series in reverse order
            if np.isnan(v):
                pass
            elif not currmin or v < currmin:
                currmin = v
            else:
                series.at[i] = currmin
        return series

    def true_cruncher(self, series):
        bmin = self.baremin_cruncher(series.copy())
        bmax = self.baremax_cruncher(series.copy())
        for i, v in series.items():
            series.at[i] = ((bmax.at[i] - bmin.at[i]) / 2) + bmin.at[i]
        return series

    def straight_cruncher(self, series):
        age = len(series) - 1
        price_start = series.iloc[0]
        price_end = series.iloc[-1]
        slope = (price_end - price_start) / age
        for i, v in series.items():
            series.at[i] = (slope * (i-series.index[0])) + price_start
        return series

    def transform(self, origseries, look_back, curvetype, nantreatment):
        series = origseries.copy()
        if nantreatment == 'ffillandremove':
            series.ffill(inplace=True)
        if look_back:
            series = series.iloc[-look_back-1:]
        series.dropna(inplace=True)
        if len(series) == 0:
            return series

        if 'norm' in curvetype:
            price_start = series.iloc[0]
            if curvetype == 'norm':  # normalize to 0
                series = series.apply(lambda x: (x / price_start) - 1)
            if curvetype == 'norm1':  # normalize to 1
                series = series.apply(lambda x: (x / price_start))

        if 'baremin' in curvetype:
            series = self.baremin_cruncher(series)
        if 'baremax' in curvetype:
            series = self.baremax_cruncher(series)
        if 'true' in curvetype:
            series = self.true_cruncher(series)
        if 'straight' in curvetype:
            series = self.straight_cruncher(series)

        if 'ppc' in curvetype:
            series = series.pct_change()

        if 'abs' in curvetype:
            series = series.abs()

        if 'nonzero' in curvetype:
            series = series.loc[series != 0]

        if '>0' in curvetype:
            series = series.loc[series > 0]

        if '>=0' in curvetype:
            series = series.loc[series >= 0]

        if '<0' in curvetype:
            series = series.loc[series < 0]

        if '<=0' in curvetype:
            series = series.loc[series <= 0]

        return series
