'''
The baker takes a stratcode and invest_startdate and returns full dataframe ranking
INPUTS:
1. dataframe of eodprices
2. ingredient dict
3. metricfunction
GOAL:
read dict and convert it into
metricfunction's specific targetvars
metricfunction needs to be in matrix friendly format as well
iteritem from dataframe.iteritems() is an iterable that is a tuple of form (colname, series). ('iteritems' is deprecated. use 'items' instead)
If you pass thatthrough a function that does some calculation on the series and return a list in form of [colname, seriesresult]
then, the multiprocess.map_async.get() command will return a list of the form = [
    [colname1, val1],
    [colname2, val2],
    ...
]
If you input this list of lists into a dataframe constructor (pd.DataFrame(data=listoflists), it'll produce a dataframe with an index col, a col that contains the colnames, and a third col that contain the values.
'''
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from newbacktest.strategies.db_strategycookbook import StrategyCookBook
from newbacktest.stagerecipes.db_stagerecipe import StageRecipeDatabase
from newbacktest.stratpools.class_stratpool import Stratpool
from newbacktest.stratpools.db_stratpool import StratPoolDatabase
from newbacktest.tickerportal import TickerPortal
from newbacktest.ingredients.db_ingredient import IngredientsDatabase
from newbacktest.ingredients.db_ingredient_settings import IngredientSettingsDatabase
from newbacktest.ingredients.db_metricfunction import MetricFunctionDatabase
from newbacktest.datasource import DataSource
from newbacktest.multiprocessor import MultiProcessor
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.baking.curvetype import CurveType


