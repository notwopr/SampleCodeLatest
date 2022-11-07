# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
from dash import dcc, html
#   LOCAL APPLICATION IMPORTS
from formatting import format_tabs
from ..dashinputs import gen_tablecontents, dash_inputbuilder
from formatting_graphs import dccgraph_config


class GraphAssets:
    def __init__(self, bp):
        self.perf_graph_inputs = [
            {
                'id': f'perf_graph_ticker_{bp.botid}',
                'prompt': 'Select tickers from the full ranking list that you want to see.',
                'inputtype': 'dropdown',
                'options': [],
                'value': [],
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
                'id': f'sd_bydd_{bp.botid}',
                'prompt': 'Choose one of the start dates of one of the tickers already graphed.',
                'inputtype': 'dropdown',
                'options': [],
                'placeholder': 'Choose a start date',
                'multi': False,
                'clearable': True
                },
            {
                'id': f'datepicker_{bp.botid}',
                'prompt': 'Select a date range.',
                'inputtype': 'datepicker_range',
                'clearable': True
                },
            {
                'id': f'contour_{bp.botid}',
                'prompt': 'Select whether you want to see the graphs in a different contour.',
                'details': 'Baremax displays the current all-time high price.  Baremin displays the floor price.  Trueline displays the midpoint between baremax and baremin prices.  Straight displays the straight line from first to last price.',
                'inputtype': 'checklist',
                'options': [
                    {'label': 'Baremax', 'value': 'baremax'},
                    {'label': 'Baremin', 'value': 'baremin'},
                    {'label': 'Trueline', 'value': 'true'},
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

        self.pdiffsettings = [
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
                'placeholder': 'select calibration',
                'value': 'all',
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

        self.compsettings = [
            {
                'id': f'graphcompoptions_{bp.botid}',
                'prompt': 'Graphs proportion difference between two available raw calibrations A and B.  Thus, option "A to B" means it will output a graph such that the graph is a representation of (A - B) / B.',
                'inputtype': 'dropdown',
                'options': [],
                'placeholder': 'select comparison',
                'multi': False,
                'searchable': False,
                'clearable': True
                }
        ]

        self.perfgraphtab = html.Div([
            html.Table(gen_tablecontents(self.perf_graph_inputs)),
            # html.Div(dash_inputbuilder({
            #     'id': f'dateslider_{bp.botid}',
            #     'prompt': 'Date Range Slider',
            #     'inputtype': 'rangeslider'
            #     }), id=f"datesliderdiv_{bp.botid}"),
            html.Div(dash_inputbuilder({
                'inputtype': 'table',
                'id': f"graphdf_{bp.botid}"
                }), id=f"hidden_{bp.botid}", hidden='hidden'),
            html.Span(id=f"dfcol_{bp.botid}", hidden='hidden'),
            html.Br(),
            dcc.Tabs([
                dcc.Tab(html.Div(dcc.Graph(id=f"perf_graph_{bp.botid}", className=format_tabs, config=dccgraph_config)), label='Price History'),
                dcc.Tab(html.Div([
                    html.Table(gen_tablecontents(self.pdiffsettings)),
                    dcc.Graph(id=f"graphdiff_{bp.botid}", config=dccgraph_config)
                    ], className=format_tabs), label='Periodic Change'),
                dcc.Tab(html.Div([
                    html.Table(gen_tablecontents(self.compsettings)),
                    dcc.Graph(id=f"graphcomp_{bp.botid}", config=dccgraph_config)
                    ], className=format_tabs), label='Comparative'),
                dcc.Tab(label='Volatility Metrics', children=[
                    html.Div([
                        html.Table(gen_tablecontents([{
                            'id': f'voltbutton_{bp.botid}',
                            'inputtype': 'button_submit',
                            'buttontext': 'Calculate Volatility',
                            'prompt': 'Note: may take some time to complete.'
                            }])),
                        html.Br(),
                        dash_inputbuilder({
                            'inputtype': 'table',
                            'id': f"voltable_{bp.botid}"
                            })
                        ], className=format_tabs),
                    html.Div(dash_inputbuilder({
                        'inputtype': 'table',
                        'id': f"voltablesource_{bp.botid}"
                        }), hidden='hidden')
                ]),
                dcc.Tab(label='Raw Data', children=[
                    html.Div(dash_inputbuilder({
                        'inputtype': 'table',
                        'id': f"rawdata_{bp.botid}"
                        }), className=format_tabs)])
            ])])
