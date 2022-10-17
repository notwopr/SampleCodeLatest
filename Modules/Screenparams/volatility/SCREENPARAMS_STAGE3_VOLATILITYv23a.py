"""
Title: SCREENPARAMS - STAGE 3 - VOLATILITY
Date Started: Jan 7, 2021
Version: 23.00a
Version Start Date: Oct 29, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Versions:
23a: change bigjump strength.

REVIEW.  IT DIDN'T REALLY MAKE ANYTHING BETTER.  POSNEGMAG ALONE IS MORE EFFECTIVE OF A METRIC THAN TRYING TO COMBINE MAGNITUDE AND PREVALENCE.  THEREFORE, V23 SHOULD NOT BE USED. V24 (WHICH IS THE ORIGINAL SMOOTHNESS SCRIPT TAKEN FROM GROPLUSVOLV15D) IS STILL SUPPERIOR.

Description:
BIGJUMP 1/6
    bigjumpoldbareminrawscore
NEGDPC 1/6
    posnegmagprevscore
MAXDROP 1/6
    allpctdrop_rawbaremaxraw_max
BMAXFLATSEG 1/6
    bmaxflatseglen_max
DROP STATS 1/6
    drop_score (dropprevalence * dropmag)
FATTINESS 1/6
    unifatscore_rawbaremaxraw_avg 1/2
    unifatscore_rawbaremaxraw_dev 1/2
DROPSCORE TO BENCHMARK RATIO
    dropscoreratio_single (no weight, just for information)
"""
from STRATTEST_FUNCBASE_MMBM import dropscore_single, unifatshell_single, bigjumpscore_single, allpctdrops_single, dropscoreratio_single
from STRATTEST_FUNCBASE_RAW import posnegmagprevscore_single, statseglen_single

bmaxflatsegweight = 1/6
maxdropweight = 1/6
bigjumpscore_weight = 1/6
dropscore_weight = 1/6
posnegmagprev_negweight = 1/6
unifatscoreweight = (1/6) * 1/2
unifatscoredevweight = (1/6) * 1/2

stage3_params = {
    'scriptname': 'VOLATILITYv23a',
    'scriptparams': [
        {
            'metricname': 'dropscoreratio_avg',
            'metricfunc': dropscoreratio_single,
            'rankascending': 1,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 0,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'benchticker': '^IXIC',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'statseglen_bmaxflat_max',
            'metricfunc': statseglen_single,
            'rankascending': 1,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': bmaxflatsegweight,
            'mode': 'flat',
            'stat_type': 'max',
            'calibration': ['baremaxraw'],
            'data': 'bmaxdpc',
            'look_back': 0
        },
        {
            'metricname': 'allpctdrop_rawbaremaxraw_max',
            'metricfunc': allpctdrops_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': -0.70,
            'filterdirection': 'no',
            'metricweight': maxdropweight,
            'calibration': ['baremaxraw'],
            'data': '',
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'min',
            'look_back': 0
        },
        {
            'metricname': 'bigjumpscore_oldbareminraw',
            'metricfunc': bigjumpscore_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': bigjumpscore_weight,
            'bigjumpstrength': 1.5,
            'calibration': ['oldbareminraw'],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawbaremaxraw_avg',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoreweight,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'unifatscore_rawbaremaxraw_dev',
            'metricfunc': unifatshell_single,
            'rankascending': 1,
            'threshold': 0.10,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': unifatscoredevweight,
            'focuscol': 'rawprice',
            'idealcol': 'baremaxraw',
            'stat_type': 'dev',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'posnegmagprevscore_neg_avg',
            'metricfunc': posnegmagprevscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'changetype': 'neg',
            'stat_type': 'avg',
            'metricweight': posnegmagprev_negweight,
            'calibration': [],
            'data': 'dpc',
            'look_back': 0
        },
        {
            'metricname': 'drop_score',
            'metricfunc': dropscore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': dropscore_weight,
            'uppercol': 'baremaxraw',
            'lowercol': 'rawprice',
            'stat_type': 'avg',
            'calibration': ['baremaxraw'],
            'data': '',
            'look_back': 0
        }
        ]
        }
