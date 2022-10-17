"""
Title: SCREENPARAMS - STAGE 2 Part II - FALL 2020
Date Started: July 25, 2020
Version: 1B
Version Start Date: Oct 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

squeezearea	0.191
unismoothfactor_mean	0.39
unismoothfactor_median	0.33
unismoothfactor_std	0.45
unismoothfactor_mad	0.37
unisqueezefactor_mean	0.92
unisqueezefactor_median	1.2
unisqueezefactor_std	0.88
unisqueezefactor_mad	0.71

"""
from STRATTEST_FUNCBASE_MMBM import unifatshell_single, fatarea_single


# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage2part2_params = {
    'scriptname': 'stage2part2_fall2020v1B',
    'scriptparams': [
        {
            'metricname': 'squeezearea',
            'metricfunc': fatarea_single,
            'rankascending': 1,
            'threshold': 0.191,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'uppercol': 'baremaxraw',
            'lowercol': 'oldbareminraw',
            'datarangecol': 'rawprice',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.39,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mean',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_median',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.33,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_std',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.45,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'std',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawoldbareminraw_mad',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.37,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'focuscol': 'rawprice',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mad',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_mean',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.92,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
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
            'threshold': 1.2,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_std',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.88,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'std',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_mad',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.71,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'mad',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
    }
