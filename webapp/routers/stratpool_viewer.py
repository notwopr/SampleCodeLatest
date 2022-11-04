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
import datetime as dt
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
from webapp.servernotes import get_minmaxdates
from newbacktest.stratpools.db_stratpool import StratPoolDatabase
from newbacktest.baking.baker_stratpool import Baker
from ..graphing.grapher import GraphAssets
from ..graphing.grapher_helper_functions import GrapherHelperFunctions
from ..graphing.grapher_helper_volstats import VolStatFunctions
from machinesettings import _machine

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
        'date': None,
        'min_date_allowed': staticmindate,
        'max_date_allowed': staticmaxdate
        },
    {
        'id': f'randomize_{bp.botid}',
        'prompt': 'Randomize date instead?',
        'buttontext': 'Randomize date',
        'inputtype': 'button_submit'
        },
    {
        'id': f'stratpooldate_{bp.botid}',
        'prompt': 'Pick a date.',
        'inputtype': 'dropdown',
        'placeholder': 'Choose a key to explore',
        'options': [],
        'value': "",
        'multi': False,
        'searchable': False,
        'clearable': False
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
        ])
])


# get possible dates
@app.callback(
    Output(f'stratpooldate_{bp.botid}', "options"),
    Input(f'strat_{bp.botid}', "value"),
    )
def gen_dates(strat):
    if strat:
        return [{'label': k, 'value': k} for k in StratPoolDatabase().view_database()['data'][strat].keys()]
    else:
        return []


# gen messaging
@app.callback(
    Output(f'preview_{bp.botid}', "children"),
    Output(f'output_{bp.botid}', "children"),
    Input(f"stratpoolsourcetable_{bp.botid}", "data"),
    Input(f'strat_{bp.botid}', "value"),
    Input(f'datepicker_single_{bp.botid}', "date"),
    Input(f'stratpooldate_{bp.botid}', "value"),
    Input(f'perf_graph_ticker_{bp.botid}', 'options'),
    )
def messenger(stratpool, stratcode, datepicker, dropdowndate, tickerlist):
    invest_startdate = dropdowndate if dropdowndate != "" else datepicker if not None else None
    if stratcode and invest_startdate and callback_context.triggered[0]['prop_id'].startswith('submitbutton_'):
        message = 'Stratpool is being generated.'
    elif stratpool and stratcode and invest_startdate and not callback_context.triggered[0]['prop_id'].startswith('submitbutton_'):
        if tickerlist:
            message = 'Stratpool generated.'
        if not tickerlist:
            message = 'Strategy run but all stocks were filtered out.'
    elif stratcode and invest_startdate:
        message = 'Ready to generate stratpool.'
    else:
        message = 'Test was not run.  Please provide both a strategy and a date.'

    setting_summary = [
        f'strategy: {stratcode}',
        f'date: {invest_startdate}'
        ]
    setting_summary = html.P([
        html.Span(f'strategy: {stratcode}'),
        html.Br(),
        html.Span(f'date: {invest_startdate}'),
        html.Br(),
        ])

    return setting_summary, message


# gen fullranking sourcetable
@app.callback(
    Output(f"stratpoolsourcetable_{bp.botid}", "data"),
    Output(f'perf_graph_ticker_{bp.botid}', 'options'),
    Output(f'perf_graph_ticker_{bp.botid}', 'value'),
    Output(f'strat_{bp.botid}', "options"),
    Output(f'stratpooldate_{bp.botid}', "value"),
    Output(f'datepicker_single_{bp.botid}', "date"),
    Output(f'datepicker_single_{bp.botid}', "disabled"),
    Output(f'randomize_{bp.botid}', "disabled"),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    Input(f'strat_{bp.botid}', "value"),
    Input(f'datepicker_single_{bp.botid}', "date"),
    Input(f'randomize_{bp.botid}', "n_clicks"),
    Input(f'stratpooldate_{bp.botid}', "value"),
    )
