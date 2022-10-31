# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from itertools import permutations
#   THIRD PARTY IMPORTS
from dash import callback_context
import pandas as pd
import plotly.express as px
import numpy as np
#   LOCAL APPLICATION IMPORTS
from ..datatables import DataTableOperations
from .pricehistoryexplorer_helper_volstats_definitions import volstat_definitions
from .pricehistoryexplorer_helper_volstats import getallmetricvalsdf
from Modules.price_calib import convertpricearr, add_calibratedprices_portfolio
from Modules.price_history_slicing import pricedf_daterange
from Modules.dataframe_functions import filtered_single
from .pricehistoryexplorer_helper_diffcomp import add_comparisons_portfolio, add_pdiffpctchange_portfolio


class PriceExplorerHelperFunctions:

    def show_portcurve_option(self, ticker, calib, portcurvevalue):
        if ticker and calib == 'normalize' and len(ticker) > 1:
            return [
                {'label': 'Add portfolio graph', 'value': 'portcurve'}
            ], portcurvevalue

        else:
            return [], []

    def show_diffgraph_options(self, contour):
        if len(contour) == 0:
            return [], None, ['rawprice'], 'rawprice'
        else:
            p = permutations(contour + ['rawprice'], 2)
            return [{'label': f'{i[0]} to {i[1]}', 'value': f'{i[0]} {i[1]}'} for i in p], None, ['all', 'rawprice']+contour, 'all'

    def sort_rawdatatable(self, sort_by, rawdatatable, sourcetable):
        if rawdatatable and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
            # convert table back to dataframe
            filterdf = pd.DataFrame.from_records(rawdatatable)
            # because filterdf is converted to .to_dict('records') and then back from that; the date col type is changed to strings
            # as consequence have to change datecol back to original datatype: <class 'pandas._libs.tslibs.timestamps.Timestamp'>
            filterdf['date'] = filterdf['date'].apply(lambda x: pd.Timestamp(x))
            filterdf = DataTableOperations().sort_datatable(sort_by, filterdf)
            return filterdf.to_dict('records')
        else:
            return sourcetable

    def gen_volstats(self, ticker, portcurve, bench, sort_by, voldata, sourcetable):
        if voldata and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
            # convert table back to dataframe
            voldf = pd.DataFrame.from_records(voldata)
            voldf = DataTableOperations().sort_datatable(sort_by, voldf)
            tooltip = {i: volstat_definitions[i] for i in voldf.columns[1:]}
        elif ticker:
            portfolio = ticker.copy()
            filterdf = pd.DataFrame.from_records(sourcetable)
            # because filterdf is converted to .to_dict('records') and then back from that; the date col type is changed to strings
            # as consequence have to change datecol back to original datatype: <class 'pandas._libs.tslibs.timestamps.Timestamp'>
            filterdf['date'] = filterdf['date'].apply(lambda x: pd.Timestamp(x))
            metdftickers = portfolio+[f'bench_{b}' for b in bench]+['portcurve'] if 'portcurve' in portcurve else portfolio+[f'bench_{b}' for b in bench]
            voldf = getallmetricvalsdf(filterdf, metdftickers, bench, str(filterdf.iat[0, 0].date()), str(filterdf.iat[-1, 0].date()))
            tooltip = {i: volstat_definitions[i] for i in voldf.columns[1:]}
        else:
            voldf = pd.DataFrame(data=['No ticker selected.'])
            tooltip = None
        return voldf.to_dict('records'), tooltip

    def gen_graph_fig(self, filterdf, ticker, diffgraphcols, compgraphcols, hovermode):
        fig = px.line(filterdf, x='date', y=ticker, markers=False)
        fig.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
        fig.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
        fig_diff = px.line(filterdf, x='date', y=diffgraphcols, markers=False)
        fig_diff.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
        fig_diff.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
        fig_comp = px.line(filterdf, x='date', y=compgraphcols, markers=False)
        fig_comp.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
        fig_comp.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
        return fig, fig_diff, fig_comp

    def gen_graph_df(self, ticker, calib, sd, sd_bydd, contour, graphcomp, gdm, gdc, gdp, portcurve, bench, hovermode):
        portfolio = ticker.copy()
        df = pricedf_daterange(ticker[0], '', '')
        for t in ticker[1:]:
            df = df.join(pricedf_daterange(t, '', '').set_index('date'), how="outer", on="date")
        df.sort_values(by='date', inplace=True)
        df.reset_index(inplace=True, drop=True)
        new_sd = str(df['date'].iloc[0].date())  # shift graph&slider to start at beginning of oldest selected stock
        all_sd = [{'label': f"{t}'s startdate", 'value': df['date'].iloc[sum(np.isnan(df[t]))]} for t in ticker]
        for b in bench:
            bdf = pricedf_daterange(b, '', '')
            bdf.rename(columns={b: f'bench_{b}'}, inplace=True)
            df = df.join(bdf.set_index('date'), how="left", on="date")
        ticker += [f'bench_{b}' for b in bench]
        if sd is not None:  # choose a diff start from datepicker
            df = filtered_single(df, '>=', sd, 'date')
            df.reset_index(drop=True, inplace=True)
        if sd_bydd is not None:  # choose a diff start from selected stocks list
            df = filtered_single(df, '>=', sd_bydd, 'date')
            df.reset_index(drop=True, inplace=True)
        if calib == 'normalize':
            df[ticker] = df[ticker].apply(lambda x: convertpricearr(x, 'norm1'))
            if len(ticker) > 1 and 'portcurve' in portcurve:
                df['portcurve'] = df[ticker].mean(axis=1)
                ticker += ['portcurve']
        df = add_calibratedprices_portfolio(df, contour, ticker)
        if len(contour) > 0:
            ticker += [f'{t}_{c}' for c in contour for t in ticker]
        if graphcomp:
            gc_inputs = graphcomp.split(" ")
            gcomp_portfolio = portfolio+[f'bench_{b}' for b in bench]+['portcurve'] if 'portcurve' in ticker else portfolio+[f'bench_{b}' for b in bench]
            df = add_comparisons_portfolio(df, gc_inputs[0], gc_inputs[1], gcomp_portfolio)
            compgraphcols = [f'{s}_{gc_inputs[0]}to{gc_inputs[1]}' for s in gcomp_portfolio]
        else:
            compgraphcols = None
        df, sourcecols = add_pdiffpctchange_portfolio(df, gdc, gdp, gdm, ticker)
        diffgraphcols = [f'{s}_{gdp}d_{gdm}' for s in sourcecols]
        return df, compgraphcols, diffgraphcols, new_sd, all_sd
