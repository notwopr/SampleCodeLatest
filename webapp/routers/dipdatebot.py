"""
Title: Dip Date Bot Endpoint
Date Started: Jan 31, 2022
Version: 1.00
Version Start: Jan 31, 2022
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
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from Modules.referencetools.dipdatevisualizer.DIPDATEVISUALIZER import dipdatevisualizer_dash
from Modules.price_history import grabsinglehistory
from ..os_functions import get_currentscript_filename
from ..common_resources import tickers
from ..dashinputs import prompt_builder, gen_tablecontents, dash_inputbuilder
from ..datatables import DataTableOperations
from Modules.dates import DateOperations
from Modules.timeperiodbot import random_dates
from formatting import formatting_schema

dccgraph_config = formatting_schema['dccgraph_config']
figure_layout_mastertemplate = formatting_schema['figure_layout_mastertemplate']

bp = BotParams(
    get_currentscript_filename(__file__),
    'Dip Date Bot',
    "The Dip Date Bot takes a ticker symbol and date range and returns info on the largest drop in price during that span of time, including the exact dates of the fall, and the price change.",
    dipdatevisualizer_dash
)

tbodydata = [
    {
        'id': f'ticker_{bp.botid}',
        'prompt': 'Choose a single ticker.',
        'inputtype': 'dropdown',
        'options': tickers,
        'placeholder': 'Select or Type a Ticker',
        'searchable': True,
        'clearable': True
        },
    {
        'id': f'datepicker_{bp.botid}',
        'prompt': 'Select a date range.',
        'inputtype': 'datepicker_range',
        'clearable': True
        },
    {
        'id': f'randomize_{bp.botid}',
        'prompt': 'Randomize dates instead?',
        'buttontext': 'Randomize dates',
        'inputtype': 'button_submit'
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
        html.Table(gen_tablecontents(tbodydata)),
        prompt_builder({
            'id': f'submitbutton_{bp.botid}',
            'inputtype': 'button_submit',
            }),
    ], id=f'input_{bp.botid}'),
    html.Br(),
    html.Div([
        'Ticker: ', html.Span(id=f'displayinput_ticker_{bp.botid}'),
        html.Br(),
        'Start date: ', html.Span(id=f'displayinput_sd_{bp.botid}'),
        html.Br(),
        'End date: ', html.Span(id=f'displayinput_ed_{bp.botid}'),
    ]),
    html.Div(id=f'readystatus_{bp.botid}'),
    html.Br(),
    html.Strong(html.P(id=f'dipreport_{bp.botid}')),
    dcc.Graph(id=f'dipgraph_{bp.botid}', config=dccgraph_config),
    dash_inputbuilder({
        'inputtype': 'table',
        'id': f"dipchart_{bp.botid}"
        }),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"dipchartsource_{bp.botid}"
        }), hidden='hidden')
])


# update min and max dates and randomize dates if requested
@app.callback(
    Output(f'datepicker_{bp.botid}', "min_date_allowed"),
    Output(f'datepicker_{bp.botid}', "max_date_allowed"),
    Output(f'datepicker_{bp.botid}', "start_date"),
    Output(f'datepicker_{bp.botid}', "end_date"),
    Input(f'ticker_{bp.botid}', "value"),
    Input(f'randomize_{bp.botid}', "n_clicks"),
    State(f'datepicker_{bp.botid}', "min_date_allowed"),
    State(f'datepicker_{bp.botid}', "max_date_allowed"))
def get_minmaxdates(ticker, n_clicks, min_date, max_date):
    if ticker:
        df = grabsinglehistory(ticker)
        min_date_allowed = df['date'].min()
        max_date_allowed = df['date'].max()
        if min_date and max_date:
            new_start = random_dates(min_date, max_date, 1)[0]
            new_end = random_dates(DateOperations().plusminusdays(new_start, 1), max_date, 1)[0]
        else:
            new_start = None
            new_end = None
        return min_date_allowed, max_date_allowed, new_start, new_end
    else:
        min_date_allowed = None
        max_date_allowed = None
        new_start = None
        new_end = None
    return min_date_allowed, max_date_allowed, new_start, new_end


# show inputs selected
@app.callback(
    Output(f'displayinput_ticker_{bp.botid}', 'children'),
    Output(f'displayinput_sd_{bp.botid}', 'children'),
    Output(f'displayinput_ed_{bp.botid}', 'children'),
    Output(f'readystatus_{bp.botid}', 'children'),
    Input(f'ticker_{bp.botid}', "value"),
    Input(f'datepicker_{bp.botid}', 'start_date'),
    Input(f'datepicker_{bp.botid}', 'end_date')
    )
def show_selected_inputs(ticker, start_date, end_date):
    if ticker and start_date and end_date:
        status = "Ready to submit!"
    else:
        status = "Please select a ticker and date range."
    return ticker, start_date, end_date, status


# gen dipreport and dipchart source
@app.callback(
    Output(f'dipreport_{bp.botid}', 'children'),
    Output(f'dipchartsource_{bp.botid}', 'data'),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    State(f'ticker_{bp.botid}', "value"),
    State(f'datepicker_{bp.botid}', 'start_date'),
    State(f'datepicker_{bp.botid}', 'end_date')
    )
def get_dipchart(n_clicks, ticker, start_date, end_date):
    if ticker and start_date and end_date:
        dipreport, df = bp.botfunc(ticker, start_date, end_date)
        tabledata = df.to_dict('records')
        return dipreport, tabledata
    else:
        return None, None


# gen and sort dipchart
@app.callback(
    Output(f'dipchart_{bp.botid}', 'data'),
    Input(f"dipchart_{bp.botid}", 'data'),
    Input(f"dipchart_{bp.botid}", 'sort_by'),
    Input(f"dipchartsource_{bp.botid}", "data"),
    )
def gen_sort_dipchart(dipchart, sort_by, dipchartsource):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, dipchart, dipchartsource).to_dict('records')


# gen graph
@app.callback(
    Output(f'dipgraph_{bp.botid}', 'figure'),
    Input(f"hovermode_{bp.botid}", 'value'),
    Input(f"dipchartsource_{bp.botid}", 'data')
    )
def gen_dipgraph(hovermode, dipchartsource):
    if dipchartsource:
        df = pd.DataFrame.from_records(dipchartsource)
        yaxes = [i for i in df.columns[1:] if i not in ['pctdrops', 'lowestprice']]
        fig = px.line(df, x='date', y=yaxes, markers=False, template=figure_layout_mastertemplate)

    else:
        fig = px.line(pd.DataFrame(data=[0]), template=figure_layout_mastertemplate)
    fig.update_layout(yaxis_title="$", legend_title_text='Ticker', hovermode=hovermode)
    fig.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
    return fig
