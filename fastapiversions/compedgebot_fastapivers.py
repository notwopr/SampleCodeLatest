"""
Title: Competitive Edge Bot Endpoint
Date Started: Feb 1, 2022
Version: 1.00
Version Start: Feb 1, 2022
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
from ..html import format_htmltable, html_entirepage, html_botinputscheme, html_multitable, html_listcontents, html_multireports
from ..servernotes import server_stats, getstockdata
from ..botrun_parambuilder import brpb_base
from ..storagemgmt import delete_folder, getbotsinglerunfolder
from ..botclasses import BotParams
from Modules.referencetools.businessmodel.businessmodelbot_base import comp_edge_needed, gen_fundprofiles, gen_fund_df
from Modules.tickers import get_tickerlist
from ..os_functions import get_currentscript_filename

bp = BotParams(
    get_currentscript_filename(__file__),
    'Competitive Edge Bot',
    "The Competitive Edge Bot returns the hypothetical growth rate your fund must achieve if you want to win over clients as compared to a competitor.",
    comp_edge_needed,
    None
)
layout = f'here is the {bp.botname}'
inputslist = [
    {
        'name': 'your_name',
        'prompt': 'Enter the name of your fund (use letters only please):',
        'inputtype': 'text',
        'pattern': "\b[A-Za-z ]"
        },
    {
        'name': 'comp_name',
        'prompt': 'Enter the name of your competitor (use letters only please):',
        'inputtype': 'text',
        'pattern': "\b[A-Za-z ]"
        },
    {
        'name': 'client_principal',
        'prompt': 'Client principal: Enter the amount a hypothetical client would have to invest (in $):',
        'inputtype': 'float'
        },
    {
        'name': 'num_clients',
        'prompt': 'Enter the number of clients your fund would have:',
        'inputtype': 'number',
        'size': 5,
        'min': 0,
        'max': 99999
        },
    {
        'name': 'comp_num_clients',
        'prompt': 'Enter the number of clients your competitor would have:',
        'inputtype': 'number',
        'size': 5,
        'min': 0,
        'max': 99999

        },
    {
        'name': 'perf_cut',
        'prompt': 'Your Performance Cut: enter the portion of gains your clients earned would go to you.  (For example, if your client money grew by $100, and you entered 0.25, your cut would be 25% of $100, or $25.):',
        'inputtype': 'float'
        },
    {
        'name': 'comp_perf_cut',
        'prompt': 'Competitor Performance Cut:',
        'inputtype': 'float'
        },
    {
        'name': 'aum_rate',
        'prompt': 'Your AUM Rate: Enter the proportion of the Client Principal that would go to you as a fee for managing client assets:',
        'inputtype': 'float'
        },
    {
        'name': 'comp_aum_rate',
        'prompt': 'Enter competitor AUM Rate:',
        'inputtype': 'float'
        },
    {
        'name': 'mkt_perf',
        'prompt': 'Enter hypothetical performance of the market (Example: if you entered 0.12, the market growth rate would be 12% over the time period being considered.):',
        'inputtype': 'float'
        },
    {
        'name': 'your_perf',
        'prompt': 'Enter hypothetical performance of your fund over the time period being considered:',
        'inputtype': 'float'
        },
    {
        'name': 'comp_perf',
        'prompt': 'Enter hypothetical performance of the competitor fund over the time period being considered:',
        'inputtype': 'float'
        },
    {
        'name': 'switch_factor',
        'prompt': 'Switch Factor: The switch factor is how much more must the client earn with your fund than with the competitor for the client to switch to your fund.  This is represented as a proportion of the amount client would have gained had it gone with the competitor.  For example, if the switch factor was 0.05, and the client grew his money by $100 investing thru the competitor after all fees were paid, then for the client to go with us, the client would need to have earned 5% more than that, or $5 (0.05 of $100), for a total gain of $105. If the client earned only $102 through your fund, that means the client would not switch to you because they would have earned only $2 more, or 2%, which is less than the 5% switch factor:',
        'inputtype': 'float'
        },
    {
        'name': 'overhead_cost',
        'prompt': 'Your Overhead Cost: Enter the total overhead cost you would incur over the time period being considered:',
        'inputtype': 'float'
        },
    {
        'name': 'comp_overhead_cost',
        'prompt': 'Competitor Overhead Cost: Enter the total overhead cost the competitor would incur over the time period being considered:',
        'inputtype': 'float'
        },
    {
        'name': 'perf_fee_regime',
        'prompt': 'Performance Fee Regime: Choose a performance fee regime for your fund.  A performance fee regime determines under which circumstances your fund earns a fee based on how well the fund performs.  "v1" is a world where your fund does not earn a performance fee if the fund is losing money or it is losing against the market.  Your fund would instead pay the client the amount by which the fund is losing against the market, or if the fund is at a loss but still beating the market, it will pay the client to make them whole.  "v2" is a world where a performance fee is paid regardless whether the fund is losing money or not so long as it is beating the market.  "v3" is a world where a performance fee is paid only if the fund grows and beats the market.  Whichever option you choose, the performance fee calculated for when the fund earns a fee is determined by the performance cut rate you selected:',
        'inputtype': 'dropdown',
        'contents': ['v1', 'v2', 'v3']
        },
    {
        'name': 'comp_perf_fee_regime',
        'prompt': 'Competitor Performance Fee Regime: Choose a performance fee regime for competitor fund:',
        'inputtype': 'dropdown',
        'contents': ['v1', 'v2', 'v3']
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
        your_name: str = Form(...),
        comp_name: str = Form(...),
        client_principal: float = Form(...),
        num_clients: int = Form(...),
        comp_num_clients: int = Form(...),
        perf_cut: float = Form(...),
        comp_perf_cut: float = Form(...),
        aum_rate: float = Form(...),
        comp_aum_rate: float = Form(...),
        mkt_perf: float = Form(...),
        your_perf: float = Form(...),
        comp_perf: float = Form(...),
        switch_factor: float = Form(...),
        overhead_cost: float = Form(...),
        comp_overhead_cost: float = Form(...),
        perf_fee_regime: str = Form(...),
        comp_perf_fee_regime: str = Form(...)
        ):
    # form bot run-specific parameters ('brp').
    brp = {
        'your_name': your_name,
        'comp_name': comp_name,
        'client_principal': client_principal,
        'num_clients': num_clients,
        'comp_num_clients': comp_num_clients,
        'perf_cut': perf_cut,
        'comp_perf_cut': comp_perf_cut,
        'aum_rate': aum_rate,
        'comp_aum_rate': comp_aum_rate,
        'mkt_perf': mkt_perf,
        'your_perf': your_perf,
        'comp_perf': comp_perf,
        'switch_factor': switch_factor,
        'overhead_cost': overhead_cost,
        'comp_overhead_cost': comp_overhead_cost,
        'perf_fee_regime': perf_fee_regime,
        'comp_perf_fee_regime': comp_perf_fee_regime
    }
    # get func output
    your_fund, comp_fund, mkt_fund = gen_fundprofiles(brp)
    output = bp.botfunc(brp)
    html_df = pd.DataFrame.to_html(gen_fund_df([your_fund, comp_fund, mkt_fund]), table_id=bp.botid, border=None, index=False)
    html_report = html_listcontents(output)
    # generate html response
    return HTMLResponse(content=html_entirepage(bp.botname, '', bp.botdesc, html_multireports([html_report, html_df]), server_stats), status_code=200)

'''format_htmltable(bp.botid)'''
