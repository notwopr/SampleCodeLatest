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
# from Modules.referencetools.dipdatevisualizer.DIPDATEVISUALIZER import dipdatevisualizer_dash
# from Modules.price_history import grabsinglehistory
from ..os_functions import get_currentscript_filename
# from ..common_resources import tickers
from ..dashinputs import dash_inputbuilder
from newbacktest.module_operations import ModuleOperations
from ..html_json import jsontodash, remove_nonrenderables
from formatting import format_tabs
from newbacktest.cloudgrapher.cloudgrapher_data import CloudGrapherData

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
    'CloudSamples': ('newbacktest.cloudgrapher.db_cloudsample', 'CloudSampleDatabase')
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
        html.Div(id=f'level_0_content_{bp.botid}')
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
            dcc.Tab(label='Table Output', children=[
                dash_inputbuilder({
                    'inputtype': 'table',
                    'id': f"dfcontent_{bp.botid}",
                    })
            ], id=f'tabletab_{bp.botid}', className=format_tabs),
            dcc.Tab(label='Table Grapher', children=[
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
                dcc.Graph(id=f'dfgraph_{bp.botid}')
            ], id=f'graphertab_{bp.botid}', className=format_tabs)
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
    if dbchoice == 'Stratpools':
        dbkeys = list(dbinstance.view_database()['data'].keys())
    else:
        dbkeys = list(dbinstance.view_database().keys())
    return dbinstance._dbname, dbinstance.__str__(), [{'label': x, 'value': x} for x in dbkeys], dbkeys[0]


@app.callback(
    # Output(f'dfcontent_{bp.botid}', 'data'),
    Output(f'level_0_content_{bp.botid}', 'children'),
    Output(f"level_1_choice_{bp.botid}", 'options'),
    Output(f"level_1_choice_{bp.botid}", 'value'),
    Output(f"keycontents_{bp.botid}", 'hidden'),
    Output(f"nextlevelkeys_{bp.botid}", 'hidden'),
    Output(f"tab_block_{bp.botid}", 'hidden'),
    Input(f"level_0_choice_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value')
    )
def gen_keycontents(dbkey, dbchoice):

    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if dbchoice == 'Stratpools':
        dictdata = dbinstance.view_database()['data'][dbkey]
        return None, [{'label': x, 'value': f"{x}{dbkey}"} for x in dictdata.keys()], f"{list(dictdata.keys())[0]}{dbkey}", 'hidden', None, None
    elif dbchoice == 'Portfolios':
        return None, [], "", 'hidden', 'hidden', None
    else:
        if dbchoice == 'Strategies':
            dictdata = dbinstance.view_item(dbkey).strategy_ingredients
        else:
            dictdata = dbinstance.view_item_details(dbkey)
            remove_nonrenderables(dictdata)
        return jsontodash(dictdata), [], "", None, 'hidden', 'hidden'


@app.callback(
    Output(f'dfcontent_{bp.botid}', 'data'),
    Input(f"level_1_choice_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value'),
    Input(f"level_0_choice_{bp.botid}", 'value'),
    Input(f"calib_{bp.botid}", "value"),
    )
def gen_stratpooldf(level1choice, dbchoice, dbkey, calibmode):
    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if level1choice and dbchoice == 'Stratpools':
        return dbinstance.view_database()['data'][level1choice[10:]][level1choice[:10]].itemdata.to_dict('records')
    elif dbchoice == 'Portfolios':
        df = dbinstance.view_item(dbkey)
        if calibmode == 'normalize':
            CloudGrapherData().convert_to_clouddf(df)
        return df.to_dict('records')
    else:
        pass


# gen graph
@app.callback(
    Output(f'dfgraph_{bp.botid}', 'figure'),
    Output(f"modeoptions_{bp.botid}", 'hidden'),
    Input(f"dfcontent_{bp.botid}", 'data'),
    Input(f"hovermode_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value'),
    Input(f"calib_{bp.botid}", "value"),
    )
def gen_cloudgraph(dfsource, hovermode, dbchoice, calibmode):
    modeoptions = 'hidden'
    if dfsource:
        df = pd.DataFrame.from_records(dfsource)
        if dbchoice == 'Stratpools':
            xaxis = 'stock'
            yaxes = df.columns
            yaxislabel = 'metricvalue'
            legendtitle = None
            fig = px.bar(df, x=xaxis, y=yaxes)

        elif dbchoice == 'Portfolios':
            yaxislabel = '$'
            if calibmode == 'normalize':
                yaxislabel = '% ("1" = 100%)'
            xaxis = 'date'
            yaxes = df.columns[1:]
            legendtitle = 'Tickers'
            fig = px.line(df, x=xaxis, y=yaxes, markers=False)
            fig.update_traces(connectgaps=True)
            modeoptions = None
    else:
        yaxislabel = '%'
        legendtitle = None
        fig = px.line(pd.DataFrame(data=[0]))
    fig.update_layout(transition_duration=500, yaxis_title=yaxislabel, legend_title_text=legendtitle, hovermode=hovermode, uirevision='some-constant')
    return fig, modeoptions
