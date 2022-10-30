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
import time
import copy
from itertools import permutations
#   THIRD PARTY IMPORTS
from dash import dcc, html, callback_context
import plotly.express as px
from dash.dependencies import Input, Output, State
from dashappobject import app
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from ..os_functions import get_currentscript_filename
from ..dashinputs import gen_tablecontents, prompt_builder, dash_inputbuilder
# from ..botrun_parambuilder import brpb_base
# from .strattester_helper_stratpanels import stratlib
# from Modules.strattester.STRAT_REPORTER_BASE import getstratdfandpool
# from newbacktest.module_operations import ModuleOperations
from ..datatables import DataTableOperations
from ..common_resources import staticmindate, staticmaxdate
from Modules.timeperiodbot import random_dates
from formatting import format_tabs
# from Modules.price_history_slicing import pricedf_daterange
# from Modules.price_calib import convertpricearr, add_calibratedprices_portfolio
# from .pricehistoryexplorer_helper_diffcomp import add_comparisons_portfolio, add_pdiffpctchange_portfolio
from webapp.servernotes import getbenchdates
from globalvars import benchmarks
from newbacktest.stratpools.db_stratpool import StratPoolDatabase
from newbacktest.baking.baker_stratpool import Baker
from newbacktest.datasource import DataSource
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.curvecalibrator import CurveCalibrator


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
        'options': [],#[{'label': k, 'value': k} for k in StratPoolDatabase().view_database()['data'].keys()],  # stratlib.keys()],
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
        },
    # {
    #     'id': f'min_age_{bp.botid}',
    #     'prompt': 'Set the minimum age (in days) a stock must be to invest in it. Must be 1 or higher.',
    #     'placeholdertext': 'Enter an integer',
    #     'inputtype': 'number',
    #     'min': 1,
    #     'step': 1
    #     }
]

perf_graph_inputs = [
    {
        'id': f'perf_graph_ticker_{bp.botid}',
        'prompt': 'Select tickers from the full ranking list that you want to see.',
        'inputtype': 'dropdown',
        'options': [],
        'placeholder': 'Select or Search a Ticker(s)',
        'multi': True,
        'searchable': True,
        'clearable': True
        },
    {
        'id': f'calib_{bp.botid}',
        'prompt': 'Select a calibration.  Absolute is where the y-axis is in $.  Normalized is where all prices are standardized to the same scale.',
        'inputtype': 'radio',
        'options': [
            {'label': 'Absolute', 'value': 'absolute'},
            {'label': 'Normalized', 'value': 'normalize'}
        ],
        'value': 'absolute',
        'inline': 'inline'
        },
    {
        'id': f'contour_{bp.botid}',
        'prompt': 'Select whether you want to see the graphs in a different contour.',
        'details': 'Baremax displays the current all-time high price.  Baremin displays the floor price.  Trueline displays the midpoint between baremax and baremin prices.  Straight displays the straight line from first to last price.',
        'inputtype': 'checklist',
        'options': [
            {'label': 'Baremax', 'value': 'baremax'},
            {'label': 'Baremin', 'value': 'baremin'},
            {'label': 'Trueline', 'value': 'true'},
            {'label': 'Straight', 'value': 'straight'}
        ]
        },
    {
        'id': f'graphdiff_mode_{bp.botid}',
        'prompt': 'Periodic difference measures arithmetic difference in value between adjacent periods. Periodic percent change measures the percent change difference between adjacent periods.',
        'inputtype': 'radio',
        'options': [
            {'label': 'Periodic Difference', 'value': 'pdiff'},
            {'label': 'Periodic Percent Change', 'value': 'pctchange'}
        ],
        'value': 'pctchange',
        'inline': 'inline'
        },
    {
        'id': f'graphdiff_changecol_{bp.botid}',
        'prompt': 'Select a calibration you want to compute the periodic change.',
        'inputtype': 'dropdown',
        'options': [],
        'value': 'all',
        'placeholder': 'select calibration',
        'multi': False,
        'searchable': False,
        'clearable': False
        },
    {
        'id': f'graphdiff_period_{bp.botid}',
        'prompt': 'Enter the period (in days) you want differences or percent change to calculated.  For example, period of 1 for mode "Periodic Percent Change" gives you a graph representing the daily percent change of the source calibration.',
        'inputtype': 'number',
        'value': 1,
        'min': 1,
        'step': 1,
        'debounce': True
        },
    {
        'id': f'graphcompoptions_{bp.botid}',
        'prompt': 'Graphs proportion difference between two available calibrations A and B.  Thus, option "A to B" means it will output a graph such that the graph is a representation of (A - B) / B.',
        'inputtype': 'dropdown',
        'options': [],
        'placeholder': 'select comparison',
        'multi': False,
        'searchable': False,
        'clearable': True
        },
    {
        'id': f'bench_{bp.botid}',
        'prompt': 'Select a benchmark to compare against your portfolio.',
        'details': '',
        'inputtype': 'checklist',
        'options': [
            {'label': 'Dow Jones', 'value': '^DJI'},
            {'label': 'S&P 500', 'value': '^INX'},
            {'label': 'NASDAQ', 'value': '^IXIC'}
        ],
        'inline': 'inline'
        },
    {
        'id': f'hovermode_{bp.botid}',
        'prompt': 'Choose how you want to display data when you hover over the graph.',
        'inputtype': 'radio',
        'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
        'value': 'closest',
        'inline': 'inline'
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
        'id': f"sourcetable_{bp.botid}"
        }), id=f"hidden_{bp.botid}", hidden='hidden'),
    dcc.Tabs([
        dcc.Tab([
            html.Div(id=f'preview_{bp.botid}')
        ], label='Input Summary', id=f'tab_preview_{bp.botid}', className=format_tabs),
        dcc.Tab([
            dash_inputbuilder({
                        'inputtype': 'table',
                        'id': f"result_table_{bp.botid}"
                        })
                ], label='Full Ranking', id=f'tab_fullranking_{bp.botid}', className=format_tabs),
        dcc.Tab([
            html.Table(gen_tablecontents(perf_graph_inputs), style={'width': '100%'}),
            dcc.Graph(id=f"perf_graph_{bp.botid}"),
            dcc.Graph(id=f"graphdiff_{bp.botid}"),
            dcc.Graph(id=f"graphcomp_{bp.botid}")
        ], label='Performance Graph', id=f'tab_perf_graph_{bp.botid}', className=format_tabs)
        ])
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
    Input(f'datepicker_single_{bp.botid}', "date"),
    # Input(f'min_age_{bp.botid}', "value")
    )
