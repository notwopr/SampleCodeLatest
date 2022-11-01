# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from itertools import permutations
#   THIRD PARTY IMPORTS
from dash import html
import plotly.express as px
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.datasource import DataSource
from newbacktest.curvecalibrator import CurveCalibrator
from webapp.servernotes import get_ipodate
from globalvars import benchmarks as benchmarksinfo


class GrapherHelperFunctions:

    def show_portcurve_option(self, ticker, calib, portcurvevalue):
        if ticker and calib == 'normalize' and len(ticker) > 1:
            return [
                {'label': 'Add portfolio graph', 'value': 'portcurve'}
            ], portcurvevalue

        else:
            return [], []

    def show_diffcomp_options(self, contour):
        if len(contour) == 0:
            return [], None, ['raw'], 'raw'
        else:
            p = permutations(contour + ['raw'], 2)
            return [{'label': f'{i[0]} to {i[1]}', 'value': f'{i[0]} {i[1]}'} for i in p], None, ['all', 'raw']+contour, 'all'

    def gen_graph_fig(self, df, pricegraphcols, diffgraphcols, compgraphcols, hovermode, yaxis, yaxis_diff):
        fig = px.line(df, x='date', y=pricegraphcols, markers=False)
        fig.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant', yaxis_title=yaxis)
        fig.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
        fig_diff = px.line(df, x='date', y=diffgraphcols, markers=False)
        fig_diff.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant', yaxis_title=yaxis_diff)
        fig_diff.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
        fig_comp = px.line(df, x='date', y=compgraphcols, markers=False)
        fig_comp.update_layout(transition_duration=500, legend_title_text='Ticker', hovermode=hovermode, uirevision='some-constant', yaxis_title='% (1=100%)')
        fig_comp.update_traces(hovertemplate='date=%{x|%Y-%m-%d}<br>value=%{y}')
        return fig, fig_diff, fig_comp

    def add_comparison_curves(self, df, uppercol, lowercol, portfolio, benchmarks, portcurve):
        allcompcols = []
        for s in portfolio+benchmarks:
            upper_label = s if uppercol == 'raw' else f'{s}_{uppercol}'
            lower_label = s if lowercol == 'raw' else f'{s}_{lowercol}'
            scolname = f'{s}_{uppercol}to{lowercol}'
            df[scolname] = (df[upper_label] - df[lower_label]) / df[lower_label]
            allcompcols.append(scolname)

        if 'portcurve' in portcurve:
            portcompcols = [f'{s}_{uppercol}to{lowercol}' for s in portfolio]
            df[f'portcurve_{uppercol}to{lowercol}'] = df[portcompcols].mean(axis=1)
            allcompcols.append(f'portcurve_{uppercol}to{lowercol}')
        return allcompcols

    def add_pdiffpctchange_portfolio(self, df, changecol, period, mode, portfolio):
        if changecol == 'all':
            sourcecols = portfolio
        elif changecol == 'raw':
            sourcecols = [s for s in portfolio if not any([b in s for b in ['baremax', 'baremin', 'straight', 'true']])]
        else:
            sourcecols = [s for s in portfolio if changecol in s]
        diffcols = [f'{s}_{period}d_{mode}' for s in sourcecols]
        if mode == 'pdiff':
            df[diffcols] = df[sourcecols].diff(periods=period)
        if mode == 'pctchange':
            df[diffcols] = df[sourcecols].pct_change(periods=period, fill_method='ffill')
        return diffcols

    def gen_graph_df(self, tickers, calib, start_date, end_date, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks):
        yaxis = '$'
        portfolio = tickers.copy()
        ds = DataSource().opends('eodprices_commonplusbench')
        df = DataFrameOperations().filter_column(ds, ['date']+tickers).copy()
        df.ffill(inplace=True)
        df.dropna(inplace=True, how='all', subset=tickers)
        df = DataFrameOperations().filtered_double(df, '>=<=', start_date, end_date, 'date')
        df.reset_index(drop=True, inplace=True)

        if benchmarks:
            bdf = DataSource().opends('eodprices_bench')
            bdf.ffill(inplace=True)
            bdf = DataFrameOperations().filter_column(bdf, ['date']+benchmarks)
            df = df.join(bdf.set_index('date'), how='left', on="date")
        tickers.extend(benchmarks)

        if calib == 'normalize':
            normvers = 'norm'
            CurveCalibrator().normalize_curves(df, normvers, tickers)
            yaxis = '% (1=100%)'
            pricegraphcols = [f'{c}_{normvers}' for c in tickers]
            if len(portfolio) > 1 and 'portcurve' in portcurve:
                df['portcurve'] = df[[f'{c}_{normvers}' for c in portfolio]].mean(axis=1)
                pricegraphcols += ['portcurve']
        else:
            pricegraphcols = tickers
        CurveCalibrator().add_curvetypes(df, contour, pricegraphcols)
        pricegraphcols.extend([f'{t}_{c}' for c in contour for t in pricegraphcols])

        if calib == 'normalize':
            CurveCalibrator().add_curvetypes(df, contour, portfolio + benchmarks)
        if graphcomp:
            gc_inputs = graphcomp.split(" ")
            compgraphcols = self.add_comparison_curves(df, gc_inputs[0], gc_inputs[1], portfolio, benchmarks, portcurve)
        else:
            compgraphcols = None

        targetdiffcols = pricegraphcols if calib != 'normalize' else portfolio + benchmarks + [f'{t}_{c}' for c in contour for t in portfolio + benchmarks]
        diffgraphcols = self.add_pdiffpctchange_portfolio(df, gdc, gdp, gdm, targetdiffcols)
        if gdm == 'pdiff':
            yaxis_diff = '$'
        if gdm == 'pctchange':
            yaxis_diff = '% (1=100%)'

        return df, pricegraphcols, compgraphcols, diffgraphcols, yaxis, yaxis_diff

    def gen_graph_output(self, callback_context, tickers, min_date_allowed, max_date_allowed, sd_bydd, pick_start, pick_end, calib, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks, hovermode, dfcol):
        nondatetriggers = [
            callback_context.triggered[0]['prop_id'].startswith('calib'),
            callback_context.triggered[0]['prop_id'].startswith('portcurve'),
            callback_context.triggered[0]['prop_id'].startswith('contour'),
            callback_context.triggered[0]['prop_id'].startswith('bench'),
            callback_context.triggered[0]['prop_id'].startswith('hovermode'),
            callback_context.triggered[0]['prop_id'].startswith('perf_graph_ticker')
                ]
        if tickers:
            benchtickers = [benchmarksinfo[k]['ticker'] for k in benchmarksinfo]
            toexclude = [t for t in tickers if t in benchtickers]
            all_sd = [{'label': f"{t}'s startdate", 'value': get_ipodate(t)} for t in tickers]

            '''modify date window'''
            if callback_context.triggered[0]['prop_id'].startswith('datepicker'):
                start_date = pick_start
                end_date = pick_end
                sd_bydd = None
            elif sd_bydd and callback_context.triggered[0]['prop_id'].startswith('sd_bydd'):
                start_date = sd_bydd
                end_date = pick_end
            # do not change graph window if graph already present (that's what dfcol is for)
            elif any(nondatetriggers) and dfcol > 2:
                start_date = pick_start
                end_date = pick_end
            else:
                start_date = min_date_allowed
                end_date = max_date_allowed

            df, pricegraphcols, compgraphcols, diffgraphcols, yaxis, yaxis_diff = GrapherHelperFunctions().gen_graph_df(tickers, calib, start_date, end_date, contour, graphcomp, gdm, gdc, gdp, portcurve, benchmarks)
        else:
            df = pd.DataFrame(data={'date': pd.date_range(min_date_allowed, max_date_allowed), '$': 0})
            pricegraphcols, compgraphcols, diffgraphcols = '$', '$', '$'
            all_sd = []
            yaxis = '$'
            yaxis_diff = '%'
            start_date = min_date_allowed
            end_date = max_date_allowed
            toexclude = []

        fig, fig_diff, fig_comp = self.gen_graph_fig(df, pricegraphcols, diffgraphcols, compgraphcols, hovermode, yaxis, yaxis_diff)

        return fig, fig_diff, fig_comp, df.to_dict('records'), all_sd, min_date_allowed, max_date_allowed, start_date, end_date, [
                html.Span("Min Date Allowed: "),
                html.Span(min_date_allowed, className='fadedpurple_txt'),
                html.Span(" | Max Date Allowed: "),
                html.Span(max_date_allowed, className='fadedpurple_txt')
                ], sd_bydd, [{'label': benchmarksinfo[k]['name'], 'value': benchmarksinfo[k]['ticker'], 'disabled': benchmarksinfo[k]['ticker'] in toexclude} for k in benchmarksinfo], len(df.columns)
