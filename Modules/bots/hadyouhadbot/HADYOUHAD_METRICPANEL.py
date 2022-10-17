"""
Title: METRIC PANEL FOR HAD YOU HAD BOT
Date Started: Nov 3, 2020
Version: 1.00
Version Start Date: Nov 3, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: This param config gives you a ranking by volatility.  Previous measures of volatility are misleading (e.g. volscore, where std of dailypercentchanges is calculated).  See Investment Research Journal Part 5 10.11.20 entry for explanation.
Description:
Loss Control
    shape 1/5
        squeezearea 1/2
        smootharea 1/2
    any-timespan drops 1/5
        average any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_mean 1/2
            allpctdrop_rawoldbareminraw_median 1/2
        max any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_max
    Baremax Flatness 1/5
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
    Consecutive Negative Losses 1/5
        Average Length 1/3
            Absolute Length 1/2
                statseglen_negseg_mean 1/2
                statseglen_negseg_median 1/2
            length to life ratio 1/2
                seglife_negseg_mean 1/2
                seglife_negseg_median 1/2
        Max Length 1/3
            Absolute Length 1/2
                statseglen_negseg_max
            length to life ratio 1/2
                seglife_negseg_max
        psegnegsegratio 1/3
            psegnegsegratio_mean 1/2
            psegnegsegratio_median 1/2
    daily drops 1/5
        average daily drops 1/3
            posnegmag_neg_mean 1/2
            posnegmag_neg_median 1/2
        max daily drop 1/3
            posnegmag_neg_max
        posnegprev_neg 1/3

"""
from STRATTEST_FUNCBASE_RAW import statseglen_single, segliferatio_single,    posnegprevalence_single, posnegmag_single, psegnegsegratio_single
from STRATTEST_FUNCBASE_MMBM import smoothsqueezeshell, allpctdrops_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
hadyouhad_params = {
    'scriptname': 'HADYOUHAD_METRICPANEL',
    'scriptparams': [
        {
            'metricname': 'squeezearea',
            'metricfunc': smoothsqueezeshell,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2),
            'stat_type': 'area',
            'calibration': 'squeezeraw',
            'look_back': 0
        },
        {
            'metricname': 'smootharea',
            'metricfunc': smoothsqueezeshell,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2),
            'stat_type': 'area',
            'calibration': 'smoothraw',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_max',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'max',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_mean',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'mean',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_median',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'median',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmax_mean',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmax_median',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_mean',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_median',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmax_max',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmax_max',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_mean',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2)*(1/2),
            'mode': 'negative',
            'stat_type': 'mean',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_median',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2)*(1/2),
            'mode': 'negative',
            'stat_type': 'median',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_negseg_mean',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2)*(1/2),
            'mode': 'negative',
            'stat_type': 'mean',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_negseg_median',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2)*(1/2),
            'mode': 'negative',
            'stat_type': 'median',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_max',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2),
            'mode': 'negative',
            'stat_type': 'max',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_negseg_max',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2),
            'mode': 'negative',
            'stat_type': 'max',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'psegnegsegratio_mean',
            'metricfunc': psegnegsegratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2),
            'stat_type': 'mean',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'psegnegsegratio_median',
            'metricfunc': psegnegsegratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/5)*(1/3)*(1/2),
            'stat_type': 'median',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_mean',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'mean',
            'metricweight': (1/5)*(1/3)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_median',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'median',
            'metricweight': (1/5)*(1/3)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_neg_max',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'min',
            'metricweight': (1/5)*(1/3),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevalence_neg',
            'metricfunc': posnegprevalence_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'metricweight': (1/5)*(1/3),
            'calibration': 'raw',
            'look_back': 0
        }
        ]
    }
