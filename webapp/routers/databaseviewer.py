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
import json
import simplejson
#   THIRD PARTY IMPORTS
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dashappobject import app
#   LOCAL APPLICATION IMPORTS
from ..botclasses import BotParams
# from Modules.referencetools.dipdatevisualizer.DIPDATEVISUALIZER import dipdatevisualizer_dash
# from Modules.price_history import grabsinglehistory
from ..os_functions import get_currentscript_filename
# from ..common_resources import tickers
from ..dashinputs import prompt_builder, gen_tablecontents, dash_inputbuilder
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater import PerfProfileUpdater
from newbacktest.module_operations import ModuleOperations

bp = BotParams(
    get_currentscript_filename(__file__),
    'Database Viewer',
    "Abstract Class to view databases.",
    None
)
# testdb = IngredientsDatabase().view_database()
tbodydata = []
layout = html.Div([
    # html.Table(gen_tablecontents(tbodydata)),
    html.Span([html.B('Select a Database:')]),
    dash_inputbuilder({
        'id': f'selectdb_{bp.botid}',
        'prompt': 'Select a Database',
        'inputtype': 'dropdown',
        'options': [{'label': k, 'value': k} for k in ['Ingredients', 'Stage Recipes', 'Strategies', 'Stratpools', 'Portfolios']],
        'placeholder': 'Choose an existing database',
        'value': 'Ingredients',
        'multi': False,
        'searchable': False,
        'clearable': False
        }),
    html.Span([html.B('Database Name:'), html.Div(id=f'databasename_{bp.botid}')]),
    html.Span(html.B('Top level Keys:')),
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
        })

])


@app.callback(
    Output(f'databasename_{bp.botid}', 'children'),
    Output(f'level_0_choice_{bp.botid}', 'options'),
    Output(f'level_0_choice_{bp.botid}', 'value'),
    Input(f"selectdb_{bp.botid}", 'value')
    )
def gen_dbname(dbchoice):
    db_directory = {
        'Ingredients': ('newbacktest.ingredients.db_ingredient', 'IngredientsDatabase'),
        'Stage Recipes': ('newbacktest.stagerecipes.db_stagerecipe', 'StageRecipeDatabase'),
        'Strategies': ('newbacktest.strategies.db_strategycookbook', 'StrategyCookBook'),
        'Stratpools': ('newbacktest.stratpools.db_stratpool', 'StratPoolDatabase'),
        'Portfolios': ('newbacktest.portfolios.db_portfolio', 'PortfolioDatabase')
    }
    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if dbchoice == 'Stratpools':
        dbkeys = list(dbinstance.view_database()['data'].keys())
    else:
        dbkeys = list(dbinstance.view_database().keys())
    return dbinstance._dbname, [{'label': x, 'value': x} for x in dbkeys], dbkeys[0]


@app.callback(
    Output(f'dfcontent_{bp.botid}', 'data'),
    Output(f'level_0_content_{bp.botid}', 'children'),
    Input(f"level_0_choice_{bp.botid}", 'value'),
    Input(f"selectdb_{bp.botid}", 'value')
    )
def gen_keycontents(dbkey, dbchoice):
    db_directory = {
        'Ingredients': ('newbacktest.ingredients.db_ingredient', 'IngredientsDatabase'),
        'Stage Recipes': ('newbacktest.stagerecipes.db_stagerecipe', 'StageRecipeDatabase'),
        'Strategies': ('newbacktest.strategies.db_strategycookbook', 'StrategyCookBook'),
        'Stratpools': ('newbacktest.stratpools.db_stratpool', 'StratPoolDatabase'),
        'Portfolios': ('newbacktest.portfolios.db_portfolio', 'PortfolioDatabase')
    }
    dbinstance = ModuleOperations().getobject_byvarname(*db_directory[dbchoice])()
    if dbchoice == 'Portfolios':
        dictdata = None
        dfdata = dbinstance.view_item(dbkey).to_dict('records')
    elif dbchoice == 'Stratpools':
        dictdata = str(dbinstance.view_database()['data'][dbkey])
        dfdata = None
    else:
        dictdata = str(dbinstance.view_item_details(dbkey))
        dfdata = None

    return dfdata, dictdata
