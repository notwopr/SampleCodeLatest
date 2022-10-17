"""
Title: FILTER - first pass
Date Started: Mar 15, 2020
Version: 4
Version Start Date: Jan 2, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: All metrics.
Versions:
1.01: added smoothness_median, smoothness_mad, squeezefactor_median, and squeezefactor_mad
1.02: add dailystd, dailymad, nonzeromeandpc, nonzeromediandpc, meandpc, and mediandpc, dailynonzeromad
1.03: Remove excess smoothsqueeze functions after having revised them to be just simple ss area/total area.
2.00: Add age > 180 filter.
3.00: Removing all filters that exclude negatives.  The reason is I found this filter excluded KRMD (one of the best stocks over a period of the last 10 years) because its dailymad was zero.  this might have been overproscriptive.  I removed all other filters that are too proscriptive.
As a result I removed the following filters:
dailystd > 0
dailymad > 0
dpcmedianscore >= 0
dpcmeanscore > 0
nonzeromediandpc >=0
nonzeromeandpc > 0
3.1: After reviewing some unrelated rankings, I found a unisqueezefactor_median of 0 produced three stocks that had a virtually flat graph but weren't otherwise filtered out by v3.  So added here.  Also realizing that squeezearea is very strict and that 99% versus 100% is a negligible difference, I lowered the threshold to 50%.

Filters:
dailynonzerostd > 0 (dpc_cruncher)
dailynonzeromad > 0 (dpc_cruncher)
bmflatlinescore < 1
flatlinescore < 1
maxbmflatliferatio < 1
maxflatliferatio < 1
smootharea > 0 and < 1
squeezearea > 0 and < 0.50
age > 180
unisqueezefactor_median > 0  (unifatrawscore_baremaxrawoldbareminraw_median)
"""
from STRATTEST_FUNCBASE_RAW import dpc_cruncher_single, flatline_single, segliferatio_single, age_single
from STRATTEST_FUNCBASE_MMBM import fatarea_single, unifatshellraw_single

stage1_params = {
    'scriptname': 'STAGE1v3',
    'scriptparams': [
        {
            'metricname': 'dpc_cruncher_nonzero_std',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc_nonzero',
            'mode': 'std',
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_nonzero_mad',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc_nonzero',
            'mode': 'mad',
            'look_back': 0
        },
        {
            'metricname': 'flatlinescore_bmin',
            'metricfunc': flatline_single,
            'rankascending': 1,
            'threshold': 1,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'look_back': 0
        },
        {
            'metricname': 'flatlinescore_raw',
            'metricfunc': flatline_single,
            'rankascending': 1,
            'threshold': 1,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'seglife_flat_max',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 1,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'seglife_bmin_max',
            'metricfunc': segliferatio_single,
            'rankascending': 1,
            'threshold': 1,
            'thresholdtype': 'absolute',
            'filterdirection': 'below',
            'metricweight': 0,
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': ['oldbareminraw'],
            'data': 'bmindpc',
            'look_back': 0
        },
        {
            'metricname': 'area_smooth',
            'metricfunc': fatarea_single,
            'rankascending': 1,
            'lowerthreshold': 0,
            'upperthreshold': 1,
            'thresholdtype': 'absolute',
            'filterdirection': 'between',
            'metricweight': 0,
            'uppercol': 'rawprice',
            'lowercol': 'oldbareminraw',
            'datarangecol': 'rawprice',
            'calibration': ['oldbareminraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'area_squeeze',
            'metricfunc': fatarea_single,
            'rankascending': 1,
            'lowerthreshold': 0,
            'upperthreshold': 1,
            'thresholdtype': 'absolute',
            'filterdirection': 'between',
            'metricweight': 0,
            'uppercol': 'baremaxraw',
            'lowercol': 'oldbareminraw',
            'datarangecol': 'rawprice',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_baremaxrawoldbareminraw_median',
            'metricfunc': unifatshellraw_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'above',
            'metricweight': 0,
            'focuscol': 'baremaxraw',
            'idealcol': 'oldbareminraw',
            'stat_type': 'median',
            'calibration': ['oldbareminraw', 'baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'age_older',
            'metricfunc': age_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 180,
            'filterdirection': 'above',
            'metricweight': 0,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
