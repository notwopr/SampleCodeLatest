"""
Title: FALL 2020 METHOD - STAGE 3
Date Started: Aug 19, 2020
Version: 2
Version Start Date: Sept 24, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

DESCRIPTION:

    Growth Factor: 1/6
        slopescore 1

    Posnegmag Factor: 1/6
        posnegmag_neg	1/3
            posnegmag_neg_mean 1/2
            posnegmag_neg_median 1/2
        posnegmag_pos	1/3
            posnegmag_pos_mean 1/2
            posnegmag_pos_median 1/2
        posnegmagratio  1/3

    Posnegprev Factor: 1/6
        posnegprevratio         1/3
        posnegprevalence_neg	1/3
        posnegprevalence_pos	1/3

    posnegseg Factor: 1/6
        Psegnegsegratio: 1/3
        avgpseglen: 1/3
            statseglen_pseg_median 1/2
            statseglen_pseg_mean 1/2
        avgnegseglen: 1/3
            statseglen_negseg_median 1/2
            statseglen_negseg_mean 1/2

    Squeezefactor 1/6
        unisqueezefactor (unifatscore_baremaxrawoldbareminraw_) 1/2
            unisqueezefactor_mean 1/2
            unisqueezefactor_median 1/2
            unisqueezefactor_std 0
            unisqueezefactor_mad 0
        squeezearea 1/2

    Difference between true graph and straight line 1/6
        Magnitude of that difference 1/2
            unifatscore_oldbareminrawstraight_mean 1/2
            unifatscore_oldbareminrawstraight_median 1/2
        Regularity of that difference 1/2
            unifatscore_oldbareminrawstraight_std 1/2
            unifatscore_oldbareminrawstraight_mad 1/2

"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single, fatarea_single
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single, psegnegsegratio_single, statseglen_single, posnegmag_single, posnegprevalence_single, posnegprevratio_single, posnegmagratio_single
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': 'stage3_fall2020v2',
    'scriptparams': [
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
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
            'metricweight': (1/6)*(1/2)*(1/2),
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'mean',
            'calibration': ['oldbareminraw', 'straight'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_median',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'median',
            'calibration': ['oldbareminraw', 'straight'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_std',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'std',
            'calibration': ['oldbareminraw', 'straight'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_oldbareminrawstraight_mad',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2)*(1/2),
            'focuscol': 'oldbareminraw',
            'idealcol': 'straight',
            'stat_type': 'mad',
            'calibration': ['oldbareminraw', 'straight'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'squeezearea',
            'metricfunc': fatarea_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/2),
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
            'metricweight': (1/6),
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
            'metricweight': (1/6)*(1/3),
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
            'metricweight': (1/6)*(1/3)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
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
            'metricweight': (1/6)*(1/3)*(1/2),
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagratio',
            'metricfunc': posnegmagratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'stat_type': 'avg',
            'metricweight': (1/6)*(1/3),
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'posnegprevratio',
            'metricfunc': posnegprevratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': (1/6)*(1/3),
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
            'metricweight': (1/6)*(1/3),
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
            'metricweight': (1/6)*(1/3),
            'calibration': [''],
            'data': 'dpc',
            'look_back': 0
        }
        ]
    }
