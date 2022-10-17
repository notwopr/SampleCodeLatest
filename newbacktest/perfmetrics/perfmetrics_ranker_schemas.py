'''
RANK rank_schema_sample
'''

rank_schemas = {
    0: {
        'growthrate_period': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'growthrate_period_bestbench': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'growthrate_period_margin': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'growthrate_effectivedaily': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'growthrate_effectivedaily_bestbench': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'growthrate_effectivedaily_margin': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP365#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.8::f4:byvalue::f6:>=': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP180#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.8::f4:byvalue::f6:>=': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP180#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.09::f4:byvalue::f6:>=': {
            'weight': 1/9,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        }
    },
    1: {
        'growthrate_effectivedaily': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'growthrate_effectivedaily_margin': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP365#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.8::f4:byvalue::f6:>=': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP180#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.8::f4:byvalue::f6:>=': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP180#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.09::f4:byvalue::f6:>=': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        }
    },
    2: {
        'WLP365#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.8::f4:byvalue::f6:>=': {
            'weight': 1,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP180#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.8::f4:byvalue::f6:>=': {
            'weight': 0,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP180#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.09::f4:byvalue::f6:>=': {
            'weight': 1,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'WLP360#::0a:74::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.12::f4:byvalue::f6:>=': {
            'weight': 1,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        }
    },
    3: {
        'growthrate_effectivedaily': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'growthrate_effectivedaily_margin': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'above_bench': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'above_zero': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        },
        'above_zero_and_bench': {
            'weight': 1/5,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        }
    },
    4: {
        "WLP180#::0a:75::0b:eodprices::0c:0::0d:raw::0e:ffillandremove::f1:value::f2:0.12::f4:byvalue::f6:>=": {
            'weight': 1,
            'rankdirection': 'd',
            'ranktype': 'percentile'
        }
    }
}
