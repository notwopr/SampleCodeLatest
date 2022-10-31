"""
Title: volstats functions
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from functools import partial
import multiprocessing as mp
#   THIRD PARTY IMPORTS
from dash import callback_context
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from Modules.price_calib import add_calibratedprices_portfolio
from Modules.metriclibrary.STRATTEST_FUNCBASE_MMBM import dropscoreratio_single
from Modules.list_functions import removedupes
from .grapher_helper_volstats_profile import VolStatProfile
from ..datatables import DataTableOperations
from webapp.routers.pricehistoryexplorer_helper_volstats_definitions import volstat_definitions


class VolStatFunctions:

    # get all calibrations needed metrics_to_run for single stock
    def get_all_calibs_single(self, metrics_to_run, pricedf, stock):
        # get list of all calibrations needed
        allcalibrations = [item for metricitem in metrics_to_run for item in metricitem['calibration']]
        allcalibrations = removedupes(allcalibrations)
        # get calibrated prices
        return add_calibratedprices_portfolio(pricedf, allcalibrations, [stock])

    # get dict of stock and its metricscores for metrics requested
    def getmetricvals_single(self, filterdf, beg_date, end_date, bench, stock):
        '''INSERT LISTOF DICTS OF METRICS TO RUN HERE'''
        metrics_to_run = VolStatProfile(stock).volstatprofile
        # add different benchmark versions of dropscore ratio
        benchnames_byticker = {
            '^DJI': 'Dow Jones',
            '^INX': 'S&P 500',
            '^IXIC': 'NASDAQ'
            }
        if len(bench) > 0:
            for b in bench:
                metrics_to_run.append(
                    {
                        'metricname': f'dropscoreratio_{benchnames_byticker[b]}',
                        'metricfunc': dropscoreratio_single,
                        'metricparams': {
                            'prices': None,
                            'uppercol': f'{stock}_baremaxraw',
                            'lowercol': stock,
                            'stat_type': 'avg',
                            'benchticker': b
                        },
                        'calibration': ['baremaxraw']
                    }
                )
        else:
            metrics_to_run.append(
                {
                    'metricname': 'dropscoreratio_NASDAQ',
                    'metricfunc': dropscoreratio_single,
                    'metricparams': {
                        'prices': None,
                        'uppercol': f'{stock}_baremaxraw',
                        'lowercol': stock,
                        'stat_type': 'avg',
                        'benchticker': '^IXIC'
                    },
                    'calibration': ['baremaxraw']
                }
            )

        '''END OF METRICS TO RUN LIST'''
        # get all required calibrations
        pricedf = self.get_all_calibs_single(metrics_to_run, filterdf[['date', stock]], stock)
        # update metricparams with new pricedf
        for m in metrics_to_run:
            m['metricparams'].update({'prices': pricedf})
        summary = {
            f'stock {beg_date} to {end_date}': stock
            }
        summary.update({f'{m["metricname"]}': m['metricfunc'](**m['metricparams']) for m in metrics_to_run})
        return summary

    # return df of stocks and their metricvals for all metrics requested
    def getallmetricvalsdf(self, filterdf, tickerlist, bench, beg_date, end_date):
        # FOR EACH STOCK IN POOL, GET METRIC VALUE
        pool = mp.Pool(mp.cpu_count())
        fn = partial(self.getmetricvals_single, filterdf, beg_date, end_date, bench)
        resultlist = pool.map_async(fn, tickerlist).get()
        pool.close()
        pool.join()
        # assemble dataframe of results
        resultdf = pd.DataFrame(data=resultlist)
        return resultdf

    def gen_volstats(self, ticker, portcurve, bench, sort_by, voldata, sourcetable):
        if voldata and callback_context.triggered[0]['prop_id'].endswith('sort_by'):
            # convert table back to dataframe
            voldf = pd.DataFrame.from_records(voldata)
            voldf = DataTableOperations().sort_datatable(sort_by, voldf)
            tooltip = {i: volstat_definitions[i] for i in voldf.columns[1:]}
        elif ticker:
            filterdf = pd.DataFrame.from_records(sourcetable)
            # because filterdf is converted to .to_dict('records') and then back from that; the date col type is changed to strings
            # as consequence have to change datecol back to original datatype: <class 'pandas._libs.tslibs.timestamps.Timestamp'>
            filterdf['date'] = filterdf['date'].apply(lambda x: pd.Timestamp(x))
            metdftickers = ticker+[f'bench_{b}' for b in bench]+['portcurve'] if 'portcurve' in portcurve else ticker+[f'bench_{b}' for b in bench]
            voldf = self.getallmetricvalsdf(filterdf, metdftickers, bench, str(filterdf.iat[0, 0].date()), str(filterdf.iat[-1, 0].date()))
            tooltip = {i: volstat_definitions[i] for i in voldf.columns[1:]}
        else:
            voldf = pd.DataFrame(data=['No ticker selected.'])
            tooltip = None
        return voldf.to_dict('records'), tooltip
