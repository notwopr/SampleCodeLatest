# IMPORT TOOLS
#   Standard library imports
#   Third party imports
#   Local application imports


class GrowthCalculator:
    # if beginning of array is zero or set of consecutive zeros, replace it or them with the next nonzero value
    def replaceleadzeros(self, seriesdata):
        nonzeroindices = seriesdata.to_numpy().nonzero()
        if seriesdata.iloc[0] == 0 and nonzeroindices:
            firstnonzeroindex = nonzeroindices[0][0]
            # replace all preceding elems with elem
            seriesdata.iloc[:firstnonzeroindex] = seriesdata.iat[firstnonzeroindex]
            return seriesdata
        else:
            return seriesdata

    # REMOVE LEADING ZEROS FROM EACH COLUMN OF DATAFRAME WITH NEXT NONZERO VALUE IN THAT COLUMN
    def removeleadingzeroprices(self, portfoliodf, modcols):
        # replace leading zero prices with next nonzero prices
        portfoliodf[modcols] = portfoliodf[modcols].apply(lambda x: self.replaceleadzeros(x))
        return portfoliodf

    # GET NORMALIZED PRICES GIVEN (1) PORTFOLIO OF PRICES ALREADY TRIMMED BY DATE AND (2) PORTFOLIO CONTENTS
    def getnormpricesdf(self, portfoliodf, portfolio):
        # replace leading zero prices with next nonzero price
        portfoliodf = self.removeleadingzeroprices(portfoliodf, portfolio)
        # normalize data
        firstp = portfoliodf.iloc[0][portfolio]
        portfoliodf[portfolio] = (portfoliodf[portfolio] - firstp) / firstp
        return portfoliodf

    # get portfolio growth rate
    def getportgrowthrate(self, portfoliodf, portfolio, mode):
        if mode == 'min':
            return self.getnormpricesdf(portfoliodf, portfolio).iloc[-1][portfolio].min()
        if mode == 'mean':
            return self.getnormpricesdf(portfoliodf, portfolio).iloc[-1][portfolio].mean()
        if mode == 'max':
            return self.getnormpricesdf(portfoliodf, portfolio).iloc[-1][portfolio].max()
        if mode == 'std':
            return self.getnormpricesdf(portfoliodf, portfolio).iloc[-1][portfolio].std()
        if mode == 'mad':
            return self.getnormpricesdf(portfoliodf, portfolio).iloc[-1][portfolio].mad()
