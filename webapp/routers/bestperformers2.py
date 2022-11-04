"""
Title: Best Performers Endpoint
Date Started: Jan 30, 2022
Version: 1.00
Version Start: Jan 30, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .
fatscore_baremaxtoraw
fatscore_baremaxtobaremin
drop_mag
drop_prev
dropscore
maxdd

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
from ..common_resources import tickers, staticmindate, staticmaxdate
from ..botrun_parambuilder import brpb_base
from file_functions import delete_folder, getbotsinglerunfolder
from ..botclasses import BotParams
from Modules.bots.bestperformers.BESTPERFORMERS_BASE2 import bestperformer_cruncher
from ..os_functions import get_currentscript_filename
from ..datatables import DataTableOperations
from Modules.dates import DateOperations
from Modules.timeperiodbot import random_dates
from formatting import format_htmltable_row, format_tabs
from .bestperformers2_helper_inputs import BestPerformerInputs
from ..graphing.grapher import GraphAssets
from ..graphing.grapher_helper_functions import GrapherHelperFunctions
from ..graphing.grapher_helper_volstats import VolStatFunctions

bp = BotParams(
    get_currentscript_filename(__file__),
    'Best Performers Bot',
    "The Best Performers Bot finds stocks that meet the requirements specified for the date range specified.  The ticker symbols considered are all United States NASDAQ and NYSE common stock.",
    bestperformer_cruncher
)

tbodydata = [
    {
        'id': f'datepicker_bptable_{bp.botid}',
        'prompt': 'Specify a date range.',
        'inputtype': 'datepicker_range',
        'clearable': True,
        'min_date_allowed': staticmindate,
        'max_date_allowed': staticmaxdate
        },
    {
        'id': f'randomize_{bp.botid}',
        'prompt': 'Randomize dates instead?',
        'buttontext': 'Randomize dates',
        'inputtype': 'button_submit'
        }
]

growthrateinputs = BestPerformerInputs(bp, tickers).growthrateinputs
fatscore_baremaxtoraw_inputs = BestPerformerInputs(bp, tickers).fatscore_baremaxtoraw_inputs
fatscore_baremaxtobaremin_inputs = BestPerformerInputs(bp, tickers).fatscore_baremaxtobaremin_inputs
drop_mag_inputs = BestPerformerInputs(bp, tickers).drop_mag_inputs
drop_prev_inputs = BestPerformerInputs(bp, tickers).drop_prev_inputs
dropscore_inputs = BestPerformerInputs(bp, tickers).dropscore_inputs
maxdd_inputs = BestPerformerInputs(bp, tickers).maxdd_inputs

layout = html.Div([
    html.Div([
        html.Table(gen_tablecontents(tbodydata)),
        html.Table(gen_tablecontents(growthrateinputs), id=f'cohort_growthrate_{bp.botid}', className=format_htmltable_row),
        html.Table(gen_tablecontents(fatscore_baremaxtoraw_inputs), id=f'cohort_fatscore_baremaxtoraw_{bp.botid}', className=format_htmltable_row),
        html.Table(gen_tablecontents(fatscore_baremaxtobaremin_inputs), id=f'cohort_fatscore_baremaxtobaremin_{bp.botid}', className=format_htmltable_row),
        html.Table(gen_tablecontents(drop_mag_inputs), id=f'cohort_drop_mag_{bp.botid}', className=format_htmltable_row),
        html.Table(gen_tablecontents(drop_prev_inputs), id=f'cohort_drop_prev_{bp.botid}', className=format_htmltable_row),
        html.Table(gen_tablecontents(dropscore_inputs), id=f'cohort_dropscore_{bp.botid}', className=format_htmltable_row),
        html.Table(gen_tablecontents(maxdd_inputs), id=f'cohort_maxdd_{bp.botid}', className=format_htmltable_row),
        prompt_builder({
            'id': f'submitbutton_{bp.botid}',
            'inputtype': 'button_submit'
            })
        ], id=f'input_{bp.botid}'),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(html.Div(id=f'tab_preview_{bp.botid}', className=format_tabs), label='Input Summary'),
        dcc.Tab(html.Div([
            html.Div(id=f"testoutput_{bp.botid}"),
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"bptable_{bp.botid}"
                })], className=format_tabs), label='Full Ranking'),
        dcc.Tab(html.Div([
            dash_inputbuilder({
                'id': f'hovermode_fullranking_graph_{bp.botid}',
                'prompt': 'Choose how you want to display data when you hover over the graph.',
                'inputtype': 'radio',
                'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
                'value': 'closest',
                'inline': 'inline'
                }),
            dcc.Graph(id=f"fullranking_graph_{bp.botid}")
        ], className=format_tabs), label='Ranking Graph'),
        dcc.Tab(html.Div(GraphAssets(bp).perfgraphtab, className=format_tabs), label='Performance Graph'),
        dcc.Tab(html.Div(dash_inputbuilder({
            'inputtype': 'table',
            'id': f"sourcetable_{bp.botid}"
            }), className=format_tabs), label='Raw Data')
        ]),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"bpsourcetable_{bp.botid}"
        }), id=f"hidden_{bp.botid}", hidden='hidden'),
])


# get random dates
@app.callback(
    Output(f'datepicker_bptable_{bp.botid}', "start_date"),
    Output(f'datepicker_bptable_{bp.botid}', "end_date"),
    Input(f'randomize_{bp.botid}', "n_clicks"),
    prevent_initial_call=True
    )
def randomize_date(n_clicks):
    new_start = random_dates(staticmindate, staticmaxdate, 1)[0]
    new_end = random_dates(DateOperations().plusminusdays(new_start, 1), staticmaxdate, 1)[0]
    return new_start, new_end


# modify growth rate input fields
@app.callback(
    Output(f'inputfield_byticker_growthrate_{bp.botid}', 'hidden'),
    Output(f'prompt_byticker_growthrate_{bp.botid}', 'hidden'),
    Output(f'inputfield_bynumber_growthrate_{bp.botid}', 'hidden'),
    Output(f'prompt_bynumber_growthrate_{bp.botid}', 'hidden'),
    Output(f'inputfield_growthrate_filter_{bp.botid}', 'hidden'),
    Output(f'prompt_growthrate_filter_{bp.botid}', 'hidden'),
    Output(f'inputfield_growthrate_margin_{bp.botid}', 'hidden'),
    Output(f'prompt_growthrate_margin_{bp.botid}', 'hidden'),
    Input(f"growthrate_{bp.botid}", 'value')
    )
def update_inputs_growthrate(thresh):
    hide_inputfield_byticker = 'hidden'
    hide_prompt_byticker = 'hidden'
    hide_inputfield_bynumber = 'hidden'
    hide_prompt_bynumber = 'hidden'
    hide_inputfield_filter = 'hidden'
    hide_prompt_filter = 'hidden'
    hide_inputfield_margin = 'hidden'
    hide_prompt_margin = 'hidden'
    if thresh == 'byticker':
        hide_inputfield_byticker = None
        hide_prompt_byticker = None
    elif thresh == 'bynumber':
        hide_inputfield_bynumber = None
        hide_prompt_bynumber = None
    if thresh in ['byticker', 'bybench', 'bynumber']:
        hide_inputfield_filter = None
        hide_prompt_filter = None
        hide_inputfield_margin = None
        hide_prompt_margin = None
    return hide_inputfield_byticker, hide_prompt_byticker, hide_inputfield_bynumber, hide_prompt_bynumber, hide_inputfield_filter, hide_prompt_filter, hide_inputfield_margin, hide_prompt_margin


# modify fatscore_baremaxtoraw input fields
@app.callback(
    Output(f'inputfield_byticker_fatscore_baremaxtoraw_{bp.botid}', 'hidden'),
    Output(f'prompt_byticker_fatscore_baremaxtoraw_{bp.botid}', 'hidden'),
    Output(f'inputfield_bynumber_fatscore_baremaxtoraw_{bp.botid}', 'hidden'),
    Output(f'prompt_bynumber_fatscore_baremaxtoraw_{bp.botid}', 'hidden'),
    Output(f'inputfield_fatscore_baremaxtoraw_filter_{bp.botid}', 'hidden'),
    Output(f'prompt_fatscore_baremaxtoraw_filter_{bp.botid}', 'hidden'),
    Output(f'inputfield_fatscore_baremaxtoraw_margin_{bp.botid}', 'hidden'),
    Output(f'prompt_fatscore_baremaxtoraw_margin_{bp.botid}', 'hidden'),
    Input(f"fatscore_baremaxtoraw_{bp.botid}", 'value')
    )
def update_inputs_fatscore_baremaxtoraw(thresh):
    hide_inputfield_byticker = 'hidden'
    hide_prompt_byticker = 'hidden'
    hide_inputfield_bynumber = 'hidden'
    hide_prompt_bynumber = 'hidden'
    hide_inputfield_filter = 'hidden'
    hide_prompt_filter = 'hidden'
    hide_inputfield_margin = 'hidden'
    hide_prompt_margin = 'hidden'
    if thresh == 'byticker':
        hide_inputfield_byticker = None
        hide_prompt_byticker = None
    elif thresh == 'bynumber':
        hide_inputfield_bynumber = None
        hide_prompt_bynumber = None
    if thresh in ['byticker', 'bybench', 'bynumber']:
        hide_inputfield_filter = None
        hide_prompt_filter = None
        hide_inputfield_margin = None
        hide_prompt_margin = None
    return hide_inputfield_byticker, hide_prompt_byticker, hide_inputfield_bynumber, hide_prompt_bynumber, hide_inputfield_filter, hide_prompt_filter, hide_inputfield_margin, hide_prompt_margin


# modify fatscore_baremaxtobaremin input fields
@app.callback(
    Output(f'inputfield_byticker_fatscore_baremaxtobaremin_{bp.botid}', 'hidden'),
    Output(f'prompt_byticker_fatscore_baremaxtobaremin_{bp.botid}', 'hidden'),
    Output(f'inputfield_bynumber_fatscore_baremaxtobaremin_{bp.botid}', 'hidden'),
    Output(f'prompt_bynumber_fatscore_baremaxtobaremin_{bp.botid}', 'hidden'),
    Output(f'inputfield_fatscore_baremaxtobaremin_filter_{bp.botid}', 'hidden'),
    Output(f'prompt_fatscore_baremaxtobaremin_filter_{bp.botid}', 'hidden'),
    Output(f'inputfield_fatscore_baremaxtobaremin_margin_{bp.botid}', 'hidden'),
    Output(f'prompt_fatscore_baremaxtobaremin_margin_{bp.botid}', 'hidden'),
    Input(f"fatscore_baremaxtobaremin_{bp.botid}", 'value')
    )
def update_inputs_fatscore_baremaxtobaremin(thresh):
    hide_inputfield_byticker = 'hidden'
    hide_prompt_byticker = 'hidden'
    hide_inputfield_bynumber = 'hidden'
    hide_prompt_bynumber = 'hidden'
    hide_inputfield_filter = 'hidden'
    hide_prompt_filter = 'hidden'
    hide_inputfield_margin = 'hidden'
    hide_prompt_margin = 'hidden'
    if thresh == 'byticker':
        hide_inputfield_byticker = None
        hide_prompt_byticker = None
    elif thresh == 'bynumber':
        hide_inputfield_bynumber = None
        hide_prompt_bynumber = None
    if thresh in ['byticker', 'bybench', 'bynumber']:
        hide_inputfield_filter = None
        hide_prompt_filter = None
        hide_inputfield_margin = None
        hide_prompt_margin = None
    return hide_inputfield_byticker, hide_prompt_byticker, hide_inputfield_bynumber, hide_prompt_bynumber, hide_inputfield_filter, hide_prompt_filter, hide_inputfield_margin, hide_prompt_margin


# modify drop_mag input fields
@app.callback(
    Output(f'inputfield_byticker_drop_mag_{bp.botid}', 'hidden'),
    Output(f'prompt_byticker_drop_mag_{bp.botid}', 'hidden'),
    Output(f'inputfield_bynumber_drop_mag_{bp.botid}', 'hidden'),
    Output(f'prompt_bynumber_drop_mag_{bp.botid}', 'hidden'),
    Output(f'inputfield_drop_mag_filter_{bp.botid}', 'hidden'),
    Output(f'prompt_drop_mag_filter_{bp.botid}', 'hidden'),
    Output(f'inputfield_drop_mag_margin_{bp.botid}', 'hidden'),
    Output(f'prompt_drop_mag_margin_{bp.botid}', 'hidden'),
    Input(f"drop_mag_{bp.botid}", 'value')
    )
def update_inputs_drop_mag(thresh):
    hide_inputfield_byticker = 'hidden'
    hide_prompt_byticker = 'hidden'
    hide_inputfield_bynumber = 'hidden'
    hide_prompt_bynumber = 'hidden'
    hide_inputfield_filter = 'hidden'
    hide_prompt_filter = 'hidden'
    hide_inputfield_margin = 'hidden'
    hide_prompt_margin = 'hidden'
    if thresh == 'byticker':
        hide_inputfield_byticker = None
        hide_prompt_byticker = None
    elif thresh == 'bynumber':
        hide_inputfield_bynumber = None
        hide_prompt_bynumber = None
    if thresh in ['byticker', 'bybench', 'bynumber']:
        hide_inputfield_filter = None
        hide_prompt_filter = None
        hide_inputfield_margin = None
        hide_prompt_margin = None
    return hide_inputfield_byticker, hide_prompt_byticker, hide_inputfield_bynumber, hide_prompt_bynumber, hide_inputfield_filter, hide_prompt_filter, hide_inputfield_margin, hide_prompt_margin


# modify drop_prev input fields
@app.callback(
    Output(f'inputfield_byticker_drop_prev_{bp.botid}', 'hidden'),
    Output(f'prompt_byticker_drop_prev_{bp.botid}', 'hidden'),
    Output(f'inputfield_bynumber_drop_prev_{bp.botid}', 'hidden'),
    Output(f'prompt_bynumber_drop_prev_{bp.botid}', 'hidden'),
    Output(f'inputfield_drop_prev_filter_{bp.botid}', 'hidden'),
    Output(f'prompt_drop_prev_filter_{bp.botid}', 'hidden'),
    Output(f'inputfield_drop_prev_margin_{bp.botid}', 'hidden'),
    Output(f'prompt_drop_prev_margin_{bp.botid}', 'hidden'),
    Input(f"drop_prev_{bp.botid}", 'value')
    )
def update_inputs_drop_prev(thresh):
    hide_inputfield_byticker = 'hidden'
    hide_prompt_byticker = 'hidden'
    hide_inputfield_bynumber = 'hidden'
    hide_prompt_bynumber = 'hidden'
    hide_inputfield_filter = 'hidden'
    hide_prompt_filter = 'hidden'
    hide_inputfield_margin = 'hidden'
    hide_prompt_margin = 'hidden'
    if thresh == 'byticker':
        hide_inputfield_byticker = None
        hide_prompt_byticker = None
    elif thresh == 'bynumber':
        hide_inputfield_bynumber = None
        hide_prompt_bynumber = None
    if thresh in ['byticker', 'bybench', 'bynumber']:
        hide_inputfield_filter = None
        hide_prompt_filter = None
        hide_inputfield_margin = None
        hide_prompt_margin = None
    return hide_inputfield_byticker, hide_prompt_byticker, hide_inputfield_bynumber, hide_prompt_bynumber, hide_inputfield_filter, hide_prompt_filter, hide_inputfield_margin, hide_prompt_margin


# modify dropscore input fields
@app.callback(
    Output(f'inputfield_byticker_dropscore_{bp.botid}', 'hidden'),
    Output(f'prompt_byticker_dropscore_{bp.botid}', 'hidden'),
    Output(f'inputfield_bynumber_dropscore_{bp.botid}', 'hidden'),
    Output(f'prompt_bynumber_dropscore_{bp.botid}', 'hidden'),
    Output(f'inputfield_dropscore_filter_{bp.botid}', 'hidden'),
    Output(f'prompt_dropscore_filter_{bp.botid}', 'hidden'),
    Output(f'inputfield_dropscore_margin_{bp.botid}', 'hidden'),
    Output(f'prompt_dropscore_margin_{bp.botid}', 'hidden'),
    Input(f"dropscore_{bp.botid}", 'value')
    )
def update_inputs_dropscore(thresh):
    hide_inputfield_byticker = 'hidden'
    hide_prompt_byticker = 'hidden'
    hide_inputfield_bynumber = 'hidden'
    hide_prompt_bynumber = 'hidden'
    hide_inputfield_filter = 'hidden'
    hide_prompt_filter = 'hidden'
    hide_inputfield_margin = 'hidden'
    hide_prompt_margin = 'hidden'
    if thresh == 'byticker':
        hide_inputfield_byticker = None
        hide_prompt_byticker = None
    elif thresh == 'bynumber':
        hide_inputfield_bynumber = None
        hide_prompt_bynumber = None
    if thresh in ['byticker', 'bybench', 'bynumber']:
        hide_inputfield_filter = None
        hide_prompt_filter = None
        hide_inputfield_margin = None
        hide_prompt_margin = None
    return hide_inputfield_byticker, hide_prompt_byticker, hide_inputfield_bynumber, hide_prompt_bynumber, hide_inputfield_filter, hide_prompt_filter, hide_inputfield_margin, hide_prompt_margin


# modify maxdd input fields
@app.callback(
    Output(f'inputfield_byticker_maxdd_{bp.botid}', 'hidden'),
    Output(f'prompt_byticker_maxdd_{bp.botid}', 'hidden'),
    Output(f'inputfield_bynumber_maxdd_{bp.botid}', 'hidden'),
    Output(f'prompt_bynumber_maxdd_{bp.botid}', 'hidden'),
    Output(f'inputfield_maxdd_filter_{bp.botid}', 'hidden'),
    Output(f'prompt_maxdd_filter_{bp.botid}', 'hidden'),
    Output(f'inputfield_maxdd_margin_{bp.botid}', 'hidden'),
    Output(f'prompt_maxdd_margin_{bp.botid}', 'hidden'),
    Input(f"maxdd_{bp.botid}", 'value')
    )
def update_inputs_maxdd(thresh):
    hide_inputfield_byticker = 'hidden'
    hide_prompt_byticker = 'hidden'
    hide_inputfield_bynumber = 'hidden'
    hide_prompt_bynumber = 'hidden'
    hide_inputfield_filter = 'hidden'
    hide_prompt_filter = 'hidden'
    hide_inputfield_margin = 'hidden'
    hide_prompt_margin = 'hidden'
    if thresh == 'byticker':
        hide_inputfield_byticker = None
        hide_prompt_byticker = None
    elif thresh == 'bynumber':
        hide_inputfield_bynumber = None
        hide_prompt_bynumber = None
    if thresh in ['byticker', 'bybench', 'bynumber']:
        hide_inputfield_filter = None
        hide_prompt_filter = None
        hide_inputfield_margin = None
        hide_prompt_margin = None
    return hide_inputfield_byticker, hide_prompt_byticker, hide_inputfield_bynumber, hide_prompt_bynumber, hide_inputfield_filter, hide_prompt_filter, hide_inputfield_margin, hide_prompt_margin


# VALIDATE INPUTS
@app.callback(
    Output(f'tab_preview_{bp.botid}', "children"),
    Input(f"datepicker_bptable_{bp.botid}", 'start_date'),
    Input(f"datepicker_bptable_{bp.botid}", 'end_date'),
    Input(f"growthrate_{bp.botid}", 'value'),
    Input(f"byticker_growthrate_{bp.botid}", 'value'),
    Input(f"bynumber_growthrate_{bp.botid}", 'value'),
    Input(f"growthrate_filter_{bp.botid}", 'value'),
    Input(f"growthrate_margin_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtoraw_{bp.botid}", 'value'),
    Input(f"byticker_fatscore_baremaxtoraw_{bp.botid}", 'value'),
    Input(f"bynumber_fatscore_baremaxtoraw_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtoraw_filter_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtoraw_margin_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtobaremin_{bp.botid}", 'value'),
    Input(f"byticker_fatscore_baremaxtobaremin_{bp.botid}", 'value'),
    Input(f"bynumber_fatscore_baremaxtobaremin_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtobaremin_filter_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtobaremin_margin_{bp.botid}", 'value'),
    Input(f"drop_mag_{bp.botid}", 'value'),
    Input(f"byticker_drop_mag_{bp.botid}", 'value'),
    Input(f"bynumber_drop_mag_{bp.botid}", 'value'),
    Input(f"drop_mag_filter_{bp.botid}", 'value'),
    Input(f"drop_mag_margin_{bp.botid}", 'value'),
    Input(f"drop_prev_{bp.botid}", 'value'),
    Input(f"byticker_drop_prev_{bp.botid}", 'value'),
    Input(f"bynumber_drop_prev_{bp.botid}", 'value'),
    Input(f"drop_prev_filter_{bp.botid}", 'value'),
    Input(f"drop_prev_margin_{bp.botid}", 'value'),
    Input(f"dropscore_{bp.botid}", 'value'),
    Input(f"byticker_dropscore_{bp.botid}", 'value'),
    Input(f"bynumber_dropscore_{bp.botid}", 'value'),
    Input(f"dropscore_filter_{bp.botid}", 'value'),
    Input(f"dropscore_margin_{bp.botid}", 'value'),
    Input(f"maxdd_{bp.botid}", 'value'),
    Input(f"byticker_maxdd_{bp.botid}", 'value'),
    Input(f"bynumber_maxdd_{bp.botid}", 'value'),
    Input(f"maxdd_filter_{bp.botid}", 'value'),
    Input(f"maxdd_margin_{bp.botid}", 'value'),
    )
def validate_inputs(
    start_date,
    end_date,
    growthrate,
    byticker_growthrate,
    bynumber_growthrate,
    growthrate_filter,
    growthrate_margin,
    fatscore_baremaxtoraw,
    byticker_fatscore_baremaxtoraw,
    bynumber_fatscore_baremaxtoraw,
    fatscore_baremaxtoraw_filter,
    fatscore_baremaxtoraw_margin,
    fatscore_baremaxtobaremin,
    byticker_fatscore_baremaxtobaremin,
    bynumber_fatscore_baremaxtobaremin,
    fatscore_baremaxtobaremin_filter,
    fatscore_baremaxtobaremin_margin,
    drop_mag,
    byticker_drop_mag,
    bynumber_drop_mag,
    drop_mag_filter,
    drop_mag_margin,
    drop_prev,
    byticker_drop_prev,
    bynumber_drop_prev,
    drop_prev_filter,
    drop_prev_margin,
    dropscore,
    byticker_dropscore,
    bynumber_dropscore,
    dropscore_filter,
    dropscore_margin,
    maxdd,
    byticker_maxdd,
    bynumber_maxdd,
    maxdd_filter,
    maxdd_margin
):
    setting_summary = [
        f'start_date: {start_date}',
        f'end_date: {end_date}',
        f'growthrate: {growthrate}',
        f'byticker_growthrate: {byticker_growthrate}',
        f'bynumber_growthrate: {bynumber_growthrate}',
        f'growthrate_filter: {growthrate_filter}',
        f'growthrate_margin: {growthrate_margin}',
        f'fatscore_baremaxtoraw: {fatscore_baremaxtoraw}',
        f'byticker_fatscore_baremaxtoraw: {byticker_fatscore_baremaxtoraw}',
        f'bynumber_fatscore_baremaxtoraw: {bynumber_fatscore_baremaxtoraw}',
        f'fatscore_baremaxtoraw_filter: {fatscore_baremaxtoraw_filter}',
        f'fatscore_baremaxtoraw_margin: {fatscore_baremaxtoraw_margin}',
        f'fatscore_baremaxtobaremin: {fatscore_baremaxtobaremin}',
        f'byticker_fatscore_baremaxtobaremin: {byticker_fatscore_baremaxtobaremin}',
        f'bynumber_fatscore_baremaxtobaremin: {bynumber_fatscore_baremaxtobaremin}',
        f'fatscore_baremaxtobaremin_filter: {fatscore_baremaxtobaremin_filter}',
        f'fatscore_baremaxtobaremin_margin: {fatscore_baremaxtobaremin_margin}',
        f'drop_mag: {drop_mag}',
        f'byticker_drop_mag: {byticker_drop_mag}',
        f'bynumber_drop_mag: {bynumber_drop_mag}',
        f'drop_mag_filter: {drop_mag_filter}',
        f'drop_mag_margin: {drop_mag_margin}',
        f'drop_prev: {drop_prev}',
        f'byticker_drop_prev: {byticker_drop_prev}',
        f'bynumber_drop_prev: {bynumber_drop_prev}',
        f'drop_prev_filter: {drop_prev_filter}',
        f'drop_prev_margin: {drop_prev_margin}',
        f'dropscore: {dropscore}',
        f'byticker_dropscore: {byticker_dropscore}',
        f'bynumber_dropscore: {bynumber_dropscore}',
        f'dropscore_filter: {dropscore_filter}',
        f'dropscore_margin: {dropscore_margin}',
        f'maxdd: {maxdd}',
        f'byticker_maxdd: {byticker_maxdd}',
        f'bynumber_maxdd: {bynumber_maxdd}',
        f'maxdd_filter: {maxdd_filter}',
        f'maxdd_margin: {maxdd_margin}'
        ]
    setting_summary = [html.P([html.Div([html.Span(i), html.Br()]) for i in setting_summary])]
    return setting_summary


# CALC BEST PERFORMERS
@app.callback(
    Output(f'bpsourcetable_{bp.botid}', 'data'),
    Input(f'submitbutton_{bp.botid}', 'n_clicks'),
    Input(f"datepicker_bptable_{bp.botid}", 'start_date'),
    Input(f"datepicker_bptable_{bp.botid}", 'end_date'),
    Input(f"growthrate_{bp.botid}", 'value'),
    Input(f"byticker_growthrate_{bp.botid}", 'value'),
    Input(f"bynumber_growthrate_{bp.botid}", 'value'),
    Input(f"growthrate_filter_{bp.botid}", 'value'),
    Input(f"growthrate_margin_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtoraw_{bp.botid}", 'value'),
    Input(f"byticker_fatscore_baremaxtoraw_{bp.botid}", 'value'),
    Input(f"bynumber_fatscore_baremaxtoraw_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtoraw_filter_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtoraw_margin_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtobaremin_{bp.botid}", 'value'),
    Input(f"byticker_fatscore_baremaxtobaremin_{bp.botid}", 'value'),
    Input(f"bynumber_fatscore_baremaxtobaremin_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtobaremin_filter_{bp.botid}", 'value'),
    Input(f"fatscore_baremaxtobaremin_margin_{bp.botid}", 'value'),
    Input(f"drop_mag_{bp.botid}", 'value'),
    Input(f"byticker_drop_mag_{bp.botid}", 'value'),
    Input(f"bynumber_drop_mag_{bp.botid}", 'value'),
    Input(f"drop_mag_filter_{bp.botid}", 'value'),
    Input(f"drop_mag_margin_{bp.botid}", 'value'),
    Input(f"drop_prev_{bp.botid}", 'value'),
    Input(f"byticker_drop_prev_{bp.botid}", 'value'),
    Input(f"bynumber_drop_prev_{bp.botid}", 'value'),
    Input(f"drop_prev_filter_{bp.botid}", 'value'),
    Input(f"drop_prev_margin_{bp.botid}", 'value'),
    Input(f"dropscore_{bp.botid}", 'value'),
    Input(f"byticker_dropscore_{bp.botid}", 'value'),
    Input(f"bynumber_dropscore_{bp.botid}", 'value'),
    Input(f"dropscore_filter_{bp.botid}", 'value'),
    Input(f"dropscore_margin_{bp.botid}", 'value'),
    Input(f"maxdd_{bp.botid}", 'value'),
    Input(f"byticker_maxdd_{bp.botid}", 'value'),
    Input(f"bynumber_maxdd_{bp.botid}", 'value'),
    Input(f"maxdd_filter_{bp.botid}", 'value'),
    Input(f"maxdd_margin_{bp.botid}", 'value'),
    prevent_initial_call=True
    )
def calc_bestperformers(
        n_clicks,
        start_date,
        end_date,
        growthrate,
        byticker_growthrate,
        bynumber_growthrate,
        growthrate_filter,
        growthrate_margin,
        fatscore_baremaxtoraw,
        byticker_fatscore_baremaxtoraw,
        bynumber_fatscore_baremaxtoraw,
        fatscore_baremaxtoraw_filter,
        fatscore_baremaxtoraw_margin,
        fatscore_baremaxtobaremin,
        byticker_fatscore_baremaxtobaremin,
        bynumber_fatscore_baremaxtobaremin,
        fatscore_baremaxtobaremin_filter,
        fatscore_baremaxtobaremin_margin,
        drop_mag,
        byticker_drop_mag,
        bynumber_drop_mag,
        drop_mag_filter,
        drop_mag_margin,
        drop_prev,
        byticker_drop_prev,
        bynumber_drop_prev,
        drop_prev_filter,
        drop_prev_margin,
        dropscore,
        byticker_dropscore,
        bynumber_dropscore,
        dropscore_filter,
        dropscore_margin,
        maxdd,
        byticker_maxdd,
        bynumber_maxdd,
        maxdd_filter,
        maxdd_margin,
        ):
    if callback_context.triggered[0]['prop_id'].startswith('submitbutton_'):
        brp = {**brpb_base(bp.botid, 1), **{
            'start_date': start_date,
            'end_date': end_date,
            'growthrate': growthrate,
            'byticker_growthrate': byticker_growthrate,
            'bynumber_growthrate': bynumber_growthrate,
            'growthrate_filter': growthrate_filter,
            'growthrate_margin': growthrate_margin,
            'fatscore_baremaxtoraw': fatscore_baremaxtoraw,
            'byticker_fatscore_baremaxtoraw': byticker_fatscore_baremaxtoraw,
            'bynumber_fatscore_baremaxtoraw': bynumber_fatscore_baremaxtoraw,
            'fatscore_baremaxtoraw_filter': fatscore_baremaxtoraw_filter,
            'fatscore_baremaxtoraw_margin': fatscore_baremaxtoraw_margin,
            'fatscore_baremaxtobaremin': fatscore_baremaxtobaremin,
            'byticker_fatscore_baremaxtobaremin': byticker_fatscore_baremaxtobaremin,
            'bynumber_fatscore_baremaxtobaremin': bynumber_fatscore_baremaxtobaremin,
            'fatscore_baremaxtobaremin_filter': fatscore_baremaxtobaremin_filter,
            'fatscore_baremaxtobaremin_margin': fatscore_baremaxtobaremin_margin,
            'drop_mag': drop_mag,
            'byticker_drop_mag': byticker_drop_mag,
            'bynumber_drop_mag': bynumber_drop_mag,
            'drop_mag_filter': drop_mag_filter,
            'drop_mag_margin': drop_mag_margin,
            'drop_prev': drop_prev,
            'byticker_drop_prev': byticker_drop_prev,
            'bynumber_drop_prev': bynumber_drop_prev,
            'drop_prev_filter': drop_prev_filter,
            'drop_prev_margin': drop_prev_margin,
            'dropscore': dropscore,
            'byticker_dropscore': byticker_dropscore,
            'bynumber_dropscore': bynumber_dropscore,
            'dropscore_filter': dropscore_filter,
            'dropscore_margin': dropscore_margin,
            'maxdd': maxdd,
            'byticker_maxdd': byticker_maxdd,
            'bynumber_maxdd': bynumber_maxdd,
            'maxdd_filter': maxdd_filter,
            'maxdd_margin': maxdd_margin
        }}
        # create table
        botdf = bp.botfunc(brp)
        # delete temp files and folder
        delete_folder(getbotsinglerunfolder(brp['rootdir'], brp['testregimename'], brp['todaysdate'], brp['testnumber']))
        return botdf.to_dict('records')
    else:
        return None


# gen and sort fullranking
@app.callback(
    Output(f'bptable_{bp.botid}', 'data'),
    Input(f"bptable_{bp.botid}", 'data'),
    Input(f"bptable_{bp.botid}", 'sort_by'),
    Input(f"bpsourcetable_{bp.botid}", "data"),
    )
def gen_sort_fullranking(displaytable, sort_by, sourcetable):
    if sourcetable:
        return DataTableOperations().return_sortedtable(sort_by, callback_context, displaytable, sourcetable).to_dict('records')
    else:
        return None


# FULL RANK GRAPH
@app.callback(
    Output(f'fullranking_graph_{bp.botid}', 'figure'),
    Input(f"bptable_{bp.botid}", 'data'),
    Input(f"hovermode_fullranking_graph_{bp.botid}", 'value')
    )
def gen_fullrankgraph(dfdata, hovermode):
    if dfdata and len(pd.DataFrame.from_records(dfdata).columns) > 1:
        botdf = pd.DataFrame.from_records(dfdata)
        xaxis = 'stock'
        yaxes = [i for i in botdf.columns if i != 'STOCK']
        yaxislabel = 'metricvalue'
        fig = px.bar(botdf, x=xaxis, y=yaxes)
        fig.update_layout(transition_duration=500, legend_title_text='Attribute', hovermode=hovermode, uirevision='some-constant', yaxis_title=yaxislabel)
    else:
        fig = px.line([0])
    return fig


# generate tickerlist for performance graph
@app.callback(
    Output(f'perf_graph_ticker_{bp.botid}', 'options'),
    Input(f"bpsourcetable_{bp.botid}", 'data')
    )
def gen_perf_graph_tickerlist(dfdata):
    return pd.DataFrame.from_records(dfdata)['stock'].tolist() if dfdata else []


@app.callback(
    Output(f"portcurve_{bp.botid}", "options"),
    Output(f"portcurve_{bp.botid}", "value"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value")
    )
def show_portcurve_option(ticker, calib, portcurvevalue):
    return GrapherHelperFunctions().show_portcurve_option(ticker, calib, portcurvevalue)


# create options for diffgraph and comp graph
@app.callback(
    Output(f"graphcompoptions_{bp.botid}", "options"),
    Output(f"graphcompoptions_{bp.botid}", "value"),
    Output(f"graphdiff_changecol_{bp.botid}", "options"),
    Output(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"contour_{bp.botid}", "value")
    )
def show_diffcomp_options(contour):
    return GrapherHelperFunctions().show_diffcomp_options(contour)


# gen performance graphs
@app.callback(
    Output(f"perf_graph_{bp.botid}", "figure"),
    Output(f"graphdiff_{bp.botid}", "figure"),
    Output(f"graphcomp_{bp.botid}", "figure"),
    Output(f"graphdf_{bp.botid}", "data"),
    Output(f"sd_bydd_{bp.botid}", "options"),
    Output(f'datepicker_{bp.botid}', "min_date_allowed"),
    Output(f'datepicker_{bp.botid}', "max_date_allowed"),
    Output(f'datepicker_{bp.botid}', "start_date"),
    Output(f'datepicker_{bp.botid}', "end_date"),
    Output(f'minmaxinfo_datepicker_{bp.botid}', "children"),
    Output(f"sd_bydd_{bp.botid}", "value"),
    Output(f'bench_{bp.botid}', "options"),
    Output(f"dfcol_{bp.botid}", "children"),
    Input(f"perf_graph_ticker_{bp.botid}", "value"),
    Input(f"datepicker_bptable_{bp.botid}", 'start_date'),
    Input(f"datepicker_bptable_{bp.botid}", 'end_date'),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"sd_bydd_{bp.botid}", "value"),
    Input(f'datepicker_{bp.botid}', "start_date"),
    Input(f'datepicker_{bp.botid}', "end_date"),
    Input(f"contour_{bp.botid}", "value"),
    Input(f"graphcompoptions_{bp.botid}", "value"),
    Input(f"graphdiff_mode_{bp.botid}", "value"),
    Input(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"graphdiff_period_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value"),
    Input(f"bench_{bp.botid}", 'value'),
    Input(f"hovermode_{bp.botid}", 'value'),
    Input(f"dfcol_{bp.botid}", "children")
    )
def gen_graph(tickers, bp_startdate, bp_enddate, calib, sd_bydd, pick_start, pick_end, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode, dfcol):
    if tickers:
        min_date_allowed = bp_startdate
        max_date_allowed = bp_enddate
    else:
        min_date_allowed = staticmindate
        max_date_allowed = staticmaxdate
    return GrapherHelperFunctions().gen_graph_output(callback_context, tickers, min_date_allowed, max_date_allowed, sd_bydd, pick_start, pick_end, calib, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode, dfcol)


# sort raw data table
@app.callback(
    Output(f"rawdata_{bp.botid}", "data"),
    Input(f"rawdata_{bp.botid}", 'sort_by'),
    Input(f"rawdata_{bp.botid}", "data"),
    Input(f"graphdf_{bp.botid}", "data")
    )
def sort_rawdatatable(sort_by, rawdatatable, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, rawdatatable, sourcetable).to_dict('records')


# get volstats
@app.callback(
    Output(f"voltablesource_{bp.botid}", "data"),
    Output(f"voltable_{bp.botid}", "tooltip_header"),
    Input(f'voltbutton_{bp.botid}', "n_clicks"),
    State(f"perf_graph_ticker_{bp.botid}", "value"),
    State(f"portcurve_{bp.botid}", "value"),
    State(f"bench_{bp.botid}", 'value'),
    State(f"voltable_{bp.botid}", 'sort_by'),
    State(f"voltable_{bp.botid}", "data"),
    State(f"graphdf_{bp.botid}", "data"),
    prevent_initial_call=True,
    )
def gen_volstats(n_clicks, ticker, portcurve, bench, sort_by, voldata, graphdfdata):
    if ticker:
        return VolStatFunctions().gen_volstats(ticker, portcurve, bench, sort_by, voldata, graphdfdata)
    else:
        return pd.DataFrame(data=['No data.']).to_dict('records'), None


# sort volatility table
@app.callback(
    Output(f"voltable_{bp.botid}", "data"),
    Input(f"voltable_{bp.botid}", 'sort_by'),
    Input(f"voltable_{bp.botid}", "data"),
    Input(f"voltablesource_{bp.botid}", "data")
    )
def sort_volatilitytable(sort_by, finaltable, sourcetable):
    return DataTableOperations().return_sortedtable(sort_by, callback_context, finaltable, sourcetable).to_dict('records')
