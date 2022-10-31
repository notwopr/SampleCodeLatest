from newbacktest.baking.curvetype import CurveType


class CurveCalibrator:

    def transform(self, origseries, curvetype):
        '''takes a series and returns its converted form'''
        series = origseries.copy()
        if 'baremin' in curvetype:
            return CurveType().baremin_cruncher(series)
        if 'baremax' in curvetype:
            return CurveType().baremax_cruncher(series)
        if 'true' in curvetype:
            return CurveType().true_cruncher(series)
        if 'straight' in curvetype:
            return CurveType().straight_cruncher(series)
        if curvetype.startswith('norm'):
            nonnanbeg = series.first_valid_index()
            price_start = series.iloc[nonnanbeg]
            if curvetype == 'norm':  # normalize to 0
                return series.apply(lambda x: (x / price_start) - 1)
            if curvetype == 'norm1':  # normalize to 1
                return series.apply(lambda x: (x / price_start))

    def normalize_curves(self, df, normtype, targetcols):
        '''takes a dataframe of prices and and replaces curves with normalized ones'''
        if normtype == 'norm':
            df[[f'{c}_norm' for c in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, normtype))
        elif normtype == 'norm1':
            df[[f'{c}_norm1' for c in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, normtype))

    def add_curvetypes(self, df, allcalibrations, targetcols):
        '''takes a dataframe of prices and adds curvetypes specified'''
        if 'true' in allcalibrations:
            df[[f'{s}_true' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'true'))
        if 'baremin' in allcalibrations:
            df[[f'{s}_baremin' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'baremin'))
        if 'baremax' in allcalibrations:
            df[[f'{s}_baremax' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'baremax'))
        if 'straight' in allcalibrations:
            df[[f'{s}_straight' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'straight'))
