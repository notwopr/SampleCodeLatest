# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import callback_context
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from .grapher_helper_volstats_profile import VolStatProfile
from ..datatables import DataTableOperations
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.multiprocessor import MultiProcessor
from newbacktest.ingredients.class_ingredient_colnamegenerator import ColNameGenerator
from newbacktest.ingredients.db_metricfunction import MetricFunctionDatabase
from newbacktest.baking.curvetype import CurveType


class VolStatFunctions:

    def _bake_singleticker(self, ingredientlist, date, dfiteritem):
        ticker = dfiteritem[0]
        seriesdata = dfiteritem[1]
        single_sr_result = {'stock': ticker}
        for i in ingredientlist:
            metricfuncname = i['metricfunc']
            newseries = CurveType().transform(seriesdata, i['look_back'], i['curvetype'], i['nantreatment'])
            dictofargs = MetricFunctionDatabase().get_metricfuncargdict(metricfuncname, i, date, newseries)
            metricfuncobj = MetricFunctionDatabase().metricfuncname_to_metricfuncobj(metricfuncname)
            single_sr_result.update(
                {ColNameGenerator().gen_colname(i): metricfuncobj(**dictofargs)}
                )
        return single_sr_result

    def gen_volstatdf(self, tickers, graphdfdata, vsp):
        graphdf = pd.DataFrame.from_records(graphdfdata)
        date = graphdf['date'].iloc[-1]
        ds = DataFrameOperations().filter_column(graphdf, tickers)
        ingredientlist = vsp.volstatprofile[0]
        r = MultiProcessor().dataframe_reduce_bycol(ds, self._bake_singleticker, (ingredientlist, date))
        volstatdf = pd.DataFrame(data=r)
        volstatdf.rename(columns={k: v for k, v in vsp.nicknamebycolname.items()}, inplace=True)
        return volstatdf[['stock']+list(vsp.nicknamebyindex.values())].copy()

    def gen_volstats(self, ticker, portcurve, bench, sort_by, voldata, graphdfdata):
        vsp = VolStatProfile()
        tooltip = {k: v for k, v in vsp.volstat_definitions.items()}

        if voldata and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
            volstatdf = pd.DataFrame.from_records(voldata)
            return DataTableOperations().sort_datatable(sort_by, volstatdf).to_dict('records'), tooltip

        volstatdf = self.gen_volstatdf(ticker+bench, graphdfdata, vsp)

        if 'portcurve' in portcurve:
            portrow = {**{'stock': 'portcurve'}, **{c: volstatdf[volstatdf['stock'].isin(ticker)][c].mean() for c in volstatdf.columns[1:]}}
            volstatdf = pd.concat([volstatdf, pd.Series(portrow).to_frame().T], ignore_index=True)

        return volstatdf.to_dict('records'), tooltip
