"""
Title: Strat Ranker 2
Date Started: Oct 16, 2022
Version: 1.00
Version Start: Oct 16, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
import os
#   THIRD PARTY IMPORTS
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from dashappobject import app
import plotly.express as px
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from ..os_functions import get_currentscript_filename
from ..dashinputs import dash_inputbuilder
from ..datatables import DataTableOperations
from formatting import formatting_schema
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater import PerfProfileUpdater
from newbacktest.perfmetrics.perfmetrics_ranker_schemas import rank_schemas
from newbacktest.perfmetrics.perfmetrics_ranker import PerfMetricRanker
from webapp.servernotes import getlastmodified
from file_hierarchy import DirPaths, FileNames
from file_functions import readpkl, join_str
from webapp.routers.strat_ranker_2_helper_grapher import StratRankerGrapher
from webapp.routers.strat_ranker_2_helper_stakefigures import StakeFigures
from machinesettings import _machine

format_tabs = formatting_schema['format_tabs']
helpful_note_value = formatting_schema['helpful_note_value']
helpful_note_key = formatting_schema['helpful_note_key']
dccgraph_config = formatting_schema['dccgraph_config']
figure_layout_mastertemplate = formatting_schema['figure_layout_mastertemplate']

bp = BotParams(
    get_currentscript_filename(__file__),
    'Strat Ranker 2',
    "Simpler interface to view all samples generated and rankings and aggregations.",
    None
)

sampdfpath = Path(join_str([DirPaths().dbparent, f"{FileNames().fn_allsampsdf}.pkl"]))


def get_lastsampupdate():
    if os.path.exists(sampdfpath):
        return getlastmodified(Path(DirPaths().dbparent), f"{FileNames().fn_allsampsdf}.pkl")#[:10]
    else:
        return 'Never.'


layout = html.Div([
    html.Div([
        dash_inputbuilder({
            'id': f'updatesamps_{bp.botid}',
            'buttontext': 'Update Samples',
            'inputtype': 'button_submit'
            }),
        html.Span(id=f'featurestatus_{bp.botid}', className='text-warning'),
        html.Br(),
        html.P([html.Small('Samples last updated: ', className=helpful_note_key), html.Small(id=f'lastupdate_{bp.botid}', className=helpful_note_value)]),
        html.Br()
    ], id=f'input_{bp.botid}'),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(html.Div([
            html.Div([
                html.B('Choose which strats to hide/show.'),
                dash_inputbuilder({
                    'id': f'hidestrat_{bp.botid}',
                    'inputtype': 'dropdown',
                    'options': [],
                    'value': [],
                    'multi': True,
                    'searchable': False,
                    'clearable': False
                    }),
                html.Br(),
                html.Span([html.B('Enter your stake (optional). '), html.Span("If you enter a stake, you also must enter the number of days for which you want to invest that stake.")]),
                dash_inputbuilder({
                    'id': f'startcapital_{bp.botid}',
                    'prompt': 'Enter your stake (optional).',
                    'placeholdertext': '$',
                    'inputtype': 'number',
                    'min': 1
                    }),
                html.Br(),
                html.Div([
                    html.Span([html.B('Enter the investment period. '), html.Span("Enter the number of days (integer) to invest that stake.")]),
                    dash_inputbuilder({
                        'id': f'stakeperiod_{bp.botid}',
                        'prompt': 'Enter the number of days (integer) to invest that stake.',
                        'placeholdertext': 'integers >= 1 only',
                        'inputtype': 'number',
                        'min': 1,
                        'step': 1
                        })], id=f'stakeperiod_div_{bp.botid}'),
                html.Br(),
                html.Span([html.B('Hover Options:')]),
                dash_inputbuilder({
                    'id': f'hovermode_{bp.botid}',
                    'inputtype': 'radio',
                    'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
                    'value': 'closest',
                    'inline': 'inline'
                    }),
                html.Br(),
                dcc.Tabs([
                    dcc.Tab(html.Div([
                        html.B('Choose graph style.'),
                        dash_inputbuilder({
                            'id': f'chart_type_{bp.botid}',
                            'inputtype': 'radio',
                            'options': [{'label': x, 'value': x} for x in [
                                'Scatter',
                                'Box',
                                'Violin']
                                ],
                            'value': 'Scatter',
                            'inline': 'inline'
                            }),
                        dcc.Graph(id=f"rankmetricgraph_{bp.botid}", config=dccgraph_config)
                        ], className=format_tabs), label='Distribution Graph'),
                    dcc.Tab(html.Div(dcc.Graph(id=f"profilegraph_{bp.botid}", config=dccgraph_config), className=format_tabs), label='Profile Graph'),
                    dcc.Tab(html.Div(dcc.Graph(id=f"abovegraph_{bp.botid}", config=dccgraph_config), className=format_tabs), label='Above Graph')
                ])
            ], id=f'displayresult_{bp.botid}')], className=format_tabs), label='Visuals'),
        dcc.Tab(html.Div([
            html.Span([html.B('Select a Ranking Schema:')]),
            dash_inputbuilder({
                'id': f'rankingschema_{bp.botid}',
                'prompt': 'Select a Ranking Schema',
                'inputtype': 'dropdown',
                'options': [{'label': k, 'value': k} for k in rank_schemas.keys()],
                'placeholder': 'Choose a ranking schema',
                'value': 3,
                'multi': False,
                'searchable': False,
                'clearable': True
                }),
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"rankingschart_{bp.botid}",
                # 'filtering': 'native'
                }),
            html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"rankingsource_{bp.botid}"
                }), hidden='hidden')
        ], className=format_tabs), label='Rankings', id=f'rankingtab_{bp.botid}'),
        dcc.Tab(html.Div([
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"sampleschart_{bp.botid}",
                # 'filtering': 'native'
                }),
            html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"sampleschartsource_{bp.botid}"
                }), hidden='hidden')
        ], className=format_tabs), label='All Samples', id=f'sampletab_{bp.botid}')
        ])
])


# update stock data
@app.callback(
    Output(f'updatesamps_{bp.botid}', 'disabled'),
    Output(f'featurestatus_{bp.botid}', 'children'),
    Input(f'updatesamps_{bp.botid}', 'n_clicks'),
    )
def update_updatesampbutton(n_clicks):
    if _machine.machinename == 'awsbeanstalk':
        return True, 'Feature disabled.'
    else:
        return False, None


# gen sample source
@app.callback(
    Output(f'sampleschartsource_{bp.botid}', 'data'),
    Output(f'lastupdate_{bp.botid}', 'children'),
    Output(f"hidestrat_{bp.botid}", 'options'),
    Output(f"hidestrat_{bp.botid}", 'value'),
    # Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"updatesamps_{bp.botid}", 'n_clicks')
    )
def get_samplesource(updatesamps):
    if updatesamps or not os.path.exists(sampdfpath):
        perfmetricdf = PerfProfileUpdater().get_samplesdf()
    else:
        perfmetricdf = readpkl(FileNames().fn_allsampsdf, Path(DirPaths().dbparent))
    tabledata = perfmetricdf.to_dict('records')
    hidestrat_options = [{'label': x, 'value': x} for x in set(perfmetricdf['stratipcode'])]
    hidestrat_values = list(set(perfmetricdf['stratipcode']))
    return tabledata, get_lastsampupdate(), hidestrat_options, hidestrat_values


# gen and sort samples chart
@app.callback(
    Output(f'sampleschart_{bp.botid}', 'data'),
    Output(f'sampleschart_{bp.botid}', 'columns'),
    Input(f"sampleschart_{bp.botid}", 'data'),
    Input(f"sampleschart_{bp.botid}", 'sort_by'),
    Input(f"sampleschartsource_{bp.botid}", "data"),
    )
def gen_sort_sampleschart(sampleschart, sort_by, sampleschartsource):
    return DataTableOperations().return_sortedtable_and_makecolhideable(sort_by, callback_context, sampleschart, sampleschartsource)


# gen ranker source
@app.callback(
    Output(f'rankingsource_{bp.botid}', 'data'),
    Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"sampleschartsource_{bp.botid}", "data"),
    Input(f'rankingschema_{bp.botid}', "value"),
    )
def get_rankersource(stake, sampleschartsource, rankschema):
    perfmetricdf = pd.DataFrame.from_records(sampleschartsource)
    rankdf = PerfMetricRanker().gen_rankdf_addperfmetricdf(perfmetricdf, rank_schemas[rankschema])
    tabledata = rankdf.to_dict('records')
    return tabledata


# gen and sort ranker chart
@app.callback(
    Output(f'rankingschart_{bp.botid}', 'data'),
    Output(f'rankingschart_{bp.botid}', 'columns'),
    Input(f"rankingschart_{bp.botid}", 'data'),
    Input(f"rankingschart_{bp.botid}", 'sort_by'),
    Input(f"rankingsource_{bp.botid}", "data"),
    )
def gen_sort_rankerchart(rankingschart, sort_by, rankingsource):
    return DataTableOperations().return_sortedtable_and_makecolhideable(sort_by, callback_context, rankingschart, rankingsource)


# gen graph
@app.callback(
    Output(f'rankmetricgraph_{bp.botid}', "figure"),
    Output(f'profilegraph_{bp.botid}', "figure"),
    Output(f'abovegraph_{bp.botid}', "figure"),
    Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"stakeperiod_{bp.botid}", 'value'),
    Input(f"hidestrat_{bp.botid}", 'value'),
    Input(f"chart_type_{bp.botid}", "value"),
    Input(f"hovermode_{bp.botid}", 'value'),
    Input(f"sampleschartsource_{bp.botid}", "data"),
    )
def gen_graph(stake, stakeperiod, hidestrat, chart_type, hovermode, sampleschartsource):
    basedf = pd.DataFrame.from_records(sampleschartsource)
    bdf = basedf[[c for c in basedf.columns if c not in ['invest_startdate', 'invest_enddate']]]
    bdf = bdf[bdf['stratipcode'].isin(hidestrat)]
    if len(bdf) == 0:
        rank_fig = px.line(x=None, y=None, template=figure_layout_mastertemplate)
        prof_fig = px.line(x=None, y=None, template=figure_layout_mastertemplate)
        above_fig = px.line(x=None, y=None, template=figure_layout_mastertemplate)
        return rank_fig, prof_fig, above_fig
    else:
        if stake and stakeperiod:
            StakeFigures().add_stakefigures(stake, stakeperiod, bdf)
        rank_fig = StratRankerGrapher().gen_rank_fig(bdf, chart_type, hovermode)
        prof_fig = StratRankerGrapher().gen_prof_fig(bdf, hovermode)
        above_fig = StratRankerGrapher().gen_above_fig(bdf, hovermode)
        return rank_fig, prof_fig, above_fig
