"""
Title: Database Viewer
Date Started: Oct 17, 2022
Version: 1.00
Version Start: Oct 17, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import dcc, html
from dash.dependencies import Input, Output
from dashappobject import app
import pandas as pd
import plotly.express as px
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
from ..os_functions import get_currentscript_filename
from ..dashinputs import dash_inputbuilder
from newbacktest.module_operations import ModuleOperations
from ..html_json import jsontodash, remove_nonrenderables
from formatting import format_tabs
from newbacktest.cloudgrapher.cloudgrapher_data import CloudGrapherData
from formatting_graphs import dccgraph_config, figure_layout_mastertemplate

bp = BotParams(
    get_currentscript_filename(__file__),
    'Database Viewer',
    "Abstract Class to view databases.",
    None
)


db_directory = {
    'Ingredients': ('newbacktest.ingredients.db_ingredient', 'IngredientsDatabase'),
    'Stage Recipes': ('newbacktest.stagerecipes.db_stagerecipe', 'StageRecipeDatabase'),
    'Strategies': ('newbacktest.strategies.db_strategycookbook', 'StrategyCookBook'),
    'Stratpools': ('newbacktest.stratpools.db_stratpool', 'StratPoolDatabase'),
    'Portfolios': ('newbacktest.portfolios.db_portfolio', 'PortfolioDatabase'),
    'CloudSamples': ('newbacktest.cloudgrapher.db_cloudsample', 'CloudSampleDatabase'),
    'Winner/Loser Pools': ('newbacktest.perfmetrics.winnerloser.db_wlpool', 'WinLosePoolDatabase'),
    'Winner/Loser Profiles': ('newbacktest.perfmetrics.winnerloser.db_wlprofile', 'WinLoseProfDatabase'),
}

layout = html.Div([
    html.P([
        html.B('Select a Database:'),
        dash_inputbuilder({
            'id': f'selectdb_{bp.botid}',
            'prompt': 'Select a Database',
            'inputtype': 'dropdown',
            'options': [{'label': k, 'value': k} for k in db_directory.keys()],
            'placeholder': 'Choose an existing database',
            'value': 'Ingredients',
            'multi': False,
            'searchable': False,
            'clearable': False
            })
            ]),
    html.P([html.B('Database Name:'), html.Div(id=f'databasename_{bp.botid}')]),
    html.P([html.B('Database Info:'), html.Div(id=f'databaseinfo_{bp.botid}')]),
    html.Span(html.B('Keys:')),
    html.P(
        dash_inputbuilder({
            'id': f'level_0_choice_{bp.botid}',
            'prompt': 'Choose a key to explore:',
            'inputtype': 'dropdown',
            'placeholder': 'Choose a key to explore',
            'options': [],
            'value': "",
            'multi': False,
            'searchable': False,
            'clearable': False
            }), id=f'level_0_{bp.botid}'),
    html.P([
        html.B('Key Contents:'),
        html.Div(id=f'level_0_content_{bp.botid}'),
        ], id=f'keycontents_{bp.botid}'),
    html.P([
        html.B('Next Level Keys:'),
        dash_inputbuilder({
            'id': f'level_1_choice_{bp.botid}',
            'prompt': 'Choose a key to explore:',
            'inputtype': 'dropdown',
            'placeholder': 'Choose a key to explore',
            'options': [],
            'value': "",
            'multi': False,
            'searchable': False,
            'clearable': False
            })
        ], id=f'nextlevelkeys_{bp.botid}'),
    html.Div(
        dcc.Tabs([
            dcc.Tab(html.Div(dash_inputbuilder({
                    'inputtype': 'table',
                    'id': f"dfcontent_{bp.botid}",
                    }), className=format_tabs), label='Table Output', id=f'tabletab_{bp.botid}'),
            dcc.Tab(html.Div([
                html.Div([
                    html.Span([html.B('Line Graph Mode:')]),
                    dash_inputbuilder({
                        'id': f'calib_{bp.botid}',
                        'inputtype': 'radio',
                        'options': [
                            {'label': 'Absolute', 'value': 'absolute'},
                            {'label': 'Normalized', 'value': 'normalize'}
                        ],
                        'value': 'absolute',
                        'inline': 'inline'
                        })
                    ], id=f'modeoptions_{bp.botid}'),
                html.Span([html.B('Hover Options:')]),
                dash_inputbuilder({
                    'id': f'hovermode_{bp.botid}',
                    'prompt': 'Choose how you want to display data when you hover over the graph.',
                    'inputtype': 'radio',
                    'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
                    'value': 'x',
                    'inline': 'inline'
                    }),
                dcc.Graph(id=f'dfgraph_{bp.botid}', config=dccgraph_config)
            ], className=format_tabs), label='Table Grapher', id=f'graphertab_{bp.botid}')
        ]), id=f'tab_block_{bp.botid}')
])


# select database
@app.callback(
    Output(f'databasename_{bp.botid}', 'children'),
    Output(f'databaseinfo_{bp.botid}', 'children'),
    Output(f'level_0_choice_{bp.botid}', 'options'),
    Output(f'level_0_choice_{bp.botid}', 'value'),
    Input(f"selectdb_{bp.botid}", 'value')
    )
def gen_dbname(dbchoice):
    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if dbchoice == 'Stratpools' or dbchoice == 'Winner/Loser Pools':
        dbkeys = list(dbinstance.view_database()['data'].keys())
    else:
        dbkeys = list(dbinstance.view_database().keys())
    return dbinstance._dbname, dbinstance.__str__(), [{'label': x, 'value': x} for x in dbkeys], dbkeys[0]


@app.callback(
    Output(f"level_1_choice_{bp.botid}", 'options'),
    Output(f"level_1_choice_{bp.botid}", 'value'),
    Output(f"nextlevelkeys_{bp.botid}", 'hidden'),
    Input(f"level_0_choice_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value')
    )
def gen_keycontents(dbkey, dbchoice):

    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if dbchoice == 'Stratpools' or dbchoice == 'Winner/Loser Pools':
        dictdata = dbinstance.view_database()['data'][dbkey]
        return [{'label': x, 'value': f"{x}"} for x in dictdata.keys()], f"{list(dictdata.keys())[0]}", None
    elif dbchoice == 'Portfolios':
        return [], "", 'hidden'
    else:
        return [], "", 'hidden'


@app.callback(
    Output(f'level_0_content_{bp.botid}', 'children'),
    Output(f"keycontents_{bp.botid}", 'hidden'),
    Output(f'dfcontent_{bp.botid}', 'data'),
    Output(f"tab_block_{bp.botid}", 'hidden'),
    Input(f"level_1_choice_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value'),
    Input(f"level_0_choice_{bp.botid}", 'value'),
    Input(f"calib_{bp.botid}", "value")
    )
def gen_level1_contents(level_1_choice, dbchoice, dbkey, calibmode):
    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if level_1_choice and (dbchoice == 'Stratpools' or dbchoice == 'Winner/Loser Pools'):
        level_1_object = dbinstance.view_database()['data'][dbkey][level_1_choice]
        level_0_content = level_1_object.__dict__.copy()
        remove_nonrenderables(level_0_content, dbchoice)
        return jsontodash(level_0_content), None, level_1_object.itemdata.to_dict('records'), None
    elif dbchoice == 'Portfolios':
        df = dbinstance.view_item(dbkey)
        if calibmode == 'normalize':
            CloudGrapherData().convert_to_clouddf(df)
        return None, 'hidden', df.to_dict('records'), None
    else:
        if dbchoice == 'Strategies':
            dictdata = dbinstance.view_item(dbkey).strategy_ingredients
        else:
            dictdata = dbinstance.view_item_details(dbkey)
            remove_nonrenderables(dictdata, dbchoice)
            if dbchoice == 'Winner/Loser Profiles':
                dictdata['ingredients'] = dbinstance.view_item(dbkey).ingredientlist
        return jsontodash(dictdata), None, None, 'hidden'


# gen graph
@app.callback(
    Output(f'dfgraph_{bp.botid}', 'figure'),
    Output(f"modeoptions_{bp.botid}", 'hidden'),
    Input(f"dfcontent_{bp.botid}", 'data'),
    Input(f"hovermode_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value'),
    Input(f"calib_{bp.botid}", "value"),
    )
def gen_graph(dfsource, hovermode, dbchoice, calibmode):
    modeoptions = 'hidden'
    if dfsource:
        df = pd.DataFrame.from_records(dfsource)
        if dbchoice == 'Stratpools' or dbchoice == 'Winner/Loser Pools':
            xaxis = 'stock'
            yaxes = df.columns
            yaxislabel = 'metricvalue'
            legendtitle = None
            fig = px.bar(df, x=xaxis, y=yaxes, template=figure_layout_mastertemplate)

        elif dbchoice == 'Portfolios':
            yaxislabel = '$'
            if calibmode == 'normalize':
                yaxislabel = '% ("1" = 100%)'
            xaxis = 'date'
            yaxes = df.columns[1:]
            legendtitle = 'Tickers'
            fig = px.line(df, x=xaxis, y=yaxes, markers=False, template=figure_layout_mastertemplate)
            # fig.update_traces(connectgaps=True)
            modeoptions = None

    else:
        yaxislabel = '%'
        legendtitle = None
        fig = px.line(pd.DataFrame(data=[0]))
    fig.update_layout(yaxis_title=yaxislabel, legend_title_text=legendtitle, hovermode=hovermode)
    return fig, modeoptions