def preview_inputs(strat, date): #, min_age):
    setting_summary = [
        f'strategy: {strat}',
        f'date: {date}',
        #f'min_age: {min_age} days old'
        ]
    setting_summary = [html.P([html.Div([html.Span(i), html.Br()]) for i in setting_summary])]
    return setting_summary, [{'label': k, 'value': k} for k in StratPoolDatabase().view_database()['data'].keys()]


# gen fullranking sourcetable
@app.callback(
    Output(f'output_{bp.botid}', "children"),
    Output(f"sourcetable_{bp.botid}", "data"),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    State(f'strat_{bp.botid}', "value"),
    State(f'datepicker_single_{bp.botid}', "date"),
    # State(f'min_age_{bp.botid}', "value")
    )
def run_stratreporter(n_clicks, stratcode, invest_startdate):  #, min_age):
    if all(i is not None for i in [stratcode, invest_startdate]):#, min_age]):
        check = StratPoolDatabase().view_stratpool(stratcode, invest_startdate)
        if check:
            stratpooldf = check.itemdata
        else:
            Baker()._bake_strategy(stratcode, invest_startdate)
            stratpooldf = StratPoolDatabase().view_stratpool(stratcode, invest_startdate).itemdata
        stratpool = stratpooldf.to_dict('records')
        message = 'Stratpool generated.'
        # brp = {**brpb_base(bp.botid, 1), **{
        #     'strat_name': strat,
        #     'exist_date': date,
        #     'minimumage': min_age,
        #     'rankmeth': 'standard',
        #     'rankregime': '1isbest'
        # }}
        # retrieve panel data
        # libsourcecopy = copy.deepcopy(stratlib[strat])
        # metriclist = ModuleOperations().getobject_byvarname(libsourcecopy['stages']['Stage 3'][0], libsourcecopy['stages']['Stage 3'][1])
        # libsourcecopy['stages']['Stage 3'] = metriclist
        # brp['strat_panel'] = libsourcecopy
        # start = time.time()
        # df = getstratdfandpool(brp)
        # end = time.time()
        # delete temp files and folder
        #delete_folder(getbotsinglerunfolder(brp['rootdir'], brp['testregimename'], brp['todaysdate'], brp['testnumber']))
        #return f'Run complete. Runtime: {end-start} secs', df.to_dict('records')
    else:
        message = 'Test was not run.'
        stratpool = None
    return message, stratpool


