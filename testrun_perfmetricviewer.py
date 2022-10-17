from newbacktest.portfolios.portfoliogenerator import PortfolioGenerator
from newbacktest.perfmetrics.winnerloser.getwlmetrics import GetWLMetrics
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater import PerfProfileUpdater
import pandas as pd
from newbacktest.perfmetrics.perfmetrics_ranker import PerfMetricRanker
from newbacktest.perfmetrics.perfmetrics_ranker_schemas import rank_schemas
teststrat_singlestage = [
    [
        {
            'metricfunc': 'globalvalgrab_single',
            # 'filterdirection': '>=<=',
            'sourcedata': 'eodprices',
            'nantreatment': 'ffillandremove',
            # 'threshold_type': 'byvalue',
            # 'threshold_value': [100, 1000],
            # 'filterby': 'value',
            'weight': 0.5,
            'rankdirection': 'd',
            'ranktype': 'percentile',
            'look_back': 5,
            'curvetype': 'raw',
            'valtype': 'max'
        },
        {
            'metricfunc': 'globalvalgrab_single',
            # 'filterdirection': '>=<=',
            'sourcedata': 'eodprices',
            'nantreatment': 'ffillandremove',
            # 'threshold_type': 'byvalue',
            # 'threshold_value': [100, 1000],
            # 'filterby': 'value',
            'weight': 0.5,
            'rankdirection': 'a',
            'ranktype': 'percentile',
            'look_back': 0,
            'curvetype': 'raw',
            'valtype': 'min'
        }
    ]
]
#
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
teststrat_2stage = [
    [
        {
            'metricfunc': 'globalvalgrab_single',
            'filterdirection': '>=',
            'sourcedata': 'eodprices',
            'nantreatment': 'ffillandremove',
            'threshold_type': 'byvalue',
            'threshold_value': 100,
            'filterby': 'value',
            # 'weight': 0.25,
            # 'rankdirection': 'd',
            # 'ranktype': 'percentile',
            'look_back': 0,
            'curvetype': 'raw',
            'valtype': 'last'
        },
        {
            'metricfunc': 'globalvalgrab_single',
            'filterdirection': '>=',
            'sourcedata': 'eodprices',
            'nantreatment': 'ffillandremove',
            'threshold_type': 'byvalue',
            'threshold_value': 10,
            'filterby': 'value',
            # 'weight': 0.25,
            # 'rankdirection': 'a',
            # 'ranktype': 'percentile',
            'look_back': 0,
            'curvetype': 'raw',
            'valtype': 'first'
        }
    ],
    [
        {
            'metricfunc': 'globalvalgrab_single',
            # 'filterdirection': '>=<=',
            'sourcedata': 'eodprices',
            'nantreatment': 'ffillandremove',
            # 'threshold_type': 'byvalue',
            # 'threshold_value': [100, 1000],
            # 'filterby': 'value',
            'weight': 0.5,
            'rankdirection': 'd',
            'ranktype': 'ordinal',
            'look_back': 0,
            'curvetype': 'raw',
            'valtype': 'last'
        },
        {
            'metricfunc': 'globalvalgrab_single',
            # 'filterdirection': '>=<=',
            'sourcedata': 'eodprices',
            'nantreatment': 'ffillandremove',
            # 'threshold_type': 'byvalue',
            # 'threshold_value': [100, 1000],
            # 'filterby': 'value',
            'weight': 0.5,
            'rankdirection': 'a',
            'ranktype': 'ordinal',
            'look_back': 0,
            'curvetype': 'raw',
            'valtype': 'first'
        }
    ]
]
#
if __name__ == '__main__':
    # PortfolioGenerator().generate(teststrat_2stage, 5, 180, 5, 0)
    # GetWLMetrics().get_wlperfmetrics(wlprofile, teststrat_2stage, 5, 180, 5, 0)
    rankschema = rank_schemas[4]
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(PerfMetricRanker().gen_rankdf(rankschema))
