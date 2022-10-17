# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS
from newbacktest.portfolios.db_portfolio import PortfolioDatabase
from newbacktest.growthcalculator import GrowthCalculator
from newbacktest.datasource import DataSource
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.perfmetrics_funclib.perfmetrics_funclib_info import invest_startdate, invest_enddate, periodlen


def geometric_rate(r, n):
    '''
    returns the geometric rate of an existing rate
    e.g. if r is a growth rate over a 30-day period, what is the daily rate?
    '''
    return ((1 + r) ** (1 / n)) - 1


def growthrate_effectivedaily(sampcode):
    pgr = growthrate_period(sampcode)
    if isinstance(pgr, dt.datetime) or np.isnan(pgr):
        return np.nan
    else:
        return geometric_rate(pgr, periodlen(sampcode))


def growthrate_effectivedaily_bestbench(sampcode):
    return geometric_rate(growthrate_period_bestbench(sampcode), periodlen(sampcode))


def growthrate_effectivedaily_margin(sampcode):
    ged = growthrate_effectivedaily(sampcode)
    if np.isnan(ged):
        return np.nan
    else:
        return growthrate_effectivedaily(sampcode) - growthrate_effectivedaily_bestbench(sampcode)


def growthrate_period(sampcode):
    portfoliodf = PortfolioDatabase().view_item(sampcode)
    if type(portfoliodf) == int:
        return np.nan
    portfolio = portfoliodf.columns[1:]
    return GrowthCalculator().getportgrowthrate(portfoliodf, portfolio, 'mean')


def growthrate_period_bestbench(sampcode):
    s = invest_startdate(sampcode)
    e = invest_enddate(sampcode)
    ds = DataSource().opends('eodprices_bench')
    ds.ffill(inplace=True)
    benchdf = DataFrameOperations().filtered_double(ds, '>=<=', s, e, 'date').copy()
    benchtickers = benchdf.columns[1:]
    if len(benchdf) == 0:
        return np.nan
    else:
        growthdf = GrowthCalculator().getnormpricesdf(benchdf, benchtickers)
        return growthdf.iloc[-1][benchtickers].max()


def growthrate_period_margin(sampcode):
    pgr = growthrate_period(sampcode)
    bgr = growthrate_period_bestbench(sampcode)
    if isinstance(pgr, dt.datetime) or np.isnan(pgr):
        return np.nan
    else:
        return pgr-bgr


def above_bench(sampcode):
    pgr = growthrate_period(sampcode)
    bgr = growthrate_period_bestbench(sampcode)
    if isinstance(pgr, dt.datetime) or np.isnan(pgr) or np.isnan(bgr):
        return np.nan
    return 1 if pgr > bgr else 0


def above_zero(sampcode):
    pgr = growthrate_period(sampcode)
    if isinstance(pgr, dt.datetime) or np.isnan(pgr):
        return np.nan
    return 1 if pgr > 0 else 0


def above_zero_and_bench(sampcode):
    if np.isnan(above_bench(sampcode)) or np.isnan(above_zero(sampcode)):
        return np.nan
    return 1 if above_bench(sampcode) == above_zero(sampcode) == 1 else 0