class Baker:
    def get_metricval_byticker(self, metricvaldf, ingredient, target_ticker):
        return metricvaldf[metricvaldf['stock'] == target_ticker][ingredient.colname].item()

    def get_metricval_bybestbench(self, metricvaldf, ingredient):
        targetvals = metricvaldf[metricvaldf['stock'].isin(["^DJI", "^INX", "^IXIC"])][ingredient.colname]
        return max(targetvals) if ingredient.itemdata['threshold_bybestbench_better'] == 'bigger' else min(targetvals)

    def _retrieve_threshval(self, i, metricvaldf):
        if i.itemdata['threshold_type'] == 'byticker':
            threshval = self.get_metricval_byticker(metricvaldf, i, i.itemdata['threshold_value'])
        elif i.itemdata['threshold_type'] == 'byvalue':
            threshval = i.itemdata['threshold_value']
        elif i.itemdata['threshold_type'] == 'bybestbench':
            threshval = self.get_metricval_bybestbench(metricvaldf, i)
        return threshval

    def _filter_stagedf(self, metricvaldf, ingredientlist, df):
        # create copy df for purposes of getting threshvals. otherwise the filtered_df may not have all stocks available to grab the threshval requested
        for i in ingredientlist:
            threshval = self._retrieve_threshval(i, metricvaldf)
            if i.itemdata.get('threshold_buffer', 0):
                if type(i.itemdata['threshold_buffer']) == list:
                    threshval = [a+b for a, b in zip(threshval, i.itemdata['threshold_buffer'])]
                else:
                    threshval += i.itemdata['threshold_buffer']
            if type(threshval) == list:
                df = DataFrameOperations().filtered_double(df, i.itemdata['filterdirection'], threshval[0], threshval[1], i.colname)
            else:
                df = DataFrameOperations().filtered_single(df, i.itemdata['filterdirection'], threshval, i.colname)
            if len(df) == 0:
                print("Stocks all filtered out!")
                return df
        return df

    def percentile_rankdir_correction(self, irankdir, iranktype):
        '''rankdir_choices is either ['a' or 'd']'''
        '''
        if i want values to be descending, then i want bigger values to have the better ranking.  So, then in percentile rank, the biggest value should be labeled 1.  Percentile rank of a value is the percent of the data that is <= to that value.  This ranking is in ascending percentile order.  Thus, when I say I want values to be ranked in descending order, if I want the ranking to be represented in percentile, then the rank order needs to be ascending.
        I want percentile 1 to represent the best rank.
        if a and ordinal, then a or 0
        if a and percentile, then d or 1
        if d and ordinal, then d or 1
        if d and percentile, then a or 0
        '''
        rankdir_choices = IngredientSettingsDatabase().igsdb['rankdirection']['vlimit_details']
        rankdir_choice_index = not any([all([irankdir == 'a', iranktype == 'ordinal']), all([irankdir == 'd', iranktype == 'percentile'])])
        return 'a' == rankdir_choices[rankdir_choice_index]

    def _rank_stagedf(self, ingredientlist, df):
        w_total = 0
        sumcols = []
        for i in ingredientlist:
            r = f'RANK_{i.colname} (w={i.itemdata["weight"]})'
            rankdir = self.percentile_rankdir_correction(i.itemdata['rankdirection'], i.itemdata['ranktype'])
            df[r] = df[i.colname].rank(ascending=rankdir, pct=i.itemdata['ranktype'] == 'percentile')
            df[f'w_{i.colname}'] = (df[r] * i.itemdata['weight'])
            w_total += i.itemdata['weight']
            sumcols.append(f'w_{i.colname}')
        m = f'wRANK {w_total}'
        df[m] = df[sumcols].sum(axis=1, min_count=len(sumcols))
        f = 'FINAL RANK'
        df[f] = df[m].rank(ascending=i.itemdata['ranktype'] != 'percentile')
        df.sort_values(ascending=True, by=[f], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def _bake_singleticker(self, ingredientlist, date, dfiteritem):
        ticker = dfiteritem[0]
        seriesdata = dfiteritem[1]
        single_sr_result = {'stock': ticker}
        for i in ingredientlist:
            metricfuncname = i.itemdata['metricfunc']
            newseries = CurveType().transform(seriesdata, i.itemdata['look_back'], i.itemdata['curvetype'], i.itemdata['nantreatment'])

            dictofargs = MetricFunctionDatabase().get_metricfuncargdict(metricfuncname, i.itemdata, date, newseries)
            metricfuncobj = MetricFunctionDatabase().metricfuncname_to_metricfuncobj(metricfuncname)
            single_sr_result.update(
                {i.colname: metricfuncobj(**dictofargs)}
                )
        return single_sr_result

    def _igcode_groupbycriteria(self, igcodelist, criteria):
        ig_bycriteria = {}
        for igcode in igcodelist:
            i = IngredientsDatabase().view_item(igcode)
            ig_bycriteria[i.itemdata[criteria]] = ig_bycriteria.get(i.itemdata[criteria], []) + [i.itemcode]
        return ig_bycriteria

    def _bake_stagerecipe(self, tickers, date, igcodedict):
        '''
        for each datasource required,
        pull datasource,
        trim datasource as required, group ingredients by datasource, then by calibration, then by lookback, then return resulting data
        '''
        allresults = []
        for datasourcetype, igcodes in igcodedict.items():
            if datasourcetype == 'eodprices':
                datasourcetype = 'eodprices_commonplusbench'
            ds = DataSource().opends(datasourcetype)
            ds = DataFrameOperations().filter_bycolandrow_single(ds, '<=', date, 'date', tickers)
            ingredientlist = [IngredientsDatabase().view_item(igcode) for igcode in igcodes]
            r = MultiProcessor().dataframe_reduce_bycol(ds, self._bake_singleticker, (ingredientlist, date))
            allresults.append(pd.DataFrame(data=r))
        # join results into final df
        resultdf = DataFrameOperations().join_matrices('stock', allresults)
        return resultdf

    def _bake_strategy(self, stratcode, invest_startdate):
        '''
        get stagecodes, tickers that existed on given date, then for each stage code bake stagerecipe, then save resulting dataframe to the Stratpool Database
        '''
        stratinstruct = StrategyCookBook().view_item(stratcode).itemdata
        remainingtickers = TickerPortal().existing_tickers(invest_startdate, 'common+bench')

        for stagecode in stratinstruct.values():

            sr = StageRecipeDatabase().view_item(stagecode)
            igcodelist = sr.itemdata
            igcodedict = self._igcode_groupbycriteria(igcodelist, 'sourcedata')
            allmetricvaldf = self._bake_stagerecipe(remainingtickers, invest_startdate, igcodedict)
            # savedftocsv_fullpath(Path(join_str([DirPaths().bot_dump, "allmetricvalsdf.csv"])), allmetricvaldf)

            ingredientlist = [IngredientsDatabase().view_item(igcode) for igcode in igcodelist]
            resultdf = allmetricvaldf[~allmetricvaldf['stock'].isin(["^DJI", "^INX", "^IXIC", 'date'])].copy()
            if sr.itemtype == 'sorter':
                resultdf = self._rank_stagedf(ingredientlist, resultdf)
            elif sr.itemtype == 'filter':
                resultdf = self._filter_stagedf(allmetricvaldf, ingredientlist, resultdf)
            remainingtickers = resultdf['stock'].tolist()
            if not remainingtickers:
                break
        sp = Stratpool(stratcode, invest_startdate, resultdf)
        StratPoolDatabase().add_item(sp)
