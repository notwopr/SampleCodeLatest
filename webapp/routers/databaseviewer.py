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
from dash import html
from dash.dependencies import Input, Output
from dashappobject import app
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
# from Modules.referencetools.dipdatevisualizer.DIPDATEVISUALIZER import dipdatevisualizer_dash
# from Modules.price_history import grabsinglehistory
from ..os_functions import get_currentscript_filename
# from ..common_resources import tickers
from ..dashinputs import dash_inputbuilder
from newbacktest.module_operations import ModuleOperations
from ..html_json import jsontodash, remove_nonrenderables

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

tbodydata = []
layout = html.Div([
    # html.Table(gen_tablecontents(tbodydata)),
    html.Span([html.B('Select a Database:')]),
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
        }),
    html.P([html.B('Database Name:'), html.Div(id=f'databasename_{bp.botid}')]),
    html.P([html.B('Database Info:'), html.Div(id=f'databaseinfo_{bp.botid}')]),
    html.P(html.B('Top level Keys:')),
    html.Div(
        dash_inputbuilder({
            'id': f'level_0_choice_{bp.botid}',
            'prompt': 'Choose a key to explore:',
            'inputtype': 'radio',
            'options': [],
            'value': "",
            }), id=f'level_0_{bp.botid}'),
    html.Span(html.B('Key Contents:')),
    html.Div(id=f'level_0_content_{bp.botid}'),
    dash_inputbuilder({
        'inputtype': 'table',
        'id': f"dfcontent_{bp.botid}",
        # 'filtering': 'native'
        }),
    html.Div(
        dash_inputbuilder({
            'id': f'level_1_choice_{bp.botid}',
            'prompt': 'Choose a key to explore:',
            'inputtype': 'radio',
            'options': [],
            'value': "",
            }), id=f'level_1_{bp.botid}'),
    dash_inputbuilder({
        'inputtype': 'table',
        'id': f"stratpooldfcontent_{bp.botid}",
        # 'filtering': 'native'
        })

])


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
    Output(f'dfcontent_{bp.botid}', 'data'),
    Output(f'level_0_content_{bp.botid}', 'children'),
    Output(f"level_1_choice_{bp.botid}", 'options'),
    Output(f"level_1_{bp.botid}", 'hidden'),
    Input(f"level_0_choice_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value')
    )
def gen_keycontents(dbkey, dbchoice):

    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if dbchoice == 'Portfolios':
        return dbinstance.view_item(dbkey).to_dict('records'), None, [], 'hidden'
    elif dbchoice == 'Stratpools':
        dictdata = dbinstance.view_database()['data'][dbkey]
        return None, None, [{'label': x, 'value': f"{x}{dbkey}"} for x in dictdata.keys()], None
    elif dbchoice == 'Strategies':
        return None, jsontodash(dbinstance.view_item(dbkey).strategy_ingredients), [], 'hidden'
    else:
        dictdata = dbinstance.view_item_details(dbkey)
        remove_nonrenderables(dictdata)
        return None, jsontodash(dictdata), [], 'hidden'


@app.callback(
    Output(f'stratpooldfcontent_{bp.botid}', 'data'),
    Input(f"level_1_choice_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value')
    )
def gen_stratpooldf(level1choice, dbchoice):
    if level1choice and dbchoice == 'Stratpools':

        dbinstance = ModuleOperations().getobject_byvarname(*db_directory['Stratpools'])()
        return dbinstance.view_database()['data'][level1choice[10:]][level1choice[:10]].itemdata.to_dict('records')
    else:
        pass
