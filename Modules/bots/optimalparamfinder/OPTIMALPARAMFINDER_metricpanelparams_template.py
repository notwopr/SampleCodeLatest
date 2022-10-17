"""
Title: Optimal Param Finder Metric List
Date Started: Mar 15, 2020
Version: 1.00
Version Start Date: July 9, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Template for filter version of metricpanel params.

METRICS NOT USED:
maxflatlitmus (requires preconceived preferences on thresholds)
maxbmflatlitmus (requires preconceived preferences on thresholds)
flatlinescorelitmus (requires preconceived preferences on thresholds)
bmflatlinescorelitmus (requires preconceived preferences on thresholds)


All metrics used:

smoothness_mean
smoothness_median

smoothness_std
smoothness_mad

dailynonzeromad
dailynonzerostd


age

bmflatlinescore
flatlinescore

meanbmflatseglen
meanflatseglen

maxbmflatseg
maxflatseg

maxbmflatliferatio
maxflatliferatio

maxdrop

squeezefactor_mean
squeezefactor_median

squeezefactor_std
squeezefactor_mad


winrateranker_MEAN (relies on pctrank)
winrateranker_MEDIAN (relies on pctrank)

winvolranker_STD (relies on pctrank)
winvolranker_MAD (relies on pctrank)

marketbeater (relies on pctrank)


"""
# MARKETBEATER SPECIFIC PARAMS
w_dow = 1/3
w_snp500 = 1/3
w_nasdaq = 1/3
w_pct_pos = 1/4
w_pct_neg = 1/4
w_avg_pos = 1/4
w_avg_neg = 1/4

mb_benchweights = [
    w_dow,
    w_snp500,
    w_nasdaq
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
                'metricname': 'bmflatlinescore',
                'rankascending': 1,
                'threshold': 1,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'flatlinescore',
                'rankascending': 1,
                'threshold': 1,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'meanbmflatseglen',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'meanflatseglen',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'maxflatseg',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatliferatio',
                'rankascending': 1,
                'threshold': 1,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'maxflatliferatio',
                'rankascending': 1,
                'threshold': 1,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'dailynonzerostd',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'dailynonzeromad',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'smoothness_mean',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'smoothraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'smoothness_median',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'smoothraw',
                'stat_type': 'median',
                'look_back': 0
            },
            {
                'metricname': 'smoothness_std',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'smoothraw',
                'stat_type': 'std',
                'look_back': 0
            },
            {
                'metricname': 'smoothness_mad',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'smoothraw',
                'stat_type': 'mad',
                'look_back': 0
            },
            {
                'metricname': 'squeezefactor_mean',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'mean',
                'look_back': 0
            },
            {
                'metricname': 'squeezefactor_median',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'median',
                'look_back': 0
            },
            {
                'metricname': 'squeezefactor_std',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'std',
                'look_back': 0
            },
            {
                'metricname': 'squeezefactor_mad',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'squeezeraw',
                'stat_type': 'mad',
                'look_back': 0
            },
            {
                'metricname': 'maxdrop',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'above',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'look_back': 0
            },
            {
                'metricname': 'winrateranker_mean',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'pctrank',
                'filterdirection': 'below',
                'metricweight': 0,
                'look_back': 0
            },
            {
                'metricname': 'winrateranker_median',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'pctrank',
                'filterdirection': 'below',
                'metricweight': 0,
                'look_back': 0
            },
            {
                'metricname': 'winvolranker_std',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'pctrank',
                'filterdirection': 'below',
                'metricweight': 0,
                'look_back': 0
            },
            {
                'metricname': 'winvolranker_mad',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'pctrank',
                'filterdirection': 'below',
                'metricweight': 0,
                'look_back': 0
            },
            {
                'metricname': 'marketbeater',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'pctrank',
                'filterdirection': 'below',
                'metricweight': 0,
                'calibration': 'noprepraw',
                'mweights': mb_metricweights,
                'bweights': mb_benchweights,
                'look_back': 0
            },
            {
                'metricname': 'age',
                'rankascending': 0,
                'threshold': 180,
                'thresholdtype': 'absolute',
                'filterdirection': 'above',
                'metricweight': 0,
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'metricpanel_params'
    }
]

# STORE
metricpanel_params_temp = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
