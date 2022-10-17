from newbacktest.baking.curvetype import CurveType


class CurveCalibrator:
    '''takes a dataframe of prices and adds curvetypes specified'''
    def transform(self, origseries, curvetype):
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
        if normtype == 'norm':
            df[targetcols] = df[targetcols].apply(lambda x: self.transform(x, normtype))
        elif normtype == 'norm1':
            df[targetcols] = df[targetcols].apply(lambda x: self.transform(x, normtype))

    def add_curvetypes(self, df, allcalibrations, targetcols):
        if 'true' in allcalibrations:
            df[[f'{s}_true' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'true'))
        if 'baremin' in allcalibrations:
            df[[f'{s}_baremin' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'baremin'))
        if 'baremax' in allcalibrations:
            df[[f'{s}_baremax' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'baremax'))
        if 'straight' in allcalibrations:
            df[[f'{s}_straight' for s in targetcols]] = df[targetcols].apply(lambda x: self.transform(x, 'straight'))

    def add_comparison_curves(self, df, uppercol, lowercol, portfolio):
        # get comparison
        for s in portfolio:
            upper_label = s if uppercol == 'rawprice' else f'{s}_{uppercol}'
            lower_label = s if lowercol == 'rawprice' else f'{s}_{lowercol}'
            df[f'{s}_{uppercol}to{lowercol}'] = (df[upper_label] - df[lower_label]) / df[lower_label]

    def add_pdiffpctchange_portfolio(self, df, changecol, period, mode, portfolio):
        if changecol == 'all':
            sourcecols = portfolio
        elif changecol == 'rawprice':
            sourcecols = [s for s in portfolio if not any([b in s for b in ['baremax', 'baremin', 'straight', 'true']])]
        else:
            sourcecols = [s for s in portfolio if changecol in s]
        if mode == 'pdiff':
            df[[f'{s}_{period}d_{mode}' for s in sourcecols]] = df[sourcecols].diff(periods=period)
        if mode == 'pctchange':
            df[[f'{s}_{period}d_{mode}' for s in sourcecols]] = df[sourcecols].pct_change(periods=period, fill_method='ffill')
        return sourcecols
