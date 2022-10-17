"""
Title: Strat Ranker
Date Started: Mar 13, 2022
Version: 1.00
Version Start: Mar 13, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Rank metricvalue ranges of each strat test run.

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import dcc, html
from dash.dependencies import Input, Output
from dashappobject import app
import plotly.express as px
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from ..os_functions import get_currentscript_filename
from ..dashinputs import dash_inputbuilder
from .strattester_helper_leaderboard import gen_leaderboard
from ..datatables import DataTableOperations
from Modules.ranking_functions import gen_ranking
from webapp.routers.strattester_helper_leaderboard_colconfig import quality_cols
from formatting import format_tabs
from Modules.dataframe_functions import join_matrices
from Modules.numbers import twodecp
from Modules.numbers_formulas import func_ending_principal

bp = BotParams(
    get_currentscript_filename(__file__),
    'Strategy Ranker',
    "Get metricvalue range of each quality metric then rank them across all strat test runs.",
    None
)


def filteredstratleaderboard():
    df = gen_leaderboard(['strat_name', 'num_periods']+quality_cols)
    df = df[df['num_periods'] >= 20]
    df = df[['strat_name']+quality_cols]
    return df


def gen_ranksourcetable(df):
    quality_rank_tuples = [
        ['effective_daily_growthrate', 1/11, 0],
        ['effective_daily_growthrate_margin', 2/11, 0],
        ['margin_daily_growthrate_min', 2/11, 0],
        ['abovezerotally_pct', 1/11, 0],
        ['abovezerotally_margin_pct', 2/11, 0],
        ['abovebench_tally_pct', 2/11, 0],
        ['abovebench_pos_tally_pct', 1/11, 0]
        ]
    lofdf = []
    for m in ['MEDIAN', 'MIN', 'MAX']:
        mdf = df.groupby('strat_name', as_index=False).median() if m == 'MEDIAN' else df.groupby('strat_name', as_index=False).min() if m == 'MIN' else df.groupby('strat_name', as_index=False).max()
        mdf.rename(columns={k: f'{k}_{m}' for k in quality_cols}, inplace=True)
        lofdf.append(mdf)
    finaldf = join_matrices('strat_name', lofdf, 1)
    grinputs = [[f'{c[0]}_{m}', (1/3)*c[1], c[2]] for c in quality_rank_tuples for m in ['MEDIAN', 'MIN', 'MAX']]
    finaldf = gen_ranking(grinputs, finaldf)
    return finaldf


basedf = filteredstratleaderboard()

layout = html.Div([
    dash_inputbuilder({
        'id': f'rankbutton_{bp.botid}',
        'buttontext': 'Rank',
        'inputtype': 'button_submit'
        }),
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
                    'inputtype': 'checklist',
                    'options': [{'label': x, 'value': x} for x in set(basedf['strat_name'])],
                    'value': list(set(basedf['strat_name'])),
                    'className': 'longchecklist',
                    'inline': 'block'
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
                dcc.Graph(id=f"overallstats_{bp.botid}"),
                html.B('Choose how you want to display labels when you hover over the graph.'),
                dash_inputbuilder({
                    'id': f'hovermode_{bp.botid}',
                    'inputtype': 'radio',
                    'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
                    'value': 'closest',
                    'inline': 'inline'
                    })
            ], id=f'displayresult_{bp.botid}')], className=format_tabs),
        dcc.Tab(label='Ranker', id=f'leadertab_{bp.botid}', children=[
            dash_inputbuilder({
                'inputtype': 'table',
                'id': f"leaderboardtable_{bp.botid}",
                'filtering': 'native'
                })
            ], className=format_tabs)
            ]),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"sourcetable_{bp.botid}"
        }), hidden='hidden')
], className='w-auto')


# gen graph
@app.callback(
    Output(f"sourcetable_{bp.botid}", "data"),
    Input(f"rankbutton_{bp.botid}", 'n_clicks')
    )
def gen_ranktable(n_clicks):
    sourcetabledata = gen_ranksourcetable(basedf)
    return sourcetabledata.to_dict('records')


# gen optional stake investment period input
@app.callback(
    Output(f'stakeperiod_div_{bp.botid}', 'hidden'),
    Input(f"startcapital_{bp.botid}", 'value')
    )
def update_inputs_growthrate(stake):
    hide_inputfield_stakeperiod_div = 'hidden'
    if stake:
        hide_inputfield_stakeperiod_div = None
    return hide_inputfield_stakeperiod_div


# gen graph
@app.callback(
    Output(f'overallstats_{bp.botid}', "figure"),
    Input(f"startcapital_{bp.botid}", 'value'),
    Input(f"stakeperiod_{bp.botid}", 'value'),
    Input(f"hidestrat_{bp.botid}", 'value'),
    Input(f"chart_type_{bp.botid}", "value"),
    Input(f"hovermode_{bp.botid}", 'value')
    )
def gen_graph(stake, stakeperiod, hidestrat, chart_type, hovermode):
    bdf = basedf[basedf['strat_name'].isin(hidestrat)]
    if len(bdf) == 0:
        fig = px.line(x=None, y=None)
        return fig
    else:
        if stake and stakeperiod:
            bdf[
                'Ending Cash ($)'
                ] = bdf[
                    'effective_daily_growthrate'
                    ].apply(lambda x: twodecp(func_ending_principal(stake, x, stakeperiod)))
            bdf[
                'Ending Cash (Benchmark) ($)'
                ] = bdf[
                    'effective_daily_growthrate_bench'
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
        bdf['sample size'] = bdf['strat_name'].apply(lambda x: bdf[bdf['strat_name'] == x]['strat_name'].count())
        df = pd.melt(bdf, id_vars="strat_name", value_vars=bdf.columns[1:], var_name='metric', value_name='value')
        df['section'] = df['metric'].apply(lambda x: 'rank metrics' if x != 'sample size' else 'sample size')
        if chart_type == 'Scatter':
            fig = px.scatter(df, x="strat_name", y="value", color="metric", facet_row="section")
            fig.update_traces(marker=dict(size=12, opacity=0.5))
        elif chart_type == 'Box':
            fig = px.box(df, x="strat_name", y="value", color="metric", facet_row="section", boxmode="overlay")
        elif chart_type == 'Violin':
            fig = px.violin(df, x="strat_name", y="value", color="metric", facet_row="section", violinmode="overlay")
        fig.update_yaxes(matches=None)
        #bdf = bdf.drop_duplicates(subset=['strat_name'])
        #fig.add_bar(x=bdf["strat_name"], y=bdf['sample size'], name="Sample Size", row=1, col=1)
        fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="grey",
            line_width=2.5)
        fig.update_layout(height=1000, transition_duration=500, legend_title_text='Legend', hovermode=hovermode, uirevision='some-constant')
        return fig


# filter, sort ranking
@app.callback(
    Output(f'leaderboardtable_{bp.botid}', 'data'),
    Output(f'leaderboardtable_{bp.botid}', 'columns'),
    Input(f'sourcetable_{bp.botid}', 'data'),
    Input(f'leaderboardtable_{bp.botid}', 'sort_by')
    )
def gen_rank_table(hiddenltable, sort_by):
    return DataTableOperations().sort_and_makecolhideable(sort_by, hiddenltable)