def run_stratreporter(submit, stratcode, datepicker, randomize, dropdowndate):
    if _machine.machinename == 'awsbeanstalk':
        datepickerdisabled = True
        randomizerdisabled = True
    else:
        datepickerdisabled = False
        randomizerdisabled = False

    if callback_context.triggered[0]['prop_id'].startswith('stratpooldate'):
        datepicker = None
        dropdowndate = dropdowndate
    elif callback_context.triggered[0]['prop_id'].startswith('datepicker_single'):
        datepicker = datepicker
        dropdowndate = ""
    elif callback_context.triggered[0]['prop_id'].startswith('randomize'):
        datepicker = random_dates(staticmindate, staticmaxdate, 1)[0]
        dropdowndate = ""
    elif callback_context.triggered[0]['prop_id'].startswith('strat_'):
        datepicker = None
        dropdowndate = None
    else:
        datepicker = datepicker
        dropdowndate = dropdowndate

    invest_startdate = dropdowndate if dropdowndate != "" else datepicker if not None else None
    if stratcode and invest_startdate and callback_context.triggered[0]['prop_id'].startswith('submitbutton_'):
        check = StratPoolDatabase().view_stratpool(stratcode, invest_startdate)
        if check:
            stratpooldf = check.itemdata
        else:
            Baker()._bake_strategy(stratcode, invest_startdate)
            stratpooldf = StratPoolDatabase().view_stratpool(stratcode, invest_startdate).itemdata
        tickerlist = stratpooldf['stock'].tolist()
        stratpool = stratpooldf.to_dict('records')
    else:
        stratpool = None
        tickerlist = []

    stratoptions = [{'label': k, 'value': k} for k in StratPoolDatabase().view_database()['data'].keys()]

    return stratpool, tickerlist, None, stratoptions, dropdowndate, datepicker, datepickerdisabled, randomizerdisabled


# gen and sort fullranking
@app.callback(
    Output(f'result_table_{bp.botid}', 'data'),
    Input(f"result_table_{bp.botid}", 'data'),
    Input(f"result_table_{bp.botid}", 'sort_by'),
    Input(f"stratpoolsourcetable_{bp.botid}", "data"),
    )
def gen_sort_fullranking(displaytable, sort_by, sourcetable):
    if sourcetable:
        return DataTableOperations().return_sortedtable(sort_by, callback_context, displaytable, sourcetable).to_dict('records')
    else:
        return None


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


# gen performance graphs
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
    Output(f"dfcol_{bp.botid}", "children"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f'datepicker_single_{bp.botid}', "date"),
    Input(f'stratpooldate_{bp.botid}', "value"),
    Input(f"calib_{bp.botid}", "value"),
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
    Input(f"hovermode_{bp.botid}", 'value'),
    Input(f"dfcol_{bp.botid}", "children"),
    )
def gen_graph(tickers, invest_startdate, dropdowndate, calib, sd_bydd, pick_start, pick_end, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode, dfcol):
    if tickers:
        minmaxdates = get_minmaxdates(tickers)
        min_date_allowed = minmaxdates[0]
        max_date_allowed = str(min([dt.date.fromisoformat(minmaxdates[1]), dt.date.fromisoformat(dropdowndate if dropdowndate != "" else invest_startdate)]))
    else:
        min_date_allowed = staticmindate
        max_date_allowed = staticmaxdate
    return GrapherHelperFunctions().gen_graph_output(callback_context, tickers, min_date_allowed, max_date_allowed, sd_bydd, pick_start, pick_end, calib, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode, dfcol)


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
    Output(f"voltablesource_{bp.botid}", "data"),
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


# sort volatility table
@app.callback(
    Output(f"voltable_{bp.botid}", "data"),
    Input(f"voltable_{bp.botid}", 'sort_by'),
    Input(f"voltable_{bp.botid}", "data"),
    Input(f"voltablesource_{bp.botid}", "data")
    )
def sort_volatilitytable(sort_by, finaltable, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, finaltable, sourcetable).to_dict('records')
