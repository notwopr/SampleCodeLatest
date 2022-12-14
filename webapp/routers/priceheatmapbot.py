"""
Title: Price Heat Map Bot Endpoint
Date Started: Feb 9, 2022
Version: 1.00
Version Start: Feb 9, 2022
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
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from Modules.bots.bpoty.BPOTYBOT_BASE import get_poty_average
from Modules.price_history import grabsinglehistory
from file_functions import delete_folder, getbotsinglerunfolder
from ..os_functions import get_currentscript_filename
from ..common_resources import tickers
from ..dashinputs import gen_tablecontents, dash_inputbuilder
from ..botrun_parambuilder import brpb_base
from ..datatables import DataTableOperations
from Modules.dates import DateOperations
from Modules.timeperiodbot import random_dates
from formatting import formatting_schema

format_tabs = formatting_schema['format_tabs']
dccgraph_config = formatting_schema['dccgraph_config']
figure_layout_mastertemplate = formatting_schema['figure_layout_mastertemplate']

bp = BotParams(
    get_currentscript_filename(__file__),
    'Price Heat Map Bot',
    "The Price Heat Map Bot takes a ticker symbol and date range and returns a heat map of its price change activity.",
    get_poty_average
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
        'prompt': 'Select a date range.  Leave blank if you want to consider the entire date range available.',
        'placeholdertext_sd': 'optional',
        'placeholdertext_ed': 'optional',
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
        'id': f'timechunk_preset_{bp.botid}',
        'prompt': 'The date range will be broken into equal chunks.  Choose whether you want them to be in years, months, or days.  With days, you can select the number of days (from 1 to 366).',
        'inputtype': 'radio',
        'options': [
            {'label': 'Month', 'value': 'month'},
            {'label': 'Year', 'value': 'year'},
            {'label': 'Days', 'value': 'day'}
        ],
        'value': 'month'
        },
    {
        'id': f'timechunk_{bp.botid}',
        'inputtype': 'hidden'
        }
]
layout = html.Div([
    html.Div([
        html.Table(gen_tablecontents(tbodydata)),
        dash_inputbuilder({
            'id': f'submitbutton_{bp.botid}',
            'inputtype': 'button_submit',
            }),
        html.Div(id=f'preview_{bp.botid}')
    ], id=f'input_{bp.botid}'),
    dcc.Tabs([
        dcc.Tab(html.Div([
            html.Span([html.B('Select Graph Type:')]),
            dash_inputbuilder({
                'id': f'graphtype_{bp.botid}',
                'prompt': 'Select Graph Type:',
                'inputtype': 'radio',
                'options': ['2-D', '3-D'],
                'value': '2-D',
                'inline': 'inline'
                }),
            html.Br(),
            dcc.Graph(config=dccgraph_config, id=f'heatmapgraph_{bp.botid}')
        ], className=format_tabs), label='Price Change Heat Map'),
        dcc.Tab(html.Div([
            html.Span([html.B('Select type of average:')]),
            dash_inputbuilder({
                'id': f'average_{bp.botid}',
                'prompt': 'Select type of average.',
                'inputtype': 'radio',
                'options': ['Mean', 'Median'],
                'value': 'Median',
                'inline': 'inline'
                }),
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"chunkranktable_{bp.botid}"
                })
            ], className=format_tabs), label='Time Chunk Ranking'),
        dcc.Tab(html.Div(
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f'rawdata_{bp.botid}'
                }), className=format_tabs), label='Raw Data')
    ]),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"chunkranksource_{bp.botid}"
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


@app.callback(
    Output(f'preview_{bp.botid}', 'children'),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    Input(f'ticker_{bp.botid}', "value"),
    Input(f'datepicker_{bp.botid}', 'start_date'),
    Input(f'datepicker_{bp.botid}', 'end_date'),
    Input(f'timechunk_preset_{bp.botid}', 'value'),
    Input(f'timechunk_{bp.botid}', 'value')
    )
def preview_inputs(n_clicks, ticker, beg_date, end_date, timechunk_preset, timechunk):
    setting_summary = [
        f'n_clicks: {n_clicks}',
        f'ticker: {ticker}',
        f'beg_date: {beg_date}',
        f'end_date: {end_date}',
        f'timechunk_preset: {timechunk_preset}',
        f'timechunk: {timechunk}'
        ]
    setting_summary = [html.P([html.Div([html.Span(i), html.Br()]) for i in setting_summary])]
    if all([ticker, timechunk_preset, (timechunk if timechunk_preset == 'day' else True)]):
        return setting_summary + ['Ready to calculate']
    else:
        return setting_summary + ['Missing inputs']


@app.callback(
    Output(f'chunkranksource_{bp.botid}', 'data'),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    State(f'ticker_{bp.botid}', "value"),
    State(f'datepicker_{bp.botid}', 'start_date'),
    State(f'datepicker_{bp.botid}', 'end_date'),
    State(f'timechunk_preset_{bp.botid}', 'value'),
    State(f'timechunk_{bp.botid}', 'value')
    )
def get_priceheatmap(n_clicks, ticker, beg_date, end_date, timechunk_preset, timechunk):
    if all([ticker, timechunk_preset, (timechunk if timechunk_preset == 'day' else True)]):
        brp = {**brpb_base(bp.botid, 1), **{
            'ticker': ticker,
            'beg_date': beg_date if beg_date is not None else '',
            'end_date': end_date if end_date is not None else '',
            'potylen': timechunk,
            'potydef': timechunk_preset
            }}
        heatmapdf = get_poty_average(brp)
        # delete temp files and folder
        delete_folder(getbotsinglerunfolder(brp['rootdir'], brp['testregimename'], brp['todaysdate'], brp['testnumber']))
    else:
        heatmapdf = pd.DataFrame(data={'Time Chunk': [0], 'YEAR': [0], 'Price Change': [0]})
    return heatmapdf.to_dict('records')


# sort raw data table
@app.callback(
    Output(f"rawdata_{bp.botid}", "data"),
    Input(f"rawdata_{bp.botid}", 'sort_by'),
    Input(f"rawdata_{bp.botid}", "data"),
    Input(f"chunkranksource_{bp.botid}", "data")
    )
def sort_rawdatatable(sort_by, rawdatatable, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, rawdatatable, sourcetable).to_dict('records')


# generate figure depending on type
@app.callback(
    Output(f'heatmapgraph_{bp.botid}', 'figure'),
    Input(f'chunkranksource_{bp.botid}', 'data'),
    Input(f"graphtype_{bp.botid}", "value")
    )
def gen_heatmapgraph(heatmapsource, graphtype):
    heatmapdf = pd.DataFrame.from_records(heatmapsource)
    if graphtype == '2-D':
        fig = px.imshow(
            heatmapdf[heatmapdf.columns[1:]],
            labels=dict(x="Time Chunk", y="Year", color="Price Change"),
            y=heatmapdf['YEAR'],
            text_auto=True,
            aspect="auto",
            height=700, template=figure_layout_mastertemplate)
    elif graphtype == '3-D':
        z = heatmapdf[heatmapdf.columns[1:]]
        sh_0, sh_1 = z.shape
        x, y = heatmapdf.columns[1:], heatmapdf['YEAR']
        fig = go.Figure(
            data=[go.Surface(z=z, x=x, y=y)],
            layout=go.Layout(
                height=700,
                template=figure_layout_mastertemplate
                ))
    fig.update_layout(autosize=True)
    return fig


# show days text input if day radio selected
@app.callback(
    Output(f"timechunk_{bp.botid}", "placeholdertext"),
    Output(f"timechunk_{bp.botid}", "type"),
    Output(f"timechunk_{bp.botid}", "min"),
    Output(f"timechunk_{bp.botid}", "max"),
    Output(f"timechunk_{bp.botid}", "step"),
    Input(f"timechunk_preset_{bp.botid}", "value")
    )
def show_day_input(preset):
    if preset == 'day':
        return '# of days', 'number', 1, 366, 1
    else:
        return None, 'hidden', None, None, None


# generate chunk rank table
@app.callback(
    Output(f'chunkranktable_{bp.botid}', 'data'),
    Input(f'chunkranksource_{bp.botid}', 'data'),
    Input(f'chunkranktable_{bp.botid}', 'data'),
    Input(f'chunkranktable_{bp.botid}', 'sort_by'),
    Input(f"average_{bp.botid}", "value")
    )
def get_chunkranktable(heatmaptable, chunkranktable, sort_by, average):
    if chunkranktable and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
        chunkrankdf = pd.DataFrame.from_records(chunkranktable)
        chunkrankdf = DataTableOperations().sort_datatable(sort_by, chunkrankdf)
        return chunkrankdf.to_dict('records')
    elif heatmaptable:
        chunkrankdf = pd.DataFrame.from_records(heatmaptable)
        if len(chunkrankdf.columns) > 2:
            if average == 'Mean':
                chunkrankdf = chunkrankdf.mean(axis=0)
            elif average == 'Median':
                chunkrankdf = chunkrankdf.median(axis=0)
            chunkrankdf = pd.DataFrame(chunkrankdf)
            chunkrankdf = chunkrankdf.iloc[1:, :]
            chunkrankdf.reset_index(inplace=True)
            chunkrankdf.rename(columns={'index': 'Time Chunk', 0: f'{average} Change'}, inplace=True)
            chunkrankdf.sort_values(ascending=False, by=[f'{average} Change'], inplace=True)
            chunkrankdf.reset_index(drop=True, inplace=True)
            return chunkrankdf.to_dict('records')
        else:
            return heatmaptable
    else:
        return None
