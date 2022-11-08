"""
Title: Cloud Grapher Bot Endpoint
Date Started: Oct 12, 2022
Version: 1.00
Version Start: Oct 12, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from dashappobject import app
import plotly.express as px
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
# from Modules.referencetools.dipdatevisualizer.DIPDATEVISUALIZER import dipdatevisualizer_dash
# from Modules.price_history import grabsinglehistory
from ..os_functions import get_currentscript_filename
# from ..common_resources import tickers
from ..dashinputs import gen_tablecontents, dash_inputbuilder
from ..datatables import DataTableOperations
# from Modules.dates import DateOperations
# from Modules.timeperiodbot import random_dates
from newbacktest.symbology.cloudsampcode import CloudSampCode
from newbacktest.cloudgrapher.db_cloudsample import CloudSampleDatabase
from .cloudgrapher_helper import aggregate_sipcols, gen_clouddf_single
from formatting import formatting_schema

format_tabs = formatting_schema['format_tabs']
dccgraph_config = formatting_schema['dccgraph_config']
figure_layout_mastertemplate = formatting_schema['figure_layout_mastertemplate']

bp = BotParams(
    get_currentscript_filename(__file__),
    'Cloud Grapher',
    "The Cloud Grapher graphs the growth curves of all trials of all strategies on the same x axis, being the number of days invested.",
    None
)

tbodydata = [
]
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
        html.Span([html.B('Add Benchmark Curves:')]),
        dash_inputbuilder({
            'id': f'addbenchmark_{bp.botid}',
            'inputtype': 'checklist',
            'options': [
                {'label': 'Dow Jones', 'value': '^DJI'},
                {'label': 'S&P 500', 'value': '^INX'},
                {'label': 'NASDAQ', 'value': '^IXIC'}
            ],
            'inline': 'inline',
            }),
        html.Span([html.B('Additional Options:')]),
        dash_inputbuilder({
            'id': f'misc_{bp.botid}',
            'inputtype': 'checklist',
            'options': [
                {'label': 'Port Curves Only', 'value': 'pco'},
                {'label': 'Endpoints Only', 'value': 'epo'},
                {'label': 'Group by Stratipcode', 'value': 'sic'}
            ],
            'value': ['pco', 'epo'],
            'inline': 'inline',
            }),
        html.Div([
            html.Span([html.B('Group by Stratipcode Options:')]),
            dash_inputbuilder({
                'id': f'aggmode_{bp.botid}',
                'prompt': 'How do you want to aggregate?',
                'inputtype': 'radio',
                'options': [{'label': 'Aggregate using Mean', 'value': 'mean'},
                            {'label': 'Aggregate using Median', 'value': 'median'}],
                'value': 'mean',
                'inline': 'inline'
                }),
            dash_inputbuilder({
                'id': f'groupby_{bp.botid}',
                'inputtype': 'checklist',
                'options': [
                    {'label': 'Show Standard Deviation Curves', 'value': 'std'}
                ],
                'inline': 'inline'
                })
                ], id=f'groupbydiv_{bp.botid}'),
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
    html.Br(),
    dcc.Tabs([
        dcc.Tab(html.Div(dcc.Graph(id=f"cloudgraph_{bp.botid}", config=dccgraph_config), className=format_tabs), label='Cloud Graph'),
        dcc.Tab(html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"codechart_{bp.botid}"
                }), className=format_tabs), label='Curve Glossary'),
        dcc.Tab(html.Div([
            html.P("(Generates only when 'Group by Stratipcode is checkmarked')", id=f"sipchartinfo_{bp.botid}"),
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"sipchart_{bp.botid}"
                })], className=format_tabs), label='Stratipcode Glossary'),
        dcc.Tab(html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"cloudchart_{bp.botid}"
                }), className=format_tabs), label='Raw Data')
    ]),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"cloudchartsource_{bp.botid}"
        }), hidden='hidden')
])


# hide show extra options
@app.callback(
    Output(f'groupbydiv_{bp.botid}', 'hidden'),
    Input(f"misc_{bp.botid}", 'value')
    )
def update_inputs_growthrate(misc):
    return None if 'sic' in misc else 'hidden'


# gen cloudchart source
@app.callback(
    Output(f'cloudchartsource_{bp.botid}', 'data'),
    Output(f'codechart_{bp.botid}', 'data'),
    Output(f'sipchart_{bp.botid}', 'data'),
    Output(f'sipchartinfo_{bp.botid}', 'hidden'),
    Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"addbenchmark_{bp.botid}", 'value'),
    Input(f"misc_{bp.botid}", 'value'),
    Input(f"aggmode_{bp.botid}", 'value'),
    Input(f"groupby_{bp.botid}", 'value'),
    )
def get_cloudchart(stake, benchmarks, misc, aggmode, groupby):
    sipchartinfo = None
    # gather all cloudsampcodes
    allcloudsampcodes = list(CloudSampleDatabase().view_database().keys())

    '''create ids for stratipcode and cloudsampcode'''
    csc_id = {}
    sic_id = {}
    for i in range(len(allcloudsampcodes)):
        csc = allcloudsampcodes[i]
        if csc not in csc_id.keys():
            csc_id[csc] = len(csc_id)
            sic = CloudSampCode().decode(csc)['stratipcode']
            sic_id[sic] = sic_id.get(sic, []) + [csc_id[csc]]

    '''generate graphdfs for each cloudsampcode'''
    idcodesuffix = '_|_'
    allclouddfs = [gen_clouddf_single(idcodesuffix, misc, stake, benchmarks, csc_id, cloudsampcode) for cloudsampcode in csc_id.keys()]

    '''combine all cloudsampcodedfs together'''
    mdf = pd.concat(allclouddfs, ignore_index=False, axis=1)
    mdf.reset_index(inplace=True)
    mdf.rename(columns={'index': 'Days Invested'}, inplace=True)

    '''aggregate by stratipcode if requested'''
    sipchartdata = []
    if 'sic' in misc:
        sipchartinfo = 'hidden'
        for i, stratipcode in enumerate(sic_id.keys()):
            sicprefix = f'sic{i}'
            sipchartdata.append({'sic_id': sicprefix, 'csc_ids': f"{sic_id[stratipcode]}", 'stratipcode': stratipcode})
            '''aggregate portcurves'''
            aggregate_sipcols(aggmode, groupby, mdf, idcodesuffix, sicprefix, sic_id, 'portcurve', stratipcode)
            '''aggregate benchcurves'''
            for b in benchmarks:
                aggregate_sipcols(aggmode, groupby, mdf, idcodesuffix, sicprefix, sic_id, b, stratipcode)

    '''generate codechart'''
    codedf = pd.DataFrame(data=[{'csc_id': v, 'sampcode': k, 'stratipcode': CloudSampCode().decode(k)['stratipcode']} for k, v in csc_id.items()])
    return mdf.to_dict('records'), codedf.to_dict('records'), pd.DataFrame(data=sipchartdata).to_dict('records'), sipchartinfo


# gen and sort cloudchart
@app.callback(
    Output(f'cloudchart_{bp.botid}', 'data'),
    Output(f'cloudchart_{bp.botid}', 'columns'),
    Input(f"cloudchart_{bp.botid}", 'data'),
    Input(f"cloudchart_{bp.botid}", 'sort_by'),
    Input(f"cloudchartsource_{bp.botid}", "data"),
    )
def gen_sort_cloudchart(cloudchart, sort_by, cloudchartsource):
    return DataTableOperations().return_sortedtable_and_makecolhideable(sort_by, callback_context, cloudchart, cloudchartsource)


# gen graph
@app.callback(
    Output(f'cloudgraph_{bp.botid}', 'figure'),
    Input(f"cloudchartsource_{bp.botid}", 'data'),
    Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"hovermode_{bp.botid}", 'value')
    )
def gen_cloudgraph(cloudchartsource, stake, hovermode):

    if cloudchartsource:
        df = pd.DataFrame.from_records(cloudchartsource)
        yaxes = [i for i in df.columns if not i.endswith('date')]
        fig = px.line(df, x='Days Invested', y=yaxes, markers=False, template=figure_layout_mastertemplate)

    else:
        fig = px.line(pd.DataFrame(data=[0]), template=figure_layout_mastertemplate)
    yaxis = '%'
    if stake:
        yaxis = '$'
    fig.update_layout(yaxis_title=yaxis, legend_title_text='Ticker', hovermode=hovermode)
    fig.update_traces(connectgaps=True)
    return fig
