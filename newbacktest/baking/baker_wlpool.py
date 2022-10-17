'''
The baker takes a wlprofcode and invest_startdate and returns filtered dataframe of the winners/losers according to those parameters.

'''
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from newbacktest.perfmetrics.winnerloser.db_wlprofile import WinLoseProfDatabase
from newbacktest.tickerportal import TickerPortal
from newbacktest.ingredients.db_ingredient import IngredientsDatabase
from newbacktest.datasource import DataSource
from newbacktest.multiprocessor import MultiProcessor
from newbacktest.dataframe_operations import DataFrameOperations
from Modules.dates import DateOperations
from newbacktest.perfmetrics.winnerloser.class_wlpool import WLPool
from newbacktest.baking.baker_stratpool import Baker


class BakerWLPool(Baker):
    # def get_metricval_byticker(self, metricvaldf, ingredient, target_ticker):
    #     return metricvaldf[metricvaldf['stock'] == target_ticker][ingredient.colname].item()

    # def get_metricval_bybestbench(self, metricvaldf, ingredient):
    #     targetvals = metricvaldf[metricvaldf['stock'].isin(["^DJI", "^INX", "^IXIC"])][ingredient.colname]
    #     return max(targetvals) if ingredient.itemdata['threshold_bybestbench_better'] == 'bigger' else min(targetvals)

    # def _retrieve_threshval(self, i, metricvaldf):
    #     if i.itemdata['threshold_type'] == 'byticker':
    #         threshval = self.get_metricval_byticker(metricvaldf, i, i.itemdata['threshold_value'])
    #     elif i.itemdata['threshold_type'] == 'byvalue':
    #         threshval = i.itemdata['threshold_value']
    #     elif i.itemdata['threshold_type'] == 'bybestbench':
    #         threshval = self.get_metricval_bybestbench(metricvaldf, i)
    #     return threshval

    # def _filter_stagedf(self, metricvaldf, ingredientlist, df):
    #     # create copy df for purposes of getting threshvals. otherwise the filtered_df may not have all stocks available to grab the threshval requested
    #     for i in ingredientlist:
    #         threshval = self._retrieve_threshval(i, metricvaldf)
    #         if i.itemdata.get('threshold_buffer', 0):
    #             if type(i.itemdata['threshold_buffer']) == list:
    #                 threshval = [a+b for a, b in zip(threshval, i.itemdata['threshold_buffer'])]
    #             else:
    #                 threshval += i.itemdata['threshold_buffer']
    #         if type(threshval) == list:
    #             df = DataFrameOperations().filtered_double(df, i.itemdata['filterdirection'], threshval[0], threshval[1], i.colname)
    #         else:
    #             df = DataFrameOperations().filtered_single(df, i.itemdata['filterdirection'], threshval, i.colname)
    #         if len(df) == 0:
    #             print("Stocks all filtered out!")
    #             return df
    #     return df

    # def _bake_singleticker(self, ingredientlist, dfiteritem):
    #     ticker = dfiteritem[0]
    #     seriesdata = dfiteritem[1]
    #     single_sr_result = {'stock': ticker}
    #     for i in ingredientlist:
    #         metricfuncname = i.itemdata['metricfunc']
    #         newseries = CurveType().transform(seriesdata, i.itemdata['look_back'], i.itemdata['curvetype'], i.itemdata['nantreatment'])
    #
    #         dictofargs = MetricFunctionDatabase().get_metricfuncargdict(metricfuncname, i.itemdata, newseries)
    #         metricfuncobj = MetricFunctionDatabase().metricfuncname_to_metricfuncobj(metricfuncname)
    #         single_sr_result.update(
    #             {i.colname: metricfuncobj(**dictofargs)}
    #             )
    #     return single_sr_result

    # def _igcode_groupbycriteria(self, igcodelist, criteria):
    #     ig_bycriteria = {}
    #     for igcode in igcodelist:
    #         i = IngredientsDatabase().view_item(igcode)
    #         ig_bycriteria[i.itemdata[criteria]] = ig_bycriteria.get(i.itemdata[criteria], []) + [i.itemcode]
    #     return ig_bycriteria

    def _bake_wlrecipe(self, tickers, invest_startdate, invest_enddate, igcodedict):
        '''
        for each datasource required,
        pull datasource,
        trim datasource as required, group ingredients by datasource, then return resulting data
        '''
        allresults = []
        for datasourcetype, igcodes in igcodedict.items():
            if datasourcetype == 'eodprices':
                datasourcetype = 'eodprices_commonplusbench'
            ds = DataSource().opends(datasourcetype)
            ds = DataFrameOperations().filter_column(ds, ['date']+tickers)
            ds.ffill(inplace=True)
            ds = DataFrameOperations().filtered_double(ds, '>=<=', invest_startdate, invest_enddate, 'date')
            ds = DataFrameOperations().filter_column(ds, tickers)
            ingredientlist = [IngredientsDatabase().view_item(igcode) for igcode in igcodes]
            r = MultiProcessor().dataframe_reduce_bycol(ds, self._bake_singleticker, (ingredientlist,))
            allresults.append(pd.DataFrame(data=r))
        # join results into final df
        resultdf = DataFrameOperations().join_matrices('stock', allresults)
        return resultdf

    def _bake_wlprofile(self, wlprofcode, invest_startdate):
        '''
        get wlprofcode, tickers that existed on invest_startdate, get date range, trim datasource, then bake wlprofile with trimmed datasource, then save resulting dataframe to the wlpool Database
        '''
        remainingtickers = TickerPortal().existing_tickers(invest_startdate, 'common+bench')
        wlprofile = WinLoseProfDatabase().view_item(wlprofcode)
        invest_period = wlprofile.periodlen
        invest_enddate = DateOperations().plusminusdays(invest_startdate, invest_period)
        igcodelist = wlprofile.itemdata
        igcodedict = self._igcode_groupbycriteria(igcodelist, 'sourcedata')
        allmetricvaldf = self._bake_wlrecipe(remainingtickers, invest_startdate, invest_enddate, igcodedict)
        # savedftocsv_fullpath(Path(join_str([DirPaths().bot_dump, "allmetricvalsdf.csv"])), allmetricvaldf)

        ingredientlist = [IngredientsDatabase().view_item(igcode) for igcode in igcodelist]
        resultdf = allmetricvaldf[~allmetricvaldf['stock'].isin(["^DJI", "^INX", "^IXIC", 'date'])].copy()
        resultdf = self._filter_stagedf(allmetricvaldf, ingredientlist, resultdf)
        wlpoolobj = WLPool(wlprofcode, invest_startdate, invest_enddate, invest_period, resultdf)
        return wlpoolobj