# gen and sort fullranking
@app.callback(
    Output(f'result_table_{bp.botid}', 'data'),
    Input(f"result_table_{bp.botid}", 'data'),
    Input(f"result_table_{bp.botid}", 'sort_by'),
    Input(f"sourcetable_{bp.botid}", "data"),
    )
def gen_sort_fullranking(displaytable, sort_by, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, displaytable, sourcetable).to_dict('records')


# generate tickerlist for performance graph
@app.callback(
    Output(f'perf_graph_ticker_{bp.botid}', 'options'),
    Input(f"sourcetable_{bp.botid}", "data")
    )
def gen_perf_graph_tickerlist(dfdata):
    return pd.DataFrame.from_records(dfdata)['stock'].tolist() if dfdata else []


# ds = DataSource().opends('eodprices')


# gen performance graphs
@app.callback(
    Output(f"perf_graph_{bp.botid}", "figure"),
    Output(f"graphdiff_{bp.botid}", "figure"),
    Output(f"graphcomp_{bp.botid}", "figure"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f'datepicker_single_{bp.botid}', "date"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"contour_{bp.botid}", "value"),
    Input(f"graphcompoptions_{bp.botid}", "value"),
    Input(f"graphdiff_mode_{bp.botid}", "value"),
    Input(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"graphdiff_period_{bp.botid}", "value"),
    Input(f"bench_{bp.botid}", 'value'),
    Input(f"hovermode_{bp.botid}", 'value')
    )
