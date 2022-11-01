# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import callback_context
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from .grapher_helper_volstats_profile import VolStatProfile
from ..datatables import DataTableOperations
from newbacktest.baking.baker_stratpool import Baker


class VolStatFunctions:

    def gen_volstatdf(self, tickers, invest_startdate, vsp):
        igcodedict = {'eodprices': [ig.itemcode for ig in vsp.values()]}
        volstatdf = Baker()._bake_stagerecipe(tickers, invest_startdate, igcodedict)
        volstatdf.rename(columns={ig.colname: ig.nickname for ig in vsp.values()}, inplace=True)
        return volstatdf[['stock']+[ig.nickname for ig in vsp.values()]].copy()

    def gen_volstats(self, ticker, portcurve, bench, sort_by, voldata, invest_startdate):
        vsp = VolStatProfile().ingredientobjects
        tooltip = {ig.nickname: ig.description for ig in vsp.values()}
        if voldata and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
            volstatdf = pd.DataFrame.from_records(voldata)
            return DataTableOperations().sort_datatable(sort_by, volstatdf).to_dict('records'), tooltip
        volstatdf = self.gen_volstatdf(ticker+bench, invest_startdate, vsp)
        if 'portcurve' in portcurve:
            portrow = {**{'stock': 'portcurve'}, **{c: volstatdf[volstatdf['stock'].isin(ticker)][c].mean() for c in volstatdf.columns[1:]}}
            volstatdf = pd.concat([volstatdf, pd.Series(portrow).to_frame().T], ignore_index=True)
        return volstatdf.to_dict('records'), tooltip
