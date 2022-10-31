"""
Title: Strat Reporter
Date Started: Feb 23, 2022
Version: 1.00
Version Start: Feb 23, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dashappobject import app
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from ..os_functions import get_currentscript_filename
from ..dashinputs import gen_tablecontents, prompt_builder, dash_inputbuilder
from ..datatables import DataTableOperations
from ..common_resources import staticmindate, staticmaxdate
from Modules.timeperiodbot import random_dates
from formatting import format_tabs
from webapp.servernotes import getbenchdates
from globalvars import benchmarks
from newbacktest.stratpools.db_stratpool import StratPoolDatabase
from newbacktest.baking.baker_stratpool import Baker
from newbacktest.dataframe_operations import DataFrameOperations
from ..graphing.grapher import GraphAssets
from ..graphing.grapher_helper_functions import GrapherHelperFunctions

benchmarkdata = getbenchdates(benchmarks)
bp = BotParams(
    get_currentscript_filename(__file__),
    'Stratpool Viewer',
    "Given a stock screening strategy and date, returns the resulting stratpool. A stratpool consists of a resulting dataframe of stocks after a given strategy has been applied to the existing stocks as of the date given.  If the strategy is a sorter, then it'll be a ranking.  If the strategy is a filter, it would simply be a list of stocks that satisfied the strategy's filter criteria.",
    None
)

tbodydata = [
    {
        'id': f'strat_{bp.botid}',
        'prompt': 'Select a Strategy to apply.',
        'inputtype': 'dropdown',
        'options': [],
        'placeholder': 'Choose an existing Strat',
        'multi': False,
        'searchable': False,
        'clearable': True
        },
    {
        'id': f'datepicker_single_{bp.botid}',
        'prompt': 'Choose a current date.',
        'inputtype': 'datepicker_single',
        'clearable': True,
        'date': staticmindate,
        'min_date_allowed': staticmindate,
        'max_date_allowed': staticmaxdate
        },
    {
        'id': f'randomize_{bp.botid}',
        'prompt': 'Randomize date instead?',
        'buttontext': 'Randomize date',
        'inputtype': 'button_submit'
        }
]


layout = html.Div([
    html.Div([
        html.Table(gen_tablecontents(tbodydata), style={'width': '100%'}),
        prompt_builder({
            'id': f'submitbutton_{bp.botid}',
            'inputtype': 'button_submit',
            })
    ], id=f'input_{bp.botid}'),
    html.P(id=f'output_{bp.botid}'),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"stratpoolsourcetable_{bp.botid}"
        }), id=f"hidden_{bp.botid}", hidden='hidden'),
    dcc.Tabs([
        dcc.Tab(html.Div(id=f'preview_{bp.botid}', className=format_tabs), label='Input Summary'),
        dcc.Tab(html.Div(
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"result_table_{bp.botid}"
                }), className=format_tabs), label='Full Ranking', id=f'tab_fullranking_{bp.botid}'),
        dcc.Tab(html.Div(GraphAssets(bp).perfgraphtab, className=format_tabs), label='Performance Graph'),
        ]),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"graphdf_{bp.botid}"
        }), id=f"hidden_{bp.botid}", hidden='hidden')
])


# get random date
@app.callback(
    Output(f'datepicker_single_{bp.botid}', "date"),
    Input(f'randomize_{bp.botid}', "n_clicks"),
    prevent_initial_call=True
    )
def randomize_date(n_clicks):
    return random_dates(staticmindate, staticmaxdate, 1)[0]


# get input summary
@app.callback(
    Output(f'preview_{bp.botid}', "children"),
    Output(f'strat_{bp.botid}', "options"),
    Input(f'strat_{bp.botid}', "value"),
    Input(f'datepicker_single_{bp.botid}', "date")
    )
def preview_inputs(strat, date):
    setting_summary = [
        f'strategy: {strat}',
        f'date: {date}'
        ]
    setting_summary = [html.P([html.Div([html.Span(i), html.Br()]) for i in setting_summary])]
    return setting_summary, [{'label': k, 'value': k} for k in StratPoolDatabase().view_database()['data'].keys()]


# gen fullranking sourcetable
@app.callback(
    Output(f'output_{bp.botid}', "children"),
    Output(f"stratpoolsourcetable_{bp.botid}", "data"),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    State(f'strat_{bp.botid}', "value"),
    State(f'datepicker_single_{bp.botid}', "date")
    )
def run_stratreporter(n_clicks, stratcode, invest_startdate):
    if all(i is not None for i in [stratcode, invest_startdate]):
        check = StratPoolDatabase().view_stratpool(stratcode, invest_startdate)
        if check:
            stratpooldf = check.itemdata
        else:
            Baker()._bake_strategy(stratcode, invest_startdate)
            stratpooldf = StratPoolDatabase().view_stratpool(stratcode, invest_startdate).itemdata
        stratpool = stratpooldf.to_dict('records')
        message = 'Stratpool generated.'
    else:
        message = 'Test was not run.'
        stratpool = None
    return message, stratpool


# gen and sort fullranking
@app.callback(
    Output(f'result_table_{bp.botid}', 'data'),
    Input(f"result_table_{bp.botid}", 'data'),
    Input(f"result_table_{bp.botid}", 'sort_by'),
    Input(f"stratpoolsourcetable_{bp.botid}", "data"),
    )
def gen_sort_fullranking(displaytable, sort_by, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, displaytable, sourcetable).to_dict('records')


# generate tickerlist for performance graph
@app.callback(
    Output(f'perf_graph_ticker_{bp.botid}', 'options'),
    Input(f"stratpoolsourcetable_{bp.botid}", "data")
    )
def gen_perf_graph_tickerlist(dfdata):
    return pd.DataFrame.from_records(dfdata)['stock'].tolist() if dfdata else []


@app.callback(
    Output(f"portcurve_{bp.botid}", "options"),
    Output(f"portcurve_{bp.botid}", "value"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value")
    )
def show_portcurve_option(ticker, calib, portcurvevalue):
    return GrapherHelperFunctions().show_portcurve_option(ticker, calib, portcurvevalue)


# gen performance graphs
@app.callback(
    Output(f"perf_graph_{bp.botid}", "figure"),
    Output(f"graphdiff_{bp.botid}", "figure"),
    Output(f"graphcomp_{bp.botid}", "figure"),
    Output(f"graphdf_{bp.botid}", "data"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f'datepicker_single_{bp.botid}', "date"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"contour_{bp.botid}", "value"),
    Input(f"graphcompoptions_{bp.botid}", "value"),
    Input(f"graphdiff_mode_{bp.botid}", "value"),
    Input(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"graphdiff_period_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value"),
    Input(f"bench_{bp.botid}", 'value'),
    Input(f"hovermode_{bp.botid}", 'value')
    )
def gen_graph(tickers, invest_startdate, calib, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode):
    if tickers:
        df, pricegraphcols, compgraphcols, diffgraphcols, new_sd, all_sd, yaxis, yaxis_diff = GrapherHelperFunctions().gen_graph_df(tickers, calib, None, None, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode)
        df = DataFrameOperations().filtered_single(df, '<=', invest_startdate, 'date')
    else:
        df = pd.DataFrame(data={'date': pd.date_range(benchmarkdata['dow']["earliestdate"], benchmarkdata['dow']["latestdate"]), '$': 0})
        pricegraphcols, compgraphcols, diffgraphcols, tickers = '$', '$', '$', '$'
        yaxis = '$'
        yaxis_diff = '%'
    fig, fig_diff, fig_comp = GrapherHelperFunctions().gen_graph_fig(df, pricegraphcols, diffgraphcols, compgraphcols, hovermode, yaxis, yaxis_diff)
    return fig, fig_diff, fig_comp, df.to_dict('records')


# sort raw data table
# sourcetable is a hidden html DIV where orig graphdf is stored to be used by voldf and rawdatatable tab
@app.callback(
    Output(f"rawdata_{bp.botid}", "data"),
    Input(f"rawdata_{bp.botid}", 'sort_by'),
    Input(f"rawdata_{bp.botid}", "data"),
    Input(f"graphdf_{bp.botid}", "data")
    )
def sort_rawdatatable(sort_by, rawdatatable, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, rawdatatable, sourcetable).to_dict('records')


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
#
#
# # get volstats
# @app.callback(
#     Output(f"voltable_{bp.botid}", "data"),
#     Output(f"voltable_{bp.botid}", "tooltip_header"),
#     Input(f"perf_graph_ticker_{bp.botid}", "value"),
#     Input(f"portcurve_{bp.botid}", "value"),
#     Input(f"bench_{bp.botid}", 'value'),
#     Input(f"voltable_{bp.botid}", 'sort_by'),
#     Input(f"voltable_{bp.botid}", "data"),
#     Input(f"graphdf_{bp.botid}", "data")
#     )
# def gen_volstats(ticker, portcurve, bench, sort_by, voldata, sourcetable):
#     return GrapherHelperFunctions().gen_volstats(ticker, portcurve, bench, sort_by, voldata, sourcetable)
