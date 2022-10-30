"""
Title: Price Graph Explorer
Date Started: Feb 3, 2022
Version: 1.00
Version Start: Feb 3, 2022
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
from webapp.servernotes import getstockdata
#   LOCAL APPLICATION IMPORTS
from Modules.dataframe_functions import filtered_double
from Modules.datetime_functions import from_pts_to_dtdate
from ..botclasses import BotParams
from ..os_functions import get_currentscript_filename
from ..common_resources import tickers, staticmindate, staticmaxdate
from ..dashinputs import gen_tablecontents, prompt_builder, dash_inputbuilder
from formatting import format_tabs
from .pricehistoryexplorer_helper_graphcomp import PriceExplorerHelperFunctions

bp = BotParams(
    get_currentscript_filename(__file__),
    'Price Explorer',
    "Display the price graphs of any NYSE/NASDAQ stock and index.",
    None
)

# set date index dictionary and base df; otherwise cannot update graph with date range slider, because it requires storing data between callbacks which requires JSONifying.
eldate = getstockdata()
mdf = pd.DataFrame().reindex(pd.date_range(eldate["earliest"], eldate["latest"]))
mdf.reset_index(inplace=True)
mdf.rename(columns={'index': 'date'}, inplace=True)
mdf['date'] = mdf['date'].apply(lambda x: from_pts_to_dtdate(x))
mdf['$'] = 0

pdiffsettings = [
    {
        'id': f'graphdiff_mode_{bp.botid}',
        'prompt': 'Periodic difference measures arithmetic difference in value between adjacent periods. Periodic percent change measures the percent change difference between adjacent periods.',
        'inputtype': 'radio',
        'options': [
            {'label': 'Periodic Difference', 'value': 'pdiff'},
            {'label': 'Periodic Percent Change', 'value': 'pctchange'}
        ],
        'value': 'pctchange',
        'inline': 'inline'
        },
    {
        'id': f'graphdiff_changecol_{bp.botid}',
        'prompt': 'Select a calibration you want to compute the periodic change.',
        'inputtype': 'dropdown',
        'options': [],
        'value': 'all',
        'placeholder': 'select calibration',
        'multi': False,
        'searchable': False,
        'clearable': False
        },
    {
        'id': f'graphdiff_period_{bp.botid}',
        'prompt': 'Enter the period (in days) you want differences or percent change to calculated.  For example, period of 1 for mode "Periodic Percent Change" gives you a graph representing the daily percent change of the source calibration.',
        'inputtype': 'number',
        'value': 1,
        'min': 1,
        'step': 1,
        'debounce': True
        }
]
compsettings = [
    {
        'id': f'graphcompoptions_{bp.botid}',
        'prompt': 'Graphs proportion difference between two available calibrations A and B.  Thus, option "A to B" means it will output a graph such that the graph is a representation of (A - B) / B.',
        'inputtype': 'dropdown',
        'options': [],
        'placeholder': 'select comparison',
        'multi': False,
        'searchable': False,
        'clearable': True
        }
]
tbodydata = [
    {
        'id': f'ticker_{bp.botid}',
        'prompt': 'Select or Search for a Ticker(s).',
        'inputtype': 'dropdown',
        'options': tickers,
        'placeholder': 'Select or Search a Ticker(s)',
        'multi': True,
        'searchable': True,
        'clearable': True
        },
    {
        'id': f'calib_{bp.botid}',
        'prompt': 'Select a calibration.  Absolute is where the y-axis is in $.  Normalized is where all prices are standardized to the same scale.',
        'inputtype': 'radio',
        'options': [
            {'label': 'Absolute', 'value': 'absolute'},
            {'label': 'Normalized', 'value': 'normalize'}
        ],
        'value': 'absolute',
        'inline': 'inline'
        },
    {
        'id': f'portcurve_{bp.botid}',
        'prompt': '[*only available when normalized pricing is chosen and more than one stock is selected.  This option shows an aggregate growth curve of all selected stocks.]',
        'inputtype': 'checklist',
        'options': []
        },
    {
        'id': f'sd_{bp.botid}',
        'prompt': 'Choose a different start date. The current graphs are "cut" to that new start date. Helpful when using the normalized price view.',
        'inputtype': 'datepicker_single',
        'clearable': True,
        'min_date_allowed': staticmindate,
        'max_date_allowed': staticmaxdate
        },
    {
        'id': f'sd_bydd_{bp.botid}',
        'prompt': 'Or choose one of the start dates of one of the tickers already graphed.',
        'inputtype': 'dropdown',
        'options': [],
        'placeholder': 'Choose a start date',
        'multi': False,
        'clearable': True
        },
    {
        'id': f'contour_{bp.botid}',
        'prompt': 'Select whether you want to see the graphs in a different contour.',
        'details': 'Baremax displays the current all-time high price.  Baremin displays the floor price.  Trueline displays the midpoint between baremax and baremin prices.  Straight displays the straight line from first to last price.',
        'inputtype': 'checklist',
        'options': [
            {'label': 'Baremax', 'value': 'baremaxraw'},
            {'label': 'Baremin', 'value': 'oldbareminraw'},
            {'label': 'Trueline', 'value': 'trueline'},
            {'label': 'Straight', 'value': 'straight'}
        ]
        },
    {
        'id': f'bench_{bp.botid}',
        'prompt': 'Select a benchmark to compare against your portfolio.',
        'details': '',
        'inputtype': 'checklist',
        'options': [
            {'label': 'Dow Jones', 'value': '^DJI'},
            {'label': 'S&P 500', 'value': '^INX'},
            {'label': 'NASDAQ', 'value': '^IXIC'}
        ],
        'inline': 'inline'
        },
    {
        'id': f'hovermode_{bp.botid}',
        'prompt': 'Choose how you want to display data when you hover over the graph.',
        'inputtype': 'radio',
        'options': [{'label': x, 'value': x} for x in ['x', 'x unified', 'closest']],
        'value': 'closest',
        'inline': 'inline'
        }
]

layout = html.Div([
    html.Div([
        html.Table(gen_tablecontents(tbodydata), style={'width': '100%'}),
    ], id=f'input_{bp.botid}'),
    prompt_builder({
        'prompt': 'Date Range Slider',
        'id': f'dateslider_{bp.botid}',
        'inputtype': 'rangeslider',
        'min': 0,
        'max': len(mdf)-1,
        'value': [0, len(mdf)-1]
        }),
    html.Div(dash_inputbuilder({
        'inputtype': 'table',
        'id': f"sourcetable_{bp.botid}"
        }), id=f"hidden_{bp.botid}", hidden='hidden'),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(html.Div(dcc.Graph(id=f"graph_{bp.botid}", className=format_tabs)), label='Price History'),
        # dcc.Tab(label='Price History', children=[dcc.Graph(id=f"graph_{bp.botid}", className=format_tabs)]),
        dcc.Tab(html.Div([
            html.Table(gen_tablecontents(pdiffsettings)),
            dcc.Graph(id=f"graphdiff_{bp.botid}")
            ], className=format_tabs), label='Periodic Change'),
        dcc.Tab(html.Div([
            html.Table(gen_tablecontents(compsettings)),
            dcc.Graph(id=f"graphcomp_{bp.botid}")
            ], className=format_tabs), label='Comparative'),
        dcc.Tab(label='Volatility Metrics', children=[
            html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"voltable_{bp.botid}"
                }), className=format_tabs)
        ]),
        dcc.Tab(label='Raw Data', children=[
            html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"rawdata_{bp.botid}"
                }), className=format_tabs)])
    ])
])


@app.callback(
    Output(f"graph_{bp.botid}", "figure"),
    Output(f"graphdiff_{bp.botid}", "figure"),
    Output(f"graphcomp_{bp.botid}", "figure"),
    Output(f"dateslider_{bp.botid}", "min"),
    Output(f"sd_{bp.botid}", "min_date_allowed"),
    Output(f"sd_bydd_{bp.botid}", "options"),
    Output(f"sourcetable_{bp.botid}", "data"),
    Input(f"ticker_{bp.botid}", "value"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"sd_{bp.botid}", "date"),
    Input(f"sd_bydd_{bp.botid}", "value"),
    Input(f"contour_{bp.botid}", "value"),
    Input(f"graphcompoptions_{bp.botid}", "value"),
    Input(f"graphdiff_mode_{bp.botid}", "value"),
    Input(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"graphdiff_period_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value"),
    Input(f"bench_{bp.botid}", 'value'),
    Input(f"dateslider_{bp.botid}", 'value'),
    Input(f"hovermode_{bp.botid}", 'value')
    )
def gen_graph(ticker, calib, sd, sd_bydd, contour, graphcomp, gdm, gdc, gdp, portcurve, bench, date, hovermode):
    if ticker:
        df, compgraphcols, diffgraphcols, new_sd, all_sd = PriceExplorerHelperFunctions().gen_graph_df(staticmindate, ticker, calib, sd, sd_bydd, contour, graphcomp, gdm, gdc, gdp, portcurve, bench, hovermode)
        new_min = mdf.index[mdf['date'] == df['date'].iloc[0].date()].tolist()[0]
        filterdf = filtered_double(df, '>=<=', str(mdf['date'][date[0]]), str(mdf['date'][date[1]]), 'date')
    else:
        filterdf = mdf
        compgraphcols, diffgraphcols, ticker = '$', '$', '$'
        new_min = 0
        new_sd = staticmindate
        all_sd = []
    fig, fig_diff, fig_comp = PriceExplorerHelperFunctions().gen_graph_fig(filterdf, ticker, diffgraphcols, compgraphcols, hovermode)
    return fig, fig_diff, fig_comp, new_min, new_sd, all_sd, filterdf.to_dict('records')


@app.callback(
    Output(f"portcurve_{bp.botid}", "options"),
    Output(f"portcurve_{bp.botid}", "value"),
    Input(f"ticker_{bp.botid}", "value"),
    Input(f"calib_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value")
    )
def show_portcurve_option(ticker, calib, portcurvevalue):
    return PriceExplorerHelperFunctions().show_portcurve_option(ticker, calib, portcurvevalue)


# create options for diffgraph and comp graph
@app.callback(
    Output(f"graphcompoptions_{bp.botid}", "options"),
    Output(f"graphcompoptions_{bp.botid}", "value"),
    Output(f"graphdiff_changecol_{bp.botid}", "options"),
    Output(f"graphdiff_changecol_{bp.botid}", "value"),
    Input(f"contour_{bp.botid}", "value")
    )
def show_diffgraph_options(contour):
    return PriceExplorerHelperFunctions().show_diffgraph_options(contour)


# sort raw data table
# sourcetable is a hidden html DIV where orig filterdf is stored to be used by voldf and rawdatatable tab
@app.callback(
    Output(f"rawdata_{bp.botid}", "data"),
    Input(f"rawdata_{bp.botid}", 'sort_by'),
    Input(f"rawdata_{bp.botid}", "data"),
    Input(f"sourcetable_{bp.botid}", "data")
    )
def sort_rawdatatable(sort_by, rawdatatable, sourcetable):
    return PriceExplorerHelperFunctions().sort_rawdatatable(sort_by, rawdatatable, sourcetable)


# get volstats
@app.callback(
    Output(f"voltable_{bp.botid}", "data"),
    Output(f"voltable_{bp.botid}", "tooltip_header"),
    Input(f"ticker_{bp.botid}", "value"),
    Input(f"portcurve_{bp.botid}", "value"),
    Input(f"bench_{bp.botid}", 'value'),
    Input(f"voltable_{bp.botid}", 'sort_by'),
    Input(f"voltable_{bp.botid}", "data"),
    Input(f"sourcetable_{bp.botid}", "data")
    )
def gen_volstats(ticker, portcurve, bench, sort_by, voldata, sourcetable):
    return PriceExplorerHelperFunctions().gen_volstats(ticker, portcurve, bench, sort_by, voldata, sourcetable)
