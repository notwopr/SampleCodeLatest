"""
Title: Dip Date Bot Endpoint
Date Started: Jan 31, 2022
Version: 1.00
Version Start: Jan 31, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..html import format_htmltable, html_entirepage, html_botinputscheme, html_multitable
from ..servernotes import server_stats, getstockdata
from ..botrun_parambuilder import brpb_base
from ..storagemgmt import delete_folder, getbotsinglerunfolder
from ..botclasses import BotParams
from Modules.referencetools.dipdatevisualizer.DIPDATEVISUALIZER import dipdatevisualizer
from Modules.tickers import get_tickerlist
from ..os_functions import get_currentscript_filename

bp = BotParams(
    get_currentscript_filename(__file__),
    'Dip Date Bot',
    "The Dip Date Bot takes a ticker symbol and date range and returns info on the largest drop in price during that span of time, including the exact dates of the fall, and the price change.",
    dipdatevisualizer,
    None
)

inputslist = [
    {
        'name': 'ticker',
        'prompt': 'Choose a stock:',
        'inputtype': 'dropdown',
        'contents': get_tickerlist('common+bench')
        },
    {
        'name': 'beg_date',
        'prompt': 'Enter start date:',
        'inputtype': 'date',
        'min': getstockdata()["earliest"],
        'max': getstockdata()["latest"]
        },
    {
        'name': 'end_date',
        'prompt': 'Enter end date:',
        'inputtype': 'date',
        'min': getstockdata()["earliest"],
        'max': getstockdata()["latest"]
        }
]

router = APIRouter(
    prefix=bp.botpath,
    tags=[bp.botname]
)


# BESTLETTER BOT INPUT PAGE
@router.get("/", response_class=HTMLResponse)
async def input_page():
    return HTMLResponse(content=
                        html_entirepage(
                            bp.botname,
                            '',
                            bp.botdesc,
                            html_botinputscheme(bp.botpath, bp.botrs, inputslist),
                            server_stats), status_code=200)


# BESTLETTER BOT OUTPUT PAGE
@router.post(bp.botrs, response_class=HTMLResponse)
async def result_page(
        ticker: str = Form(...),
        beg_date: str = Form(...),
        end_date: str = Form(...)
        ):
    # get func output
    output = bp.botfunc(ticker, beg_date, end_date)
    # generate html response
    return HTMLResponse(content=html_entirepage(bp.botname, '', bp.botdesc, output, server_stats), status_code=200)

'''format_htmltable(bp.botid)'''
