"""
Title: Price Graph Explorer
Date Started: Feb 3, 2022
Version: 1.00
Version Start: Feb 3, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import html, callback_context  # , dcc
from dash.dependencies import Input, Output, State
from dashappobject import app
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from ..os_functions import get_currentscript_filename
from ..common_resources import staticmaxdate, tickers as alltickers, staticmindate
from webapp.servernotes import getbenchdates, get_minmaxdates, get_ipodate
from globalvars import benchmarks as benchmarksinfo
from ..graphing.grapher import GraphAssets
from ..datatables import DataTableOperations
from ..graphing.grapher_helper_functions import GrapherHelperFunctions
from ..graphing.grapher_helper_volstats import VolStatFunctions

benchtickers = [benchmarksinfo[k]['ticker'] for k in benchmarksinfo]
benchmarkdata = getbenchdates(benchmarksinfo)

bp = BotParams(
    get_currentscript_filename(__file__),
    'Price Explorer',
    "Display the price graphs of any NYSE/NASDAQ stock and index.",
    None
)

layout = html.Div(GraphAssets(bp).perfgraphtab, id=f'input_{bp.botid}')


@app.callback(
    Output(f"perf_graph_ticker_{bp.botid}", "options"),
    Input(f"bench_{bp.botid}", 'value'),
    )
def set_tickers(benchmarks):
    return [t for t in alltickers if t not in benchmarks]


@app.callback(
    Output(f"portcurve_{bp.botid}", "options"),
    Output(f"portcurve_{bp.botid}", "value"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value")
    )
def show_portcurve_option(ticker, calib, portcurvevalue):
    return GrapherHelperFunctions().show_portcurve_option(ticker, calib, portcurvevalue)


# create options for diffgraph and comp graph
@app.callback(
    Output(f"graphcompoptions_{bp.botid}", "options"),
    Output(f"graphcompoptions_{bp.botid}", "value"),
    Output(f"graphdiff_changecol_{bp.botid}", "options"),
    Output(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"contour_{bp.botid}", "value")
    )
def show_diffcomp_options(contour):
    return GrapherHelperFunctions().show_diffcomp_options(contour)


@app.callback(
    Output(f"perf_graph_{bp.botid}", "figure"),
    Output(f"graphdiff_{bp.botid}", "figure"),
    Output(f"graphcomp_{bp.botid}", "figure"),
    Output(f"graphdf_{bp.botid}", "data"),
    Output(f"sd_bydd_{bp.botid}", "options"),
    Output(f'datepicker_{bp.botid}', "min_date_allowed"),
    Output(f'datepicker_{bp.botid}', "max_date_allowed"),
    Output(f'datepicker_{bp.botid}', "start_date"),
    Output(f'datepicker_{bp.botid}', "end_date"),
    Output(f'minmaxinfo_datepicker_{bp.botid}', "children"),
    Output(f"sd_bydd_{bp.botid}", "value"),
    Output(f'bench_{bp.botid}', "options"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f'datepicker_{bp.botid}', "max_date_allowed"),
    Input(f"sd_bydd_{bp.botid}", "value"),
    Input(f'datepicker_{bp.botid}', "start_date"),
    Input(f'datepicker_{bp.botid}', "end_date"),
    Input(f"contour_{bp.botid}", "value"),
    Input(f"graphcompoptions_{bp.botid}", "value"),
    Input(f"graphdiff_mode_{bp.botid}", "value"),
    Input(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"graphdiff_period_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value"),
    Input(f"bench_{bp.botid}", 'value'),
    Input(f"hovermode_{bp.botid}", 'value')
    )
def gen_graph(tickers, calib, max_date_allowed, sd_bydd, pick_start, pick_end, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode):
    nondatetriggers = [
        callback_context.triggered[0]['prop_id'].startswith('calib'),
        callback_context.triggered[0]['prop_id'].startswith('portcurve'),
        callback_context.triggered[0]['prop_id'].startswith('contour'),
        callback_context.triggered[0]['prop_id'].startswith('bench'),
        callback_context.triggered[0]['prop_id'].startswith('hovermode'),
        callback_context.triggered[0]['prop_id'].startswith('perf_graph_ticker')
            ]
    if tickers:
        toexclude = [t for t in tickers if t in benchtickers]
        minmaxdates = get_minmaxdates(tickers)
        min_date_allowed = minmaxdates[0]
        max_date_allowed = minmaxdates[1]
        all_sd = [{'label': f"{t}'s startdate", 'value': get_ipodate(t)} for t in tickers]

        '''modify date window'''
        if callback_context.triggered[0]['prop_id'].startswith('datepicker'):
            start_date = pick_start
            end_date = pick_end
            sd_bydd = None
        elif sd_bydd and callback_context.triggered[0]['prop_id'].startswith('sd_bydd'):
            start_date = sd_bydd
            end_date = pick_end
        elif any(nondatetriggers):
            start_date = pick_start
            end_date = pick_end
        else:
            start_date = min_date_allowed
            end_date = max_date_allowed

        df, pricegraphcols, compgraphcols, diffgraphcols, yaxis, yaxis_diff = GrapherHelperFunctions().gen_graph_df(tickers, calib, start_date, end_date, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks)
    else:
        df = pd.DataFrame(data={'date': pd.date_range(benchmarkdata['dow']["earliestdate"], benchmarkdata['dow']["latestdate"]), '$': 0})
        pricegraphcols, compgraphcols, diffgraphcols = '$', '$', '$'
        all_sd = []
        yaxis = '$'
        yaxis_diff = '%'
        min_date_allowed = staticmindate
        max_date_allowed = staticmaxdate
        start_date = min_date_allowed
        end_date = max_date_allowed
        toexclude = []

    fig, fig_diff, fig_comp = GrapherHelperFunctions().gen_graph_fig(df, pricegraphcols, diffgraphcols, compgraphcols, hovermode, yaxis, yaxis_diff)
    return fig, fig_diff, fig_comp, df.to_dict('records'), all_sd, min_date_allowed, max_date_allowed, start_date, end_date, [
            html.Span("Min Date Allowed: "),
            html.Span(min_date_allowed, className='fadedpurple_txt'),
            html.Span(" | Max Date Allowed: "),
            html.Span(max_date_allowed, className='fadedpurple_txt')
            ], sd_bydd, [{'label': benchmarksinfo[k]['name'], 'value': benchmarksinfo[k]['ticker'], 'disabled': benchmarksinfo[k]['ticker'] in toexclude} for k in benchmarksinfo]


# sort raw data table
@app.callback(
    Output(f"rawdata_{bp.botid}", "data"),
    Input(f"rawdata_{bp.botid}", 'sort_by'),
    Input(f"rawdata_{bp.botid}", "data"),
    Input(f"graphdf_{bp.botid}", "data")
    )
def sort_rawdatatable(sort_by, rawdatatable, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, rawdatatable, sourcetable).to_dict('records')


# get volstats
@app.callback(
    Output(f"voltable_{bp.botid}", "data"),
    Output(f"voltable_{bp.botid}", "tooltip_header"),
    Input(f'voltbutton_{bp.botid}', "n_clicks"),
    State(f"perf_graph_ticker_{bp.botid}", "value"),
    State(f"portcurve_{bp.botid}", "value"),
    State(f"bench_{bp.botid}", 'value'),
    State(f"voltable_{bp.botid}", 'sort_by'),
    State(f"voltable_{bp.botid}", "data"),
    State(f"graphdf_{bp.botid}", "data"),
    prevent_initial_call=True,
    )
def gen_volstats(n_clicks, ticker, portcurve, bench, sort_by, voldata, graphdfdata):
    if ticker:
        return VolStatFunctions().gen_volstats(ticker, portcurve, bench, sort_by, voldata, graphdfdata)
    else:
        return pd.DataFrame(data=['No data.']).to_dict('records'), None
