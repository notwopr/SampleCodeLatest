"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Aug 19, 2020
Version: 12
Version Start Date: Sept 18, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
6: compares rawprice graph to trueline graph, then trueline graph to kneescore graph
7: compares rawprice graph to oldbareminraw graph, then oldbareminraw graph to kneescore graph
9: compares rawprice graph to oldbareminraw graph, then oldbareminraw graph to kneescore graph but on uniform scale

"""
flatw = 0.10                # weight of the flat metrics combined
squeezew = 0.50                # weight of the squeeze metrics combined
smoothw = 0.0                # weight of the smooth metrics combined
slopew = 0.0                   # weight of the slopescore metric
kneew = 0.3                 # weight of the bmknee metrics combined
sqarea = 0.1                # weight of squeezearea metric
kneemagw = 1.00              # weight of the bmknee mean/median metrics combined
kneedevw = 1 - kneemagw       # weight of the bmknee std/mad metrics combined
squeezemagw = 1.00             # weight of the squeeze mean/median metrics combined
squeezedevw = 1 - squeezemagw     # weight of the squeeze std/mad metrics combined
smoothmagw = 0.50             # weight of the smooth mean/median metrics combined
smoothdevw = 1 - smoothmagw     # weight of the smooth std/mad metrics combined
medmad = 0.00
meanstd = 1 - medmad

# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
fnlbatches = [
    {
        'batch': [
            {
                'metricname': 'maxbmaxflatseg',
                'rankascending': 1,
                'threshold': 210.1,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*flatw,
                'mode': 'flat',
                'stat_type': 'max',
                'calibration': 'baremaxraw',
                'look_back': 0
            },
            {
                'metricname': 'maxbmflatseg',
                'rankascending': 1,
                'threshold': 115.36,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': (1/2)*flatw,
                'mode': 'flat',
                'stat_type': 'max',
                'calibration': 'oldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor_mean',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': meanstd*squeezemagw*squeezew,
                'stat_type': 'mean',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor_median',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': medmad*squeezemagw*squeezew,
                'stat_type': 'median',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor_std',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': meanstd*squeezedevw*squeezew,
                'stat_type': 'std',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'unisqueezefactor_mad',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': medmad*squeezedevw*squeezew,
                'stat_type': 'mad',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'unismoothfactor_mean',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': meanstd*smoothmagw*smoothw,
                'stat_type': 'mean',
                'calibration': 'smoothraw',
                'look_back': 0
            },
            {
                'metricname': 'unismoothfactor_median',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': medmad*smoothmagw*smoothw,
                'stat_type': 'median',
                'calibration': 'smoothraw',
                'look_back': 0
            },
            {
                'metricname': 'unismoothfactor_std',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': meanstd*smoothdevw*smoothw,
                'stat_type': 'std',
                'calibration': 'smoothraw',
                'look_back': 0
            },
            {
                'metricname': 'unismoothfactor_mad',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': medmad*smoothdevw*smoothw,
                'stat_type': 'mad',
                'calibration': 'smoothraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight_mean',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': meanstd*kneemagw*kneew,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'mean',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight_median',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': medmad*kneemagw*kneew,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'median',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight_std',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': meanstd*kneedevw*kneew,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'std',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'unifatscore_oldbareminrawstraight_mad',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': medmad*kneedevw*kneew,
                'focuscol': 'oldbareminraw',
                'idealcol': 'straight',
                'stat_type': 'mad',
                'calibration': 'noprepoldbareminraw',
                'look_back': 0
            },
            {
                'metricname': 'squeezearea',
                'rankascending': 1,
                'threshold': 0.10,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': 0,
                'stat_type': 'area',
                'calibration': 'squeezeraw',
                'look_back': 0
            },
            {
                'metricname': 'slopescore',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': 1*slopew,
                'calibration': 'noprepraw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3v12'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
