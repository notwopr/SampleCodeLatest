# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
# from newbacktest.perfmetrics_ranker_schemas import rank_schemas
# from newbacktest.perfmetrics_ranker import Ranker
# from newbacktest.perfmetrics_getwlmetricsforstrategy import WLMetricsOnStrategy
# from newbacktest.db_stratpool import StratPoolDatabase
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater_perfmetricnames import PerfMetricNameDatabase
# from newbacktest.perfmetrics_perfprofileupdater import PerfProfileUpdater
# from pprintpp import pprint
# from newbacktest.portfoliogenerator import PortfolioGenerator
# from newbacktest.db_metricfunction import MetricFunctionDatabase
# from newbacktest.datasource import DataSource
# from newbacktest.dataframe_operations import DataFrameOperations
# from newbacktest.db_portfolio import PortfolioDatabase
# from newbacktest.db_sampcode import SampleCodeDatabase
# from newbacktest.class_sampcode import SampCode
# from newbacktest.class_cloudsampcode import CloudSampCode
from newbacktest.cloudgrapher.cloudsampgenerator import CloudSampleGenerator
# from newbacktest.db_cloudsample import CloudSampleDatabase
# from newbacktest.growthcalculator import GrowthCalculator
# from newbacktest.class_investplan import InvestPlanCode
if __name__ == '__main__':
    wlprofile = [
        {
            'metricfunc': 'getpctchange_single',
            'filterdirection': '>=',
            'sourcedata': 'eodprices',
            'nantreatment': 'ffillandremove',
            'threshold_type': 'byvalue',
            'threshold_value': 0.12,
            'filterby': 'value',
            'look_back': 0,
            'curvetype': 'raw'
        }
    ]
    strategydict = [
        [
            {
                'metricfunc': 'drawdown_to_ipotoathdiff_single',
                # 'filterdirection': '>',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                # 'threshold_type': 'byvalue',
                # 'threshold_value': 0,
                # 'filterby': 'value',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1,
                'ranktype': 'percentile',
                'rankdirection': 'd'
                # 'occurtype': 'last',
                # 'compmode': 'last'
            }
        ]
    ]
    # ds = DataSource().opends('eodprices_bench')
    # ds.ffill(inplace=True)
    # print(ds)
    # ds = DataFrameOperations().filtered_double(ds, '>=<=', '1980-05-22', '1980-05-31', 'date')
    # print(ds)
    # exit()

    # seriesdata = ds.loc[:, 'AAPL']
    # seriesdata.dropna(inplace=True)
    # print(seriesdata)
    # print(ipotoathslope_single('first', seriesdata))
    # exit()
    # wlmos = WLMetricsOnStrategy(wlprofile, strategydict, 1, 360, 10, 0)
    # wlmos.get_wlperfmetrics_for_strategy()
    # print(MetricFunctionDatabase().view_database().keys())
    # pprint(PortfolioDatabase().view_database())
    # exit()

    # num_periods = 5
    # periodlen = 360
    # portsize = 5
    # batchstart = 0
    #
    # CloudSampleGenerator().generate(strategydict, periodlen, portsize, batchstart, 1, num_periods)
    # exit()
    # sampcode = 'SCTG|0$f#::0a:123::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.002::f4:byvalue::f6:<=::m1:first::m2:last.IP.10.360.0.1.2017-06-05'
    # scobj = SampCode().decode(sampcode)
    # ipcode = scobj['ipcode']
    # pprint(InvestPlanCode().decode(ipcode))
    # stratcode = scobj['stratcode']
    # cloudsamp_startdate = scobj['invest_startdate']
    # CloudSampleGenerator().generate_bycode(stratcode, ipcode, 1, num_periods)
    # exit()
    # cloudsampcode = 'CDTG|0$f#::0a:128::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0::f4:byvalue::f6:>.IP.10.360.0.1.2.1986-09-08'
    # cso = CloudSampleDatabase().view_item(cloudsampcode).itemdata
    # pprint(cso)
    # for period, sampcode in cso.items():
    #     portfoliodf = PortfolioDatabase().view_item(sampcode)
    #     portfolio = portfoliodf.columns[1:]
    #     GrowthCalculator().getnormpricesdf(portfoliodf, portfolio)
    #     portfoliodf['portcurve'] = portfoliodf[portfolio].mean(axis=1)
    #     print(portfoliodf)
    # exit()

    # pg = PortfolioGenerator(strategydict, 1, 360, 10, 0, '1999-06-04', '2000-05-30')
    # pg.generate()
    # print(StratPoolDatabase().view_stratpool('TG|0$f#::0a:128::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0::f4:byvalue::f6:>', '1999-06-04').itemdata)
    # exit()
    '''add new perfmetricnames'''
    PerfMetricNameDatabase().add_item(['above_bench', 'above_zero', 'above_zero_and_bench'])
    '''update perf profiles'''
    PerfProfileUpdater().update_profiles()
    '''rank perfprofiles'''
    rankschema = rank_schemas[3]
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(Ranker().gen_rankdf(rankschema))