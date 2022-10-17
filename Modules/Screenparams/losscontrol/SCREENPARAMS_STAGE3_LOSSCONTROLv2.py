"""
Title: SCREENPARAMS - STAGE 3 - LOSS CONTROL
Date Started: Oct 30, 2020
Version: 2.00
Version Start Date: Oct 30, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description: Same as v1 except remove negseg to life ratios because no matter how old the stock is the consecutive neg loss range will not deviate much.  The reason to keep the baremax to life ratios though is because bmaxseglen does seem to depend on age, so we would have to control for age by using a len to life ratio.

Loss Control
    Baremax Flatness 1/4
        average length 1/2
            absolute length 1/2
                statseglen_bmax_mean 1/2
                statseglen_bmax_median 1/2
            length to life ratio 1/2
                seglife_bmax_mean 1/2
                seglife_bmax_median 1/2
        max length 1/2
            absolute length 1/2
                statseglen_bmax_max
            length to life ratio 1/2
                seglife_bmax_max
    Consecutive Negative Losses 1/4
        Average Length 1/2
            statseglen_negseg_mean 1/2
            statseglen_negseg_median 1/2
        Max Length 1/2
            statseglen_negseg_max
    daily drops 1/4
        average daily drops 1/3
            posnegmag_neg_mean 1/2
            posnegmag_neg_median 1/2
        max daily drop 1/3
            posnegmag_neg_max
        posnegprev_neg 1/3
    any-timespan drops 1/4
        average any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_mean 1/2
            allpctdrop_rawoldbareminraw_median 1/2
        max any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_max
"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'STAGE3_LOSSCONTROLv2',
    'scriptparams': [
        {
            'metricname': 'statseglen_bmax_mean',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmax_median',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_mean',
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_median',
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmax_max',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_max',
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_mean',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2),
            'mode': 'negative',
            'stat_type': 'mean',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_median',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2),
            'mode': 'negative',
            'stat_type': 'median',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_max',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2),
            'mode': 'negative',
            'stat_type': 'max',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'mean',
            'metricweight': (1/4)*(1/3)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_median',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'median',
            'metricweight': (1/4)*(1/3)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_max',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'min',
            'metricweight': (1/4)*(1/3),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevalence_neg',
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'metricweight': (1/4)*(1/3),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'mean',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_median',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'median',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_max',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/4)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'max',
            'look_back': 0
        }
        ]
    }
