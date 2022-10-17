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

bp = BotParams(
    get_currentscript_filename(__file__),
    'Cloud Grapher',
    "The Cloud Grapher graphs the growth curves of all trials of all strategies on the same x axis, being the number of days invested.",
    CloudGrapherData
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
                {'label': 'Endpoints Only', 'value': 'epo'}
            ],
            'value': ['pco', 'epo'],
            'inline': 'inline',
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
    dcc.Graph(id=f'cloudgraph_{bp.botid}'),
    dash_inputbuilder({
        'inputtype': 'table',
        'id': f"cloudchart_{bp.botid}"
        }),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"cloudchartsource_{bp.botid}"
        }), hidden='hidden')
])


# gen dipchart source
@app.callback(
    Output(f'cloudchartsource_{bp.botid}', 'data'),
    Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"addbenchmark_{bp.botid}", 'value'),
    Input(f"misc_{bp.botid}", 'value')
    )
def get_cloudchart(stake, benchmarks, misc):
    cloudsampcode = 'CDTG|0$s#::0a:70::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::2a:1::2b:d::2c:percentile.IP.5.360.0.5.2000-10-24'
    df = bp.botfunc().gen_cloudgraph_singlesample(cloudsampcode)
    portcols = [i for i in df.columns if i not in ['date', 'Days Invested', 'portcurve']]

    '''benchmark options'''
    if benchmarks:
        bdf = DataSource().opends('eodprices_bench')
        bdf.ffill(inplace=True)
        bdf = DataFrameOperations().filter_column(bdf, ['date']+benchmarks)
        df = df.join(bdf.set_index('date'), how='left', on="date")
        GrowthCalculator().getnormpricesdf(df, benchmarks)

    '''stake calculations'''
    cso = CloudSampCode().decode(cloudsampcode)
    portsize = InvestPlanCode().decode(cso['ipcode'])['portsize']
    periodlen = InvestPlanCode().decode(cso['ipcode'])['periodlen']
    num_periods = cso['num_periods']
    if stake:
        nonportfoliocurves = ['portcurve'] + benchmarks
        df[nonportfoliocurves] = stake * (1 + df[nonportfoliocurves])
        for p in range(num_periods):
            periodcols = [i for i in df.columns if i.endswith(str(p))]
            periodstake = df['portcurve'].iloc[p * periodlen]
            df[periodcols] = (periodstake / portsize) * (1 + df[periodcols])
    else:
        allcurves = portcols + ['portcurve'] + benchmarks
        df[allcurves] = df[allcurves] * 100

    '''misc options'''
    if misc:
        allcurves = portcols + ['portcurve'] + benchmarks
        if 'pco' in misc:
            df = df[[i for i in df.columns if i not in portcols]]
            allcurves = ['portcurve'] + benchmarks
        if 'epo' in misc:
            df.loc[~df['Days Invested'].isin([i*periodlen for i in range(num_periods+1)]), allcurves] = np.nan
    tabledata = df.to_dict('records')
    return tabledata


# gen and sort cloudchart
@app.callback(
    Output(f'cloudchart_{bp.botid}', 'data'),
    Input(f"cloudchart_{bp.botid}", 'data'),
    Input(f"cloudchart_{bp.botid}", 'sort_by'),
    Input(f"cloudchartsource_{bp.botid}", "data"),
    )
def gen_sort_cloudchart(cloudchart, sort_by, cloudchartsource):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, cloudchart, cloudchartsource).to_dict('records')


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
        yaxes = [i for i in df.columns[1:]]
        fig = px.line(df, x='Days Invested', y=yaxes, markers=False)

    else:
        fig = px.line(pd.DataFrame(data=[0]))
    yaxis = '%'
    if stake:
        yaxis = '$'
    fig.update_layout(transition_duration=500, yaxis_title=yaxis, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant')
    fig.update_traces(connectgaps=True)
    return fig
