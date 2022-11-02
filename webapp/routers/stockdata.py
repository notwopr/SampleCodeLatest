"""
Title: Stock Data Bot Endpoint
Date Started: Apr 8, 2022
Version: 1.00
Version Start: Apr 8, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Interface to update price data and view the data, like ticker lists, date ranges, and company names.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
from pathlib import Path
#   THIRD PARTY IMPORTS
from dash import html, dcc
from dash.dependencies import Input, Output
from dashappobject import app
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..dashinputs import gen_tablecontents, dash_inputbuilder
from ..botrun_parambuilder import brpb_base
from ..botclasses import BotParams
from Modules.updatepricedata.UPDATESTOCKDATA import updatestockdata
from Modules.dates_alpaca import getmostrecenttradingdate
from ..os_functions import get_currentscript_filename
from ..datatables import DataTableOperations
from formatting import format_tabs
from file_functions import readpkl
from file_hierarchy import DirPaths, FileNames
from webapp.servernotes import getlastmodified
from machinesettings import _machine

FULL_INFO_DB = Path(DirPaths().full_info_db)
daterangedb_name = FileNames().fn_daterangedb
fullinfodb_name = FileNames().fn_fullinfodb

bp = BotParams(
    get_currentscript_filename(__file__),
    'Stock Data Bot',
    "The Stock Data Bot is where you can update the stock price data to the latest available or view information on the price data, such as a list of tickers, company names, or date ranges.",
    updatestockdata
)

tbodydata = [
    {
        'id': f'updatebutton_{bp.botid}',
        'prompt': 'Click to download the latest stock data.',
        'buttontext': 'Update Stock Data',
        'inputtype': 'button_submit'
        }
]

# open ticker data file

layout = html.Div([
    html.Div([
        html.Table(gen_tablecontents(tbodydata)),
        html.Span(id=f'featurestatus_{bp.botid}', className='text-warning'),
        html.Div(id=f'updatestatus_{bp.botid}')
    ], id=f'input_{bp.botid}'),
    dcc.Tabs([
        dcc.Tab(label='Ticker Data', children=[
            dash_inputbuilder({
                'inputtype': 'table',
                'filtering': 'native',
                'id': f"tickertable_{bp.botid}"
                })
            ], className=format_tabs)
    ])
])


# update stock data
@app.callback(
    Output(f'updatebutton_{bp.botid}', 'disabled'),
    Output(f'featurestatus_{bp.botid}', 'children'),
    Input(f'updatebutton_{bp.botid}', 'n_clicks'),
    )
def update_button(n_clicks):
    if _machine.machinename == 'awsbeanstalk':
        return True, 'Feature disabled.'
    else:
        return False, None


# update stock data
@app.callback(
    Output(f'tickertable_{bp.botid}', 'data'),
    Output(f'tickertable_{bp.botid}', 'columns'),
    Output(f'updatestatus_{bp.botid}', "children"),
    Input(f'updatebutton_{bp.botid}', 'n_clicks'),
    Input(f'tickertable_{bp.botid}', 'sort_by')
    )
def update_stockdata(n_clicks, sort_by):
    df = readpkl(fullinfodb_name, FULL_INFO_DB)
    df = DataTableOperations().sort_datatable(sort_by, df)
    brp = brpb_base(bp.botid, 5)
    todaysdate = brp['todaysdate']
    date_lastrun = getlastmodified(FULL_INFO_DB, f"{fullinfodb_name}.pkl")[:10]
    mostrecenttradedate = getmostrecenttradingdate(todaysdate)
    update_summary = {
        "Today's date": todaysdate,
        "Last updated": date_lastrun,
        "Most recent trading date": mostrecenttradedate,
        "Update status": None
    }
    # do not update only if todaysdate is the same date as the date it was last updated or
    # if todaysdate is not the same as it was last updated, update it, unless doing so would not change any of the data, i.e. the last time it was updated was on or after the last available trading date.
    if n_clicks:
        if todaysdate == date_lastrun or dt.date.fromisoformat(date_lastrun) >= mostrecenttradedate:
            update_summary.update({"Update status": "Stock data is already up-to-date."})
        else:
            bp.botfunc(brp['chunksize'])
            update_summary.update({
                "Update status": "Update completed.",
                "Last updated": getlastmodified(FULL_INFO_DB, f'{fullinfodb_name}.pkl')[:10]
                })
    columns = DataTableOperations().hide_or_not(df, True)
    return df.to_dict('records'), columns, [html.P([html.Div([html.Span(f'{k}: {v}'), html.Br()]) for k, v in update_summary.items()])]
