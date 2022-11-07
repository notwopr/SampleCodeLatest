"""
Title: Best Letter Bot Endpoint
Date Started: Jan 22, 2022
Version: 1.00
Version Start: Jan 22, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  To provide API endpoint for best letter bot.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import html, callback_context, dcc
from dash.dependencies import Input, Output, State
from dashappobject import app
import plotly.express as px
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..dashinputs import prompt_builder, gen_tablecontents, dash_inputbuilder
from ..botrun_parambuilder import brpb_base
from ..botclasses import BotParams
from Modules.bots.bestletterbot.BESTLETTER_BASE import masterbestletter
from ..os_functions import get_currentscript_filename
from ..datatables import DataTableOperations
from Modules.timeperiodbot import random_dates
from ..common_resources import staticmindate, staticmaxdate
from formatting import format_tabs
from formatting_graphs import dccgraph_config, figure_layout_mastertemplate

bp = BotParams(
    get_currentscript_filename(__file__),
    'Best Letter Bot',
    "The Best Letter Bot ranks the letters of the alphabet based on the growth rates of stocks whose ticker symbols begin with each respective letter as of a given date.  It also calculates how prevalent ticker symbols that begin with each respective letter are.  The ticker symbols considered are all United States NASDAQ and NYSE common stock.",
    masterbestletter
)

tbodydata = [
    {
        'id': f'datepicker_single_{bp.botid}',
        'prompt': 'Choose a date.',
        'inputtype': 'datepicker_single',
        'clearable': True,
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
        html.Table(gen_tablecontents(tbodydata)),
        prompt_builder({
            'id': f'submitbutton_{bp.botid}',
            'inputtype': 'button_submit',
            })
    ], id=f'input_{bp.botid}'),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(html.Div(
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"letterstats_{bp.botid}"
                }), className=format_tabs), label='Statistics'),
        dcc.Tab(
            html.Div([
                html.Span([html.B('Hover Options:')]),
                dash_inputbuilder({
                    'id': f'hovermode_{bp.botid}',
                    'prompt': 'Choose how you want to display data when you hover over the graph.',
                    'inputtype': 'radio',
                    'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
                    'value': 'closest',
                    'inline': 'inline'
                    }),
                dcc.Graph(id=f'output_{bp.botid}', config=dccgraph_config),
                dcc.Graph(id=f'output_pie_{bp.botid}', config=dccgraph_config)
            ], className=format_tabs), label='Visuals')
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


@app.callback(
    Output(f'letterstats_{bp.botid}', "data"),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    State(f'datepicker_single_{bp.botid}', "date"),
    Input(f'letterstats_{bp.botid}', "data"),
    Input(f"letterstats_{bp.botid}", 'sort_by'),
    prevent_initial_call=True
    )
def calc_bestletter(n_clicks, date, dfdata, sort_by):
    if dfdata and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
        df = pd.DataFrame.from_records(dfdata)
        df = DataTableOperations().sort_datatable(sort_by, df)
    else:
        brp = {**brpb_base(bp.botid, 1), **{'presentdate': date}}
        df = bp.botfunc(brp)
    return df.to_dict('records')


@app.callback(
    Output(f'output_{bp.botid}', "figure"),
    Output(f'output_pie_{bp.botid}', "figure"),
    Input(f'letterstats_{bp.botid}', "data"),
    Input(f"hovermode_{bp.botid}", 'value')
    )
def gen_graph(dfdata, hovermode):
    if dfdata:
        df = pd.DataFrame.from_records(dfdata)
        bar_y = [i for i in df.columns[1:] if not i.startswith('Number of Tickers') and not i.startswith('% of Total')]
        bar_x = pie_names = 'First Letter'
        pie_values = df.columns[1]
    else:
        df = pd.DataFrame(data=[0])
        bar_x = pie_names = 0
        bar_y = []
        pie_values = df.columns
    pie_fig = px.pie(df, names=pie_names, values=pie_values, template=figure_layout_mastertemplate)
    fig = px.bar(df, x=bar_x, y=bar_y, barmode='group', template=figure_layout_mastertemplate)
    fig.update_layout(hovermode=hovermode)
    return fig, pie_fig
