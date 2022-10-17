"""
Title: Screen Parameters - Summer 2020 Temp - Stage 2
Date Started: July 24, 2020
Version: 1.00
Version Start Date: July 24, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Temporary 2020 Summer Stage 2 Ranker.  Used to consider rebalancing of portfolio for short term temporary solution.

"""
# MARKETBEATER SPECIFIC PARAMS
w_dow = 1/3
w_snp500 = 1/3
w_nasdaq = 1/3
w_market = 0
w_pct_pos = 1/4
w_pct_neg = 1/4
w_avg_pos = 1/4
w_avg_neg = 1/4

mb_benchweights = [
    w_dow,
    w_snp500,
    w_nasdaq,
    w_market
]

mb_metricweights = {
    'pct_pos': w_pct_pos,
    'pct_neg': w_pct_neg,
    'avg_pos': w_avg_pos,
    'avg_neg': w_avg_neg
}
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'threshold': -0.30,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatliferatio',
                'rankascending': 1,
                'threshold': 0.30,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metric_category': 'pricestockandage',
                'metricweight': 1/6,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0.0005,
                'filterdirection': 'no',
                'metric_category': 'priceandstock',
                'metricweight': 1/6,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'volscore_composite',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': '^IXIC',
                'filterdirection': 'no',
                'metric_category': 'priceandstock',
                'metricweight': 1/6,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'normsqueezefactor_compositeavg',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metric_category': 'priceandstock',
                'metricweight': 1/6,
                'calibration': 'normsqueeze',
                'stat_type': 'compositeavg',
                'look_back': 0
            },
            {
                'metricname': 'marketbeater',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'pctrank',
                'filterdirection': 'no',
                'metricweight': 1/6,
                'calibration': 'noprepraw',
                'mweights': mb_metricweights,
                'bweights': mb_benchweights,
                'look_back': 0
            },
            {
                'metricname': 'winrateranker_composite',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'pctrank',
                'filterdirection': 'no',
                'metricweight': 1/6,
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'Summer2020temp'
    }
]

# STORE
research_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