def gen_graph(tickers, invest_startdate, calib, contour, graphcomp, gdm, gdc, gdp, benchmarks, hovermode):
    yaxis = '$'
    if tickers:
        # df = DataSource().opends('eodprices')
        ds = DataSource().opends('eodprices')
        df = DataFrameOperations().filter_column(ds, ['date']+tickers)
        df.ffill(inplace=True)
        df = DataFrameOperations().filtered_single(df, '<=', invest_startdate, 'date')
        df.dropna(inplace=True, how='all', subset=tickers)
        portfolio = tickers.copy()
        df.reset_index(inplace=True, drop=True)
        if benchmarks:
            bdf = DataSource().opends('eodprices_bench')
            bdf.ffill(inplace=True)
            bdf = DataFrameOperations().filter_column(bdf, ['date']+benchmarks)
            df = df.join(bdf.set_index('date'), how='left', on="date")
        tickers.extend(benchmarks)
        if calib == 'normalize':
            CurveCalibrator().normalize_curves(df, 'norm', tickers)
            yaxis = '%'
        CurveCalibrator().add_curvetypes(df, contour, tickers)
        tickers.extend([f'{t}_{c}' for c in contour for t in tickers])
        if graphcomp:
            gc_inputs = graphcomp.split(" ")
            gcomp_portfolio = portfolio+benchmarks
            CurveCalibrator().add_comparison_curves(df, gc_inputs[0], gc_inputs[1], gcomp_portfolio)
            compgraphcols = [f'{s}_{gc_inputs[0]}to{gc_inputs[1]}' for s in gcomp_portfolio]
        else:
            compgraphcols = None
        sourcecols = CurveCalibrator().add_pdiffpctchange_portfolio(df, gdc, gdp, gdm, tickers)
        if gdm == 'pdiff':
            yaxis_diff = '$'
        if gdm == 'pctchange':
            yaxis_diff = '%'
        diffgraphcols = [f'{s}_{gdp}d_{gdm}' for s in sourcecols]
    else:
        df = pd.DataFrame(data={'date': pd.date_range(benchmarkdata['dow']["earliestdate"], benchmarkdata['dow']["latestdate"]), '$': 0})
        compgraphcols, diffgraphcols, tickers = '$', '$', '$'
        yaxis = '$'
        yaxis_diff = '%'
    fig = px.line(df, x='date', y=tickers, markers=False)
    fig.update_layout(transition_duration=500, yaxis_title=yaxis, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
    fig.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
    fig_diff = px.line(df, x='date', y=diffgraphcols, markers=False)
    fig_diff.update_layout(transition_duration=500, yaxis_title=yaxis_diff, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
    fig_diff.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
    fig_comp = px.line(df, x='date', y=compgraphcols, markers=False)
    fig_comp.update_layout(transition_duration=500, yaxis_title='%', legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
    fig_comp.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
    return fig, fig_diff, fig_comp


# # gen performance graphs
# @app.callback(
#     Output(f"perf_graph_{bp.botid}", "figure"),
#     Output(f"graphdiff_{bp.botid}", "figure"),
#     Output(f"graphcomp_{bp.botid}", "figure"),
#     Input(f"perf_graph_ticker_{bp.botid}", "value"),
#     Input(f'datepicker_single_{bp.botid}', "date"),
#     Input(f"calib_{bp.botid}", "value"),
#     Input(f"contour_{bp.botid}", "value"),
#     Input(f"graphcompoptions_{bp.botid}", "value"),
#     Input(f"graphdiff_mode_{bp.botid}", "value"),
#     Input(f"graphdiff_changecol_{bp.botid}", "value"),
#     Input(f"graphdiff_period_{bp.botid}", "value"),
#     Input(f"bench_{bp.botid}", 'value'),
#     Input(f"hovermode_{bp.botid}", 'value')
#     )
# def gen_graph(ticker, date, calib, contour, graphcomp, gdm, gdc, gdp, bench, hovermode):
#     if ticker:
#         portfolio = ticker.copy()
#         df = pricedf_daterange(ticker[0], '', date)
#         for t in ticker[1:]:
#             df = df.join(pricedf_daterange(t, '', date).set_index('date'), how="outer", on="date")
#         df.sort_values(by='date', inplace=True)
#         df.reset_index(inplace=True, drop=True)
#         for b in bench:
#             bdf = pricedf_daterange(b, '', date)
#             bdf.rename(columns={b: f'bench_{b}'}, inplace=True)
#             df = df.join(bdf.set_index('date'), how="left", on="date")
#         ticker += [f'bench_{b}' for b in bench]
#         if calib == 'normalize':
#             df[ticker] = df[ticker].apply(lambda x: convertpricearr(x, 'norm1'))
#         df = add_calibratedprices_portfolio(df, contour, ticker)
#         if len(contour) > 0:
#             ticker += [f'{t}_{c}' for c in contour for t in ticker]
#         if graphcomp:
#             gc_inputs = graphcomp.split(" ")
#             gcomp_portfolio = portfolio+[f'bench_{b}' for b in bench]
#             df = add_comparisons_portfolio(df, gc_inputs[0], gc_inputs[1], gcomp_portfolio)
#             compgraphcols = [f'{s}_{gc_inputs[0]}to{gc_inputs[1]}' for s in gcomp_portfolio]
#         else:
#             compgraphcols = None
#         df, sourcecols = add_pdiffpctchange_portfolio(df, gdc, gdp, gdm, ticker)
#         diffgraphcols = [f'{s}_{gdp}d_{gdm}' for s in sourcecols]
#     else:
#         df = pd.DataFrame(data={'date': pd.date_range(benchmarkdata['dow']["earliestdate"], benchmarkdata['dow']["latestdate"]), '$': 0})
#         compgraphcols, diffgraphcols, ticker = '$', '$', '$'
#     fig = px.line(df, x='date', y=ticker, markers=False)
#     fig.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
#     fig.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
#     fig_diff = px.line(df, x='date', y=diffgraphcols, markers=False)
#     fig_diff.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
#     fig_diff.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
#     fig_comp = px.line(df, x='date', y=compgraphcols, markers=False)
#     fig_comp.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
#     fig_comp.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
#     return fig, fig_diff, fig_comp


# create options for diffgraph and comp graph
@app.callback(
    Output(f"graphcompoptions_{bp.botid}", "options"),
    Output(f"graphcompoptions_{bp.botid}", "value"),
    Output(f"graphdiff_changecol_{bp.botid}", "options"),
    Input(f"contour_{bp.botid}", "value")
    )
def show_diffgraph_options(contour):
    if len(contour) == 0:
        return [], None, ['rawprice']
    else:
        p = permutations(contour + ['rawprice'], 2)
        return [{'label': f'{i[0]} to {i[1]}', 'value': f'{i[0]} {i[1]}'} for i in p], None, ['all', 'rawprice']+contour
