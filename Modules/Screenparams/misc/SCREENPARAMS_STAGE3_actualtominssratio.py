"""
Title:  SCREEN PARAMS - ACTUAL TO MIN SLOPESCORE RATIO
Date Started: Apr 26, 2021
Version: 1.00
Version Start Date: Apr 26, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:

FILTERS:

'overallrate' is the amount in percent by which you'd like the stock to appreciate over a one year period.  enter 1 for 100% for example. In essence, its a growth rate factor.  so an overall rate of 1 means the set of overall appreciation equivalent to num_years * 100%.  So if overall rate = 1, then that implies an overall growth for a 2-year period of 200%, 3-yr (300%), etc.  an overall rate of .9, means 90% over 1yr, 180% over 2yrs, etc.
"""
from STRATTEST_FUNCBASE_RAW import slopescorefocus_single, minslopescore_single, actualtominssratio_single, dpctominssratio_single, dpc_cruncher_single

focuscol = 'rawprice'
overallrate = 1
# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
stage3_params = {
    'scriptname': f'STAGE3_slopescoreonly_{focuscol}',
    'scriptparams': [
        {
            'metricname': 'dpc_cruncher_mean',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc',
            'mode': 'mean',
            'look_back': 0
        },
        {
            'metricname': 'dpctominss_mean',
            'metricfunc': dpctominssratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc',
            'mode': 'mean',
            'overallrate': overallrate,
            'look_back': 0
        },
        {
            'metricname': 'dpc_cruncher_median',
            'metricfunc': dpc_cruncher_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc',
            'mode': 'median',
            'look_back': 0
        },
        {
            'metricname': 'dpctominss_median',
            'metricfunc': dpctominssratio_single,
            'rankascending': 0,
            'threshold': 0,
            'thresholdtype': 'absolute',
            'filterdirection': 'no',
            'metricweight': 0,
            'calibration': [],
            'data': 'dpc',
            'mode': 'median',
            'overallrate': overallrate,
            'look_back': 0
        },
        {
            'metricname': 'slopescore',
            'metricfunc': slopescorefocus_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 0,
            'focuscol': focuscol,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'minslopescore',
            'metricfunc': minslopescore_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 0,
            'filterdirection': 'no',
            'metricweight': 0,
            'overallrate': overallrate,
            'calibration': [],
            'data': '',
            'look_back': 0
        },
        {
            'metricname': 'actualtominssratio',
            'metricfunc': actualtominssratio_single,
            'rankascending': 0,
            'thresholdtype': 'absolute',
            'threshold': 1,
            'filterdirection': 'no',
            'metricweight': 1,
            'focuscol': focuscol,
            'overallrate': overallrate,
            'calibration': [],
            'data': '',
            'look_back': 0
        }
        ]
    }
