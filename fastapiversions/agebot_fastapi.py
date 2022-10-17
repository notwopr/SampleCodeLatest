"""
Title: Age Bot Endpoint
Date Started: Jan 27, 2022
Version: 1.00
Version Start: Jan 27, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  To provide API endpoint for Age bot.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
#   THIRD PARTY IMPORTS
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from ..html import format_htmltable, html_entirepage, html_botinputscheme, html_multitable
from ..servernotes import server_stats, getstockdata
from ..botrun_parambuilder import brpb_base
from file_functions import delete_folder, getbotsinglerunfolder
from ..botclasses import BotParams
from Modules.bots.agebot.AGEBOT_BASE import agebotmaster
from ..os_functions import get_currentscript_filename

bp = BotParams(
    get_currentscript_filename(__file__),
    'Age Bot',
    "The Age Bot returns age stats on stocks based on the user's chosen growth requirements.  The ticker symbols considered are all United States NASDAQ and NYSE common stock.",
    agebotmaster
)
inputslist = [
    {
        'name': 'num_trials',
        'prompt': 'Number of trials:',
        'inputtype': 'number',
        'size': 3,
        'min': 1,
        'max': 100
        },
    {
        'name': 'testlen',
        'prompt': 'Test period length:',
        'inputtype': 'number',
        'size': 5,
        'min': 1,
        'max': 18000
        },
    {
        'name': 'rank_beg',
        'prompt': 'Rank batch start bound:',
        'inputtype': 'number',
        'size': 4,
        'min': 0,
        'max': 9999
        },
    {
        'name': 'rank_end',
        'prompt': 'Rank batch end bound:',
        'inputtype': 'number',
        'size': 4,
        'min': 0,
        'max': 9999
        },
    {
        'name': 'latestdate',
        'prompt': 'Enter trial date range end bound:',
        'inputtype': 'date',
        'min': getstockdata()["earliest"],
        'max': getstockdata()["latest"]
        },
    {
        'name': 'firstdate',
        'prompt': 'Enter trial date range start bound:',
        'inputtype': 'date',
        'min': getstockdata()["earliest"],
        'max': getstockdata()["latest"]
        },
    {
        'name': 'gr_u',
        'prompt': 'Set upper bound growth rate (1.00 = 100%):',
        'inputtype': 'float'
        },
    {
        'name': 'gr_l',
        'prompt': 'Set lower bound growth rate (1.00 = 100%):',
        'inputtype': 'float'
        },
    {
        'name': 'dir_u',
        'prompt': 'Filter stocks that are __ the upper bound growth rate:',
        'inputtype': 'filter'
        },
    {
        'name': 'dir_l',
        'prompt': 'Filter stocks that are __ the lower bound growth rate:',
        'inputtype': 'filter'
        },
    {
        'name': 'trialdates',
        'prompt': 'Enter trial dates manually. The number of dates selected must equal the number of trials selected. Use YYYY-MM-DD format. Separate each date with a comma.',
        'inputtype': 'datelist'
        }
]

router = APIRouter(
    prefix=bp.botpath,
    tags=[bp.botname]
)

layout = f'here is the {bp.botname}'


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
        num_trials: int = Form(...),
        testlen: int = Form(...),
        rank_beg: int | None = Form(None),
        rank_end: int | None = Form(None),
        latestdate: str | None = Form(None),
        firstdate: str = Form(...),
        gr_u: float | None = Form(None),
        gr_l: float | None = Form(None),
        dir_u: str | None = Form(None),
        dir_l: str | None = Form(None),
        trialdates: str | None = Form(None)
        ):
    # form bot run-specific parameters ('brp').
    brp = brpb_base(bp.botid, 1) | {
        'num_trials': num_trials,
        'testlen': testlen,
        'rank_beg': rank_beg,
        'rank_end': rank_end,
        'latestdate': '' if latestdate is None else latestdate,
        'firstdate': firstdate,
        'gr_u': gr_u,
        'gr_l': gr_l,
        'dir_u': dir_u,
        'dir_l': dir_l,
        'statictrialexistdates': [] if trialdates is None else list(map(str.strip, trialdates.split(',')))
        }
    # create table
    age_stats, trialsummaries = bp.botfunc(brp)
    age_stats_html = pd.DataFrame.to_html(age_stats, table_id=bp.botid, border=None, index=False)
    trialsummaries_html = pd.DataFrame.to_html(trialsummaries, table_id=bp.botid, border=None, index=False)
    # delete temp files and folder
    delete_folder(getbotsinglerunfolder(brp['rootdir'], brp['testregimename'], brp['todaysdate'], brp['testnumber']))
    # generate html response
    return HTMLResponse(content=html_entirepage(bp.botname, None, bp.botdesc, html_multitable([age_stats_html, trialsummaries_html]), server_stats), status_code=200)

'''format_htmltable(bp.botid)'''
