from pprintpp import pprint
from newbacktest.class_stagerecipe import StageRecipe
from newbacktest.db_stagerecipe import StageRecipeDatabase
# from newbacktest.class_ingredient import Ingredient
# from newbacktest.db_ingredient import IngredientsDatabase
# from newbacktest.class_strategy import Strategy
# from newbacktest.db_strategycookbook import StrategyCookBook
# from newbacktest.class_stratpool import Stratpool
# from newbacktest.db_stratpool import StratPoolDatabase
# from newbacktest.baker import Baker
from Modules.dates import DateOperations
from newbacktest.datasource import DataSource
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.tickerportal import TickerPortal
from newbacktest.multiprocessor import MultiProcessor
from newbacktest.db_metricfunction import MetricFunctionDatabase
import pandas as pd

'''
iteritem from dataframe.iteritems() is an iterable that is a tuple of form (colname, series).
If you pass thatthrough a function that does some calculation on the series and return a list in form of [colname, seriesresult]
then, the multiprocess.map_async.get() command will return a list of the form = [
    [colname1, val1],
    [colname2, val2],
    ...
]
If you input this list of lists into a dataframe constructor (pd.DataFrame(data=listoflists), it'll produce a dataframe with an index col, a col that contains the colnames, and a third col that contain the values.
If we pass a stagerecipe through with multiple metricfunctions, can we design a function that will return for each iterable:
    [colname, mval1, mval2, ...., mvaln]?


'''


def subfunc1(series):
    return series.max()


def subfunc2(series):
    return series.mean()


def _bake_singleticker(ingredientlist, dfiteritem):
    ticker = dfiteritem[0]
    seriesdata = dfiteritem[1]
    single_sr_result = {'stock': ticker}
    for i in ingredientlist:
        metricfuncname = i.itemdata['metricfunc']
        dictofargs = MetricFunctionDatabase().get_metricfuncargdict(metricfuncname, i, seriesdata)
        metricfuncobj = MetricFunctionDatabase().metricfuncname_to_metricfuncobj(metricfuncname)
        single_sr_result.update(
            {i.itemcode: metricfuncobj(**dictofargs)}
            )
    return single_sr_result


date = '2017-04-01'
lookback = 10
remainingtickers = TickerPortal().existing_tickers(date, 'common')
remainingtickers = remainingtickers[:3]
ds = DataSource().opends('eodprices')
ds = DataFrameOperations().filter_bycolandrow_single(ds, '<=', date, 'date', ['date']+remainingtickers)
ds = DataFrameOperations().filtered_single(ds, '>=', DateOperations().plusminusdays(date, -lookback), 'date')
if __name__ == '__main__':
    print(ds)
    r = MultiProcessor().dataframe_reduce_bycol(ds, get_single_sr_result, ())
    df = pd.DataFrame(data=r)
    print(df)
    exit()
