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
#   THIRD PARTY IMPORTS
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dashappobject import app
import plotly.express as px
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
# from Modules.referencetools.dipdatevisualizer.DIPDATEVISUALIZER import dipdatevisualizer_dash
# from Modules.price_history import grabsinglehistory
from ..os_functions import get_currentscript_filename
# from ..common_resources import tickers
from ..dashinputs import prompt_builder, gen_tablecontents, dash_inputbuilder
from ..datatables import DataTableOperations
# from Modules.dates import DateOperations
# from Modules.timeperiodbot import random_dates
from newbacktest.cloudgrapher.cloudgrapher_data import CloudGrapherData
from newbacktest.symbology.cloudsampcode import CloudSampCode
from newbacktest.datasource import DataSource
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.growthcalculator import GrowthCalculator
from newbacktest.symbology.investplancode import InvestPlanCode
from formatting import format_tabs
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater import PerfProfileUpdater
from newbacktest.perfmetrics.perfmetrics_ranker_schemas import rank_schemas
from newbacktest.perfmetrics.perfmetrics_ranker import PerfMetricRanker

bp = BotParams(
    get_currentscript_filename(__file__),
    'Strat Ranker 2',
    "Simpler interface to view all samples generated and rankings and aggregations.",
    None
)

tbodydata = []
layout = html.Div([
    html.Div([
        html.Table(gen_tablecontents(tbodydata)),
        html.Span([html.B('Enter your stake:')]),
        dash_inputbuilder({
            'id': f'startcapital_{bp.botid}',
            'prompt': 'Enter your stake',
            'placeholdertext': '$',
            'inputtype': 'number',
            'min': 1
            }),
        html.Span([html.B('Hover Options:')]),
        dash_inputbuilder({
            'id': f'hovermode_{bp.botid}',
            'prompt': 'Choose how you want to display data when you hover over the graph.',
            'inputtype': 'radio',
            'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
            'value': 'x',
            'inline': 'inline'
            })
    ], id=f'input_{bp.botid}'),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Rankings', children=[
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
        ], id=f'rankingtab_{bp.botid}', className=format_tabs),
        dcc.Tab(label='All Samples', children=[
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"sampleschart_{bp.botid}",
                # 'filtering': 'native'
                }),
            html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"sampleschartsource_{bp.botid}"
                }), hidden='hidden')
        ], id=f'sampletab_{bp.botid}', className=format_tabs)
        ])
])


# gen sample source
@app.callback(
    Output(f'sampleschartsource_{bp.botid}', 'data'),
    Input(f"startcapital_{bp.botid}", 'value')
    )
def get_samplesource(stake):
    perfmetricdf = PerfProfileUpdater().get_samplesdf()
    tabledata = perfmetricdf.to_dict('records')
    return tabledata


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


# # gen graph
# @app.callback(
#     Output(f'cloudgraph_{bp.botid}', 'figure'),
#     Input(f"cloudchartsource_{bp.botid}", 'data'),
#     Input(f"startcapital_{bp.botid}", 'value'),
#     Input(f"hovermode_{bp.botid}", 'value')
#     )
# def gen_cloudgraph(cloudchartsource, stake, hovermode):
#
#     if cloudchartsource:
#         df = pd.DataFrame.from_records(cloudchartsource)
#         yaxes = [i for i in df.columns[1:]]
#         fig = px.line(df, x='Days Invested', y=yaxes, markers=False)
#
#     else:
#         fig = px.line(pd.DataFrame(data=[0]))
#     yaxis = '%'
#     if stake:
#         yaxis = '$'
#     fig.update_layout(transition_duration=500, yaxis_title=yaxis, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
#     fig.update_traces(connectgaps=True)
#     return fig
