
class BestPerformerInputs:
    def __init__(self, bp, tickers):
        self.growthrateinputs = [
            {
                'id': f'growthrate_{bp.botid}',
                'prompt': 'Set growth rate threshold.  The threshold can be determined either by a specific number, by the growth rate of another stock or benchmark, or the best performing benchmark.',
                'options': [
                    {'label': 'By Ticker', 'value': 'byticker'},
                    {'label': 'By Best Benchmark', 'value': 'bybench'},
                    {'label': 'By specific number', 'value': 'bynumber'}
                ],
                'clearable': True,
                'inputtype': 'dropdown'
                },
            {
                'id': f'byticker_growthrate_{bp.botid}',
                'prompt': 'Choose a ticker to be the growth rate threshold.',
                'inputtype': 'dropdown',
                'options': tickers,
                'placeholder': 'Select or Type a Ticker',
                'searchable': True,
                'clearable': True
                },
            {
                'id': f'bynumber_growthrate_{bp.botid}',
                'prompt': 'Enter a growth rate threshold.',
                'inputtype': 'number'
                },
            {
                'id': f'growthrate_filter_{bp.botid}',
                'prompt': 'Keep stocks that are __ the growth rate threshold.',
                'options': ['>', '>=', '<', '<='],
                'inputtype': 'dropdown'
                },
            {
                'id': f'growthrate_margin_{bp.botid}',
                'prompt': 'By how much must a stock beat the growthrate threshold? This is added to the threshold value.  So if the filter direction is > or >= use a positive value.  If the filter direction is < or <=, use a negative value.',
                'inputtype': 'number'
                }
                ]

        self.fatscore_baremaxtoraw_inputs = [
            {
                'id': f'fatscore_baremaxtoraw_{bp.botid}',
                'prompt': 'Set fatscore_baremaxtoraw threshold.  The threshold can be determined either by a specific number, by the fatscore_baremaxtoraw of another stock or benchmark, or the best performing benchmark.',
                'options': [
                    {'label': 'By Ticker', 'value': 'byticker'},
                    {'label': 'By Best Benchmark', 'value': 'bybench'},
                    {'label': 'By specific number', 'value': 'bynumber'}
                ],
                'clearable': True,
                'inputtype': 'dropdown'
                },
            {
                'id': f'byticker_fatscore_baremaxtoraw_{bp.botid}',
                'prompt': 'Choose a ticker to be the fatscore_baremaxtoraw threshold.',
                'inputtype': 'dropdown',
                'options': tickers,
                'placeholder': 'Select or Type a Ticker',
                'searchable': True,
                'clearable': True
                },
            {
                'id': f'bynumber_fatscore_baremaxtoraw_{bp.botid}',
                'prompt': 'Enter a fatscore_baremaxtoraw threshold.',
                'inputtype': 'number',
                'max': 1,
                'min': 0
                },
            {
                'id': f'fatscore_baremaxtoraw_filter_{bp.botid}',
                'prompt': 'Keep stocks that are __ the fatscore_baremaxtoraw threshold.',
                'options': ['>', '>=', '<', '<='],
                'inputtype': 'dropdown'
                },
            {
                'id': f'fatscore_baremaxtoraw_margin_{bp.botid}',
                'prompt': 'By how much must a stock beat the fatscore_baremaxtoraw threshold? This is added to the threshold value.  So if the filter direction is > or >= use a positive value.  If the filter direction is < or <=, use a negative value.',
                'inputtype': 'number'
                }
                ]

        self.fatscore_baremaxtobaremin_inputs = [
            {
                'id': f'fatscore_baremaxtobaremin_{bp.botid}',
                'prompt': 'Set fatscore_baremaxtobaremin threshold.  The threshold can be determined either by a specific number, by the fatscore_baremaxtobaremin of another stock or benchmark, or the best performing benchmark.',
                'options': [
                    {'label': 'By Ticker', 'value': 'byticker'},
                    {'label': 'By Best Benchmark', 'value': 'bybench'},
                    {'label': 'By specific number', 'value': 'bynumber'}
                ],
                'clearable': True,
                'inputtype': 'dropdown'
                },
            {
                'id': f'byticker_fatscore_baremaxtobaremin_{bp.botid}',
                'prompt': 'Choose a ticker to be the fatscore_baremaxtobaremin threshold.',
                'inputtype': 'dropdown',
                'options': tickers,
                'placeholder': 'Select or Type a Ticker',
                'searchable': True,
                'clearable': True
                },
            {
                'id': f'bynumber_fatscore_baremaxtobaremin_{bp.botid}',
                'prompt': 'Enter a fatscore_baremaxtobaremin threshold.',
                'inputtype': 'number',
                'max': 1,
                'min': 0
                },
            {
                'id': f'fatscore_baremaxtobaremin_filter_{bp.botid}',
                'prompt': 'Keep stocks that are __ the fatscore_baremaxtobaremin threshold.',
                'options': ['>', '>=', '<', '<='],
                'inputtype': 'dropdown'
                },
            {
                'id': f'fatscore_baremaxtobaremin_margin_{bp.botid}',
                'prompt': 'By how much must a stock beat the fatscore_baremaxtobaremin threshold? This is added to the threshold value.  So if the filter direction is > or >= use a positive value.  If the filter direction is < or <=, use a negative value.',
                'inputtype': 'number'
                }
                ]

        self.drop_mag_inputs = [
            {
                'id': f'drop_mag_{bp.botid}',
                'prompt': 'Set drop_mag threshold.  The threshold can be determined either by a specific number, by the drop_mag of another stock or benchmark, or the best performing benchmark.',
                'options': [
                    {'label': 'By Ticker', 'value': 'byticker'},
                    {'label': 'By Best Benchmark', 'value': 'bybench'},
                    {'label': 'By specific number', 'value': 'bynumber'}
                ],
                'clearable': True,
                'inputtype': 'dropdown'
                },
            {
                'id': f'byticker_drop_mag_{bp.botid}',
                'prompt': 'Choose a ticker to be the drop_mag threshold.',
                'inputtype': 'dropdown',
                'options': tickers,
                'placeholder': 'Select or Type a Ticker',
                'searchable': True,
                'clearable': True
                },
            {
                'id': f'bynumber_drop_mag_{bp.botid}',
                'prompt': 'Enter a drop_mag threshold.',
                'inputtype': 'number',
                'max': 0,
                'min': -1
                },
            {
                'id': f'drop_mag_filter_{bp.botid}',
                'prompt': 'Keep stocks that are __ the drop_mag threshold.',
                'options': ['>', '>=', '<', '<='],
                'inputtype': 'dropdown'
                },
            {
                'id': f'drop_mag_margin_{bp.botid}',
                'prompt': 'By how much must a stock beat the drop_mag threshold? This is added to the threshold value.  So if the filter direction is > or >= use a positive value.  If the filter direction is < or <=, use a negative value.',
                'inputtype': 'number'
                }
                ]

        self.drop_prev_inputs = [
            {
                'id': f'drop_prev_{bp.botid}',
                'prompt': 'Set drop_prev threshold.  The threshold can be determined either by a specific number, by the drop_prev of another stock or benchmark, or the best performing benchmark.',
                'options': [
                    {'label': 'By Ticker', 'value': 'byticker'},
                    {'label': 'By Best Benchmark', 'value': 'bybench'},
                    {'label': 'By specific number', 'value': 'bynumber'}
                ],
                'clearable': True,
                'inputtype': 'dropdown'
                },
            {
                'id': f'byticker_drop_prev_{bp.botid}',
                'prompt': 'Choose a ticker to be the drop_prev threshold.',
                'inputtype': 'dropdown',
                'options': tickers,
                'placeholder': 'Select or Type a Ticker',
                'searchable': True,
                'clearable': True
                },
            {
                'id': f'bynumber_drop_prev_{bp.botid}',
                'prompt': 'Enter a drop_prev threshold.',
                'inputtype': 'number',
                'max': 1,
                'min': 0
                },
            {
                'id': f'drop_prev_filter_{bp.botid}',
                'prompt': 'Keep stocks that are __ the drop_prev threshold.',
                'options': ['>', '>=', '<', '<='],
                'inputtype': 'dropdown'
                },
            {
                'id': f'drop_prev_margin_{bp.botid}',
                'prompt': 'By how much must a stock beat the drop_prev threshold? This is added to the threshold value.  So if the filter direction is > or >= use a positive value.  If the filter direction is < or <=, use a negative value.',
                'inputtype': 'number'
                }
                ]

        self.dropscore_inputs = [
            {
                'id': f'dropscore_{bp.botid}',
                'prompt': 'Set dropscore threshold.  The threshold can be determined either by a specific number, by the dropscore of another stock or benchmark, or the best performing benchmark.',
                'options': [
                    {'label': 'By Ticker', 'value': 'byticker'},
                    {'label': 'By Best Benchmark', 'value': 'bybench'},
                    {'label': 'By specific number', 'value': 'bynumber'}
                ],
                'clearable': True,
                'inputtype': 'dropdown'
                },
            {
                'id': f'byticker_dropscore_{bp.botid}',
                'prompt': 'Choose a ticker to be the dropscore threshold.',
                'inputtype': 'dropdown',
                'options': tickers,
                'placeholder': 'Select or Type a Ticker',
                'searchable': True,
                'clearable': True
                },
            {
                'id': f'bynumber_dropscore_{bp.botid}',
                'prompt': 'Enter a dropscore threshold.',
                'inputtype': 'number',
                'max': 0,
                'min': -1
                },
            {
                'id': f'dropscore_filter_{bp.botid}',
                'prompt': 'Keep stocks that are __ the dropscore threshold.',
                'options': ['>', '>=', '<', '<='],
                'inputtype': 'dropdown'
                },
            {
                'id': f'dropscore_margin_{bp.botid}',
                'prompt': 'By how much must a stock beat the dropscore threshold? This is added to the threshold value.  So if the filter direction is > or >= use a positive value.  If the filter direction is < or <=, use a negative value.',
                'inputtype': 'number'
                }
                ]

        self.maxdd_inputs = [
            {
                'id': f'maxdd_{bp.botid}',
                'prompt': 'Set maxdd threshold.  The threshold can be determined either by a specific number, by the maxdd of another stock or benchmark, or the best performing benchmark.',
                'options': [
                    {'label': 'By Ticker', 'value': 'byticker'},
                    {'label': 'By Best Benchmark', 'value': 'bybench'},
                    {'label': 'By specific number', 'value': 'bynumber'}
                ],
                'clearable': True,
                'inputtype': 'dropdown'
                },
            {
                'id': f'byticker_maxdd_{bp.botid}',
                'prompt': 'Choose a ticker to be the maxdd threshold.',
                'inputtype': 'dropdown',
                'options': tickers,
                'placeholder': 'Select or Type a Ticker',
                'searchable': True,
                'clearable': True
                },
            {
                'id': f'bynumber_maxdd_{bp.botid}',
                'prompt': 'Enter a maxdd threshold.',
                'inputtype': 'number',
                'max': 0
                },
            {
                'id': f'maxdd_filter_{bp.botid}',
                'prompt': 'Keep stocks that are __ the maxdd threshold.',
                'options': ['>', '>=', '<', '<='],
                'inputtype': 'dropdown'
                },
            {
                'id': f'maxdd_margin_{bp.botid}',
                'prompt': 'By how much must a stock beat the maxdd threshold? This is added to the threshold value.  So if the filter direction is > or >= use a positive value.  If the filter direction is < or <=, use a negative value.',
                'inputtype': 'number'
                }
                ]

        self.perf_graph_inputs = [
            {
                'id': f'perf_graph_ticker_{bp.botid}',
                'prompt': 'Select tickers from the full ranking list that you want to see.',
                'inputtype': 'dropdown',
                'options': [],
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
                'prompt': 'Graphs proportion difference between two available calibrations A and B.  Thus, option "A to B" means it will output a graph such that the graph is a representation of (A - B) / B.',
                'inputtype': 'dropdown',
                'options': [],
                'placeholder': 'select comparison',
                'multi': False,
                'searchable': False,
                'clearable': True
                }
        ]
