"""
Title:  MANUAL REVIEW SCRIPT - PARAMSCRIPT FOR GRAPH GRADING
Date Started: Nov 4, 2020
Version: 1.00
Version Start Date: Nov 4, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Components:
    stagnation 1/6
        average length 1/2
            absolute length 1/2
                statseglen_bmin_mean 1/2
                statseglen_bmin_median 1/2
            length to life ratio 1/2
                seglife_bmin_mean 1/2
                seglife_bmin_median 1/2
        max length 1/2
            absolute length 1/2
                statseglen_bmin_max
            length to life ratio 1/2
                seglife_bmax_max
    recovery 1/6
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
    drawdowns 1/6
        average any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_mean 1/2
            allpctdrop_rawoldbareminraw_median 1/2
        max any-timespan drops 1/2
            allpctdrop_rawoldbareminraw_max
    Magnitude DPC 1/6
        loss 1/3
            max loss 1/2
                posnegmag_neg_max
            avg loss 1/2
                posnegmag_neg_mean 1/2
                posnegmag_neg_median 1/2
        gain 1/3
            max gain 1/2
                posnegmag_pos_max
            avg gain 1/2
                posnegmag_pos_mean 1/2
                posnegmag_pos_median 1/2
        gain:loss 1/3
            posnegmagratio_mean 1/2
            posnegmagratio_median 1/2
    Frequency DPC 1/6
        gain 1/3
            posnegprev_pos
        loss 1/3
            posnegprev_neg
        gain:loss 1/3
            posnegprevratio
    Consecutive DPC 1/6
        consec loss 1/3
            avg len 1/2
                statseglen_negseg_mean 1/2
                statseglen_negseg_median 1/2
            max len 1/2
                statseglen_negseg_max
        consec gain 1/3
            avg len 1/2
                statseglen_pseg_mean 1/2
                statseglen_pseg_median 1/2
            max len 1/2
                statseglen_pseg_max
        gain:loss 1/3
            psegnegsegratio_mean 1/2
            psegnegsegratio_median 1/2

"""

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
graphgrader_params = {
    'scriptname': 'manualreview_algographgrader',
    'scriptparams': [
        {
            'metricname': 'statseglen_bmin_mean',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': 'oldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmin_median',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': 'oldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmin_mean',
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'mean',
            'calibration': 'oldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmin_median',
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'median',
            'calibration': 'oldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmin_max',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'oldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmin_max',
            'rankascending': 1,
            'threshold': 0.3,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'oldbareminraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmax_mean',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2)*(1/2),
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': 'baremaxraw',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawoldbareminraw_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.50,
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2),
            'calibration': 'smoothraw',
            'stat_type': 'max',
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
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_pos_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'stat_type': 'mean',
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_pos_median',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'stat_type': 'median',
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_pos_max',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'stat_type': 'min',
            'metricweight': (1/6)*(1/3)*(1/2),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagratio_mean',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2),
            'stat_type': 'mean',
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagratio_median',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2),
            'stat_type': 'median',
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
            'metricweight': (1/6)*(1/3),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevalence_pos',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'metricweight': (1/6)*(1/3),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevratio',
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3),
            'calibration': 'raw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_mean',
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
            'mode': 'negative',
            'stat_type': 'max',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_pseg_mean',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
            'mode': 'positive',
            'stat_type': 'mean',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_pseg_median',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2)*(1/2),
            'mode': 'positive',
            'stat_type': 'median',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_pseg_max',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2),
            'mode': 'positive',
            'stat_type': 'max',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'psegnegsegratio_mean',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2),
            'stat_type': 'mean',
            'calibration': 'nonzeroraw',
            'look_back': 0
        },
        {
            'metricname': 'psegnegsegratio_median',
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3)*(1/2),
            'stat_type': 'median',
            'calibration': 'nonzeroraw',
            'look_back': 0
        }
        ]
    }
