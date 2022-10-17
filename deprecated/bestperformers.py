"""
Title: Best Performers Endpoint
Date Started: Jan 30, 2022
Version: 1.00
Version Start: Jan 30, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
from dashappobject import app
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..dashinputs import prompt_builder, gen_tablecontents, dash_inputbuilder
from ..servernotes import getstockdata
from ..botrun_parambuilder import brpb_base
from file_functions import delete_folder, getbotsinglerunfolder
from ..botclasses import BotParams
from Modules.bots.bestperformers.BESTPERFORMERS_BASE import bestperformer_cruncher
from ..os_functions import get_currentscript_filename
from ..datatables import sort_datatable

bp = BotParams(
    get_currentscript_filename(__file__),
    'Best Performers Bot',
    "The Best Performers Bot finds the best stocks by overall growth for a given period.  The ticker symbols considered are all United States NASDAQ and NYSE common stock.",
    bestperformer_cruncher
)

tbodydata = [
    {
        'id': f'datepicker_{bp.botid}',
        'prompt': 'Specify a date range.',
        'inputtype': 'datepicker_range',
        'clearable': True,
        'min_date_allowed': getstockdata()["earliest"],
        'max_date_allowed': getstockdata()["latest"]
        },
    {
        'id': f'checklist_{bp.botid}',
        'prompt': '',
        'inputtype': 'checklist',
        'options': [
            {'label': 'Compare the results to benchmark indices (Dow, S&P, Nasdaq)', 'value': 'compare'},
            {'label': 'Save your results', 'value': 'save'},
            {'label': 'See growth rates in annualized terms', 'value': 'annualize'},
            {'label': 'Only include stocks that beat the best performing index', 'value': 'beat'}
        ]
        },
    {
        'id': f'marginrate_{bp.botid}',
        'prompt': 'By how much must those stocks beat the best performing index?',
        'details':  "For example, entering 0.15 means you want stocks that perform 15% better than the best performing benchmark index.",
        'placeholdertext': 'Enter margin rate',
        'inputtype': 'number',
        'min': 0
        },
    {
        'id': f'fatscorecap_hip_{bp.botid}',
        'prompt': 'Enter a fatscorecap threshold if you want to filter out stocks that do not meet that threshold over the date range selected.',
        'details':  "[Define fatscorecap and its usefulnesss]",
        'placeholdertext': 'Optional',
        'inputtype': 'number',
        'min': 0
        },
    {
        'id': f'fatscorecap_hip_filter_{bp.botid}',
        'prompt': 'Keep stocks that, over the date range selected, are __ the fatscorecap threshold established above.',
        'details':  "[Define fatscorecap and its usefulnesss]",
        'options': ['>', '>=', '<', '<='],
        'inputtype': 'dropdown'
        },
    {
        'id': f'maxddcap_hip_{bp.botid}',
        'prompt': 'Enter a max drawdown threshold if you want to filter out stocks do not meet that threshold over the date range selected.',
        'details':  "[Define maxdd and its usefulnesss]",
        'placeholdertext': 'Optional',
        'inputtype': 'number',
        'max': 0
        },
    {
        'id': f'maxddcap_hip_filter_{bp.botid}',
        'prompt': 'Keep stocks whose max drawdown is, over the date range selected, __ the threshold established above.',
        'details':  "[Define maxdd and its usefulnesss]",
        'options': ['>', '>=', '<', '<='],
        'inputtype': 'dropdown'
        },
    {
        'id': f'fatscorecap_life_{bp.botid}',
        'prompt': 'Enter a fatscorecap threshold if you want to filter out stocks that do not meet that threshold over their respective lifetimes.',
        'details':  "[Define fatscorecap lifetime and its usefulnesss]",
        'placeholdertext': 'Optional',
        'inputtype': 'number',
        'min': 0
        },
    {
        'id': f'fatscorecap_life_filter_{bp.botid}',
        'prompt': 'Keep stocks that, over their respective lifetimes, are __ the fatscorecap threshold established above.',
        'details':  "[Define fatscorecap life and its usefulnesss]",
        'options': ['>', '>=', '<', '<='],
        'inputtype': 'dropdown'
        },
    {
        'id': f'maxddcap_life_{bp.botid}',
        'prompt': 'Enter a max drawdown threshold if you want to filter out stocks do not meet that threshold over their respective lifetimes.',
        'details':  "[Define maxdd life and its usefulnesss]",
        'placeholdertext': 'Optional',
        'inputtype': 'number',
        'max': 0
        },
    {
        'id': f'maxddcap_life_filter_{bp.botid}',
        'prompt': 'Keep stocks whose max drawdown is, over their respective lifetimes, __ the threshold established above.',
        'details':  "[Define maxdd life and its usefulnesss]",
        'options': ['>', '>=', '<', '<='],
        'inputtype': 'dropdown'
        },
    {
        'id': f'hipgrolifefatcap_{bp.botid}',
        'prompt': 'Enter a growth rate to lifetime raw baremax fatscore ratio threshold if you want to filter out stocks that do not meet that threshold.',
        'details':  "[Define maxdd life and its usefulnesss]",
        'placeholdertext': 'Optional',
        'inputtype': 'number'
        },
    {
        'id': f'hipgrolifefatcap_filter_{bp.botid}',
        'prompt': 'Keep stocks whose growth rate to lifetime raw baremax fatscore ratio is __ the threshold established above.',
        'details':  "[Define maxdd life and its usefulnesss]",
        'options': ['>', '>=', '<', '<='],
        'inputtype': 'dropdown'
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
            'inputtype': 'button_submit'
            })
        ], id=f'input_{bp.botid}'),
    html.Div([
        dcc.Graph(id=f"graph_{bp.botid}"),
        dash_inputbuilder({
            'inputtype': 'table',
            'id': f"bptable_{bp.botid}"
            })
    ], id=f'output_{bp.botid}')
])


# BESTLETTER BOT OUTPUT PAGE
@app.callback(
    Output(f'graph_{bp.botid}', 'figure'),
    Output(f'bptable_{bp.botid}', 'data'),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    State(f'datepicker_{bp.botid}', "start_date"),
    State(f'datepicker_{bp.botid}', "end_date"),
    State(f'checklist_{bp.botid}', "value"),
    State(f'marginrate_{bp.botid}', "value"),
    State(f'fatscorecap_hip_{bp.botid}', "value"),
    State(f'fatscorecap_hip_filter_{bp.botid}', "value"),
    State(f'maxddcap_hip_{bp.botid}', "value"),
    State(f'maxddcap_hip_filter_{bp.botid}', "value"),
    State(f'fatscorecap_life_{bp.botid}', "value"),
    State(f'fatscorecap_life_filter_{bp.botid}', "value"),
    State(f'maxddcap_life_{bp.botid}', "value"),
    State(f'maxddcap_life_filter_{bp.botid}', "value"),
    State(f'hipgrolifefatcap_{bp.botid}', "value"),
    State(f'hipgrolifefatcap_filter_{bp.botid}', "value"),
    Input(f"bptable_{bp.botid}", 'sort_by'),
    Input(f"bptable_{bp.botid}", 'data'),
    Input(f"hovermode_{bp.botid}", 'value'),
    prevent_initial_call=True
    )
def calc_bestperformers(
        n_clicks,
        beg_date,
        end_date,
        checklist,
        marginrate,
        fatscorecap_hip,
        fatscorecap_hip_filter,
        maxddcap_hip,
        maxddcap_hip_filter,
        fatscorecap_life,
        fatscorecap_life_filter,
        maxddcap_life,
        maxddcap_life_filter,
        hipgrolifefatcap,
        hipgrolifefatcap_filter,
        sort_by,
        dfdata,
        hovermode
        ):
    if dfdata and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
        # convert table back to dataframe
        botdf = pd.DataFrame.from_records(dfdata)
        botdf = sort_datatable(sort_by, botdf)
    else:
        # form bot run-specific parameters ('brp').
        brp = brpb_base(bp.botid, 1) | {
            'beg_date': beg_date,
            'end_date': end_date,
            'checklist': checklist,
            'marginrate': marginrate,
            'fatscorecap_hip': fatscorecap_hip,
            'fatscorecap_hip_filter': fatscorecap_hip_filter,
            'maxddcap_hip': maxddcap_hip,
            'maxddcap_hip_filter': maxddcap_hip_filter,
            'fatscorecap_life': fatscorecap_life,
            'fatscorecap_life_filter': fatscorecap_life_filter,
            'maxddcap_life': maxddcap_life,
            'maxddcap_life_filter': maxddcap_life_filter,
            'hipgrolifefatcap': hipgrolifefatcap,
            'hipgrolifefatcap_filter': hipgrolifefatcap_filter
        }
        # create table
        botdf = bp.botfunc(brp)
        # delete temp files and folder
        if 'save' not in checklist:
            delete_folder(getbotsinglerunfolder(brp['rootdir'], brp['testregimename'], brp['todaysdate'], brp['testnumber']))
    fig = px.line(botdf, x='STOCK', y=[i for i in botdf.columns if i != 'STOCK'], markers=False)
    fig.update_layout(transition_duration=500, legend_title_text='Attribute', hovermode=hovermode, uirevision='some-constant')
    return fig, botdf.to_dict('records')
