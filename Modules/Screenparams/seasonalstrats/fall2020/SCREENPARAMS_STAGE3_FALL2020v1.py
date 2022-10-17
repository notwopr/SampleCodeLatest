"""
Title: FALL 2020 STRAT - STAGE 3
Date Started: Aug 19, 2020
Version: 1
Version Start Date: Sept 29, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

DESCRIPTION:

    Growth Factor: 1/8
        slopescore

    Posnegmag Factor: 1/8
        posnegmag_neg	(1/2)
            posnegmag_neg_mean (1/2)
            posnegmag_neg_median (1/2)
        posnegmag_pos	(1/2)
            posnegmag_pos_mean (1/2)
            posnegmag_pos_median (1/2)

    Posnegprev Factor: 1/8
        posnegprevalence_neg	1/2
        posnegprevalence_pos	1/2

    Psegnegsegratio: 1/8

    avgpseglen: 1/8
        statseglen_pseg_median 1/2
        statseglen_pseg_mean 1/2
    avgnegseglen: 1/8
        statseglen_negseg_median 1/2
        statseglen_negseg_mean 1/2

    squeezearea 1/8
    unifatscore_baremaxrawoldbareminraw 1/8
        unifatscore_baremaxrawoldbareminraw_mean	1/2
        unifatscore_baremaxrawoldbareminraw_median 1/2

"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single, fatarea_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single, psegnegsegratio_single, statseglen_single, posnegmag_single, posnegprevalence_single

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'stage3_fall2020v1',
    'scriptparams': [
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8)*(1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mean',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_median',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8)*(1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'area_squeeze',
            'metricfunc': fatarea_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8),
            'uppercol': 'baremaxraw',
            'lowercol': 'oldbareminraw',
            'datarangecol': 'rawprice',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/8),
            'focuscol': 'rawprice',
            'calibration': [''],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'psegnegsegratio',
            'metricfunc': psegnegsegratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8),
            'stat_type': 'avg',
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_pseg_mean',
            'metricfunc': statseglen_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8)*(1/2),
            'mode': 'positive',
            'stat_type': 'mean',
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_pseg_median',
            'metricfunc': statseglen_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8)*(1/2),
            'mode': 'positive',
            'stat_type': 'median',
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_mean',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8)*(1/2),
            'mode': 'negative',
            'stat_type': 'mean',
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_negseg_median',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/8)*(1/2),
            'mode': 'negative',
            'stat_type': 'median',
            'calibration': [''],
            'data': 'dpc',
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
            'metricweight': (1/8)*(1/2)*(1/2),
            'calibration': [''],
            'data': 'dpc',
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
            'metricweight': (1/8)*(1/2)*(1/2),
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_pos_mean',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'stat_type': 'mean',
            'metricweight': (1/8)*(1/2)*(1/2),
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegmag_pos_median',
            'metricfunc': posnegmag_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'stat_type': 'median',
            'metricweight': (1/8)*(1/2)*(1/2),
            'calibration': [''],
            'data': 'dpc',
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
            'metricweight': (1/8)*(1/2),
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevalence_pos',
            'metricfunc': posnegprevalence_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'pos',
            'metricweight': (1/8)*(1/2),
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        }
        ]
    }
