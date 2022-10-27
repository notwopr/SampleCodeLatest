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
from webapp.servernotes import getlastmodified
from file_hierarchy import DirPaths, FileNames
from file_functions import readpkl, join_str
from formatting import helpful_note_value, helpful_note_key
from Modules.numbers import twodecp
from Modules.numbers_formulas import func_ending_principal

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
        html.Br(),
        html.P([html.Small('Samples last updated: ', className=helpful_note_key), html.Small(id=f'lastupdate_{bp.botid}', className=helpful_note_value)]),
        html.Br(),
        # html.Span([html.B('Enter your stake:')]),
        # dash_inputbuilder({
        #     'id': f'startcapital_{bp.botid}',
        #     'prompt': 'Enter your stake',
        #     'placeholdertext': '$',
        #     'inputtype': 'number',
        #     'min': 1
        #     }),
        # html.Span([html.B('Hover Options:')]),
        # dash_inputbuilder({
        #     'id': f'hovermode_{bp.botid}',
        #     'prompt': 'Choose how you want to display data when you hover over the graph.',
        #     'inputtype': 'radio',
        #     'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
        #     'value': 'x',
        #     'inline': 'inline'
        #     })
    ], id=f'input_{bp.botid}'),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Visuals', children=[
            html.Div([
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
                html.B('Choose which strats to hide/show.'),
                dash_inputbuilder({
                    'id': f'hidestrat_{bp.botid}',
                    'inputtype': 'dropdown',
                    'options': [],
                    'value': [],
                    'multi': True,
                    'searchable': False,
                    'clearable': False
                    # 'className': 'longchecklist',
                    # 'inline': 'block'
                    }),
                html.Span([html.B('Enter your stake (optional). '), html.Span("If you enter a stake, you also must enter the number of days for which you want to invest that stake.")]),
                dash_inputbuilder({
                    'id': f'startcapital_{bp.botid}',
                    'prompt': 'Enter your stake (optional).',
                    'placeholdertext': '$',
                    'inputtype': 'number',
                    'min': 1
                    }),
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
                html.Span([html.B('Hover Options:')]),
                dash_inputbuilder({
                    'id': f'hovermode_{bp.botid}',
                    'inputtype': 'radio',
                    'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
                    'value': 'closest',
                    'inline': 'inline'
                    }),
                dcc.Graph(id=f"overallstats_{bp.botid}")
            ], id=f'displayresult_{bp.botid}')], className=format_tabs),
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
    Output(f'lastupdate_{bp.botid}', 'children'),
    Output(f"hidestrat_{bp.botid}", 'options'),
    Output(f"hidestrat_{bp.botid}", 'value'),
    Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"updatesamps_{bp.botid}", 'n_clicks')
    )
def get_samplesource(stake, updatesamps):
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
    Output(f'overallstats_{bp.botid}', "figure"),
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
        fig = px.line(x=None, y=None)
        return fig
    else:
        if stake and stakeperiod:
            bdf[
                'Ending Cash ($)'
                ] = bdf[
                    'growthrate_effectivedaily'
                    ].apply(lambda x: twodecp(func_ending_principal(stake, x, stakeperiod)))
            bdf[
                'Ending Cash (Benchmark) ($)'
                ] = bdf[
                    'growthrate_effectivedaily_bestbench'
                    ].apply(lambda x: twodecp(func_ending_principal(stake, x, stakeperiod)))
            bdf[
                'Ending Cash over Benchmark ($)'
                ] = bdf['Ending Cash ($)']-bdf['Ending Cash (Benchmark) ($)']
            bdf[
                'Amount Earned ($)'
                ] = bdf[
                    'Ending Cash ($)'
                    ]-stake
            bdf[
                'Amount Earned (Benchmark) ($)'
                ] = bdf[
                    'Ending Cash (Benchmark) ($)'
                    ]-stake
            bdf[
                'Amount Earned over Benchmark ($)'
                ] = bdf['Amount Earned ($)']-bdf['Amount Earned (Benchmark) ($)']
            bdf[
                'Overall Growth'
                ] = bdf[
                    'Amount Earned ($)'
                    ]/stake
            bdf[
                'Overall Growth (Benchmark)'
                ] = bdf[
                    'Amount Earned (Benchmark) ($)'
                    ]/stake
            bdf[
                'Overall Growth over Benchmark'
                ] = bdf['Overall Growth']-bdf['Overall Growth (Benchmark)']
            bdf[
                'Earned per Day ($)'
                ] = bdf[
                    'Amount Earned ($)'
                    ]/stakeperiod
            bdf[
                'Earned per Day (Benchmark) ($)'
                ] = bdf[
                    'Amount Earned (Benchmark) ($)'
                    ]/stakeperiod
            bdf[
                'Earned per Day over Benchmark ($)'
                ] = bdf['Earned per Day ($)']-bdf['Earned per Day (Benchmark) ($)']
        bdf['sample size'] = bdf['stratipcode'].apply(lambda x: bdf[bdf['stratipcode'] == x]['stratipcode'].count())
        df = pd.melt(bdf, id_vars="stratipcode", value_vars=bdf.columns[1:], var_name='metric', value_name='value')
        df['section'] = df['metric'].apply(lambda x: 'rank metrics' if x != 'sample size' else 'sample size')
        if chart_type == 'Scatter':
            fig = px.scatter(df, x="stratipcode", y="value", color="metric", facet_row="section")
            fig.update_traces(marker=dict(size=12, opacity=0.5))
        elif chart_type == 'Box':
            fig = px.box(df, x="stratipcode", y="value", color="metric", facet_row="section", boxmode="overlay")
        elif chart_type == 'Violin':
            fig = px.violin(df, x="stratipcode", y="value", color="metric", facet_row="section", violinmode="overlay")
        fig.update_yaxes(matches=None)
        #bdf = bdf.drop_duplicates(subset=['stratipcode'])
        #fig.add_bar(x=bdf["stratipcode"], y=bdf['sample size'], name="Sample Size", row=1, col=1)
        fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="grey",
            line_width=2.5)
        # truncate long xtick labels
        fig.update_layout(
            xaxis={
             'tickmode': 'array',
             'tickvals': bdf['stratipcode'].tolist(),
             'ticktext': [(i[:17] + '...') for i in bdf['stratipcode']],
            })
        fig.update_layout(height=1000, transition_duration=500, legend_title_text='Legend', hovermode=hovermode, uirevision='some-constant')
        return fig
