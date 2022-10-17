"""
Title: SUMMER 2020 TEMP STRAT - STAGE 3
Date Started: Aug 19, 2020
Version: 13
Version Start Date: Sept 24, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Modeled after optimalparamfinder second pass params.
Versions:
6: compares rawprice graph to trueline graph, then trueline graph to kneescore graph
7: compares rawprice graph to oldbareminraw graph, then oldbareminraw graph to kneescore graph
9: compares rawprice graph to oldbareminraw graph, then oldbareminraw graph to kneescore graph but on uniform scale

"""

squeezew = 1/7                # weight of the squeeze metrics combined
slopew = 0.0                   # weight of the slopescore metric
sqaw = 1/7                # weight of squeezearea metric
pnegsegw = 1/7        # posnegseg metrics
posnegmagw = 1/7      # posnegmag metrics
posnegprevw = 1/7     # posnegprev metrics
kneew = 1/7                # weight of the bmknee metrics combined
flatw = 1/7                # weight of the flat metrics combined
smoothw = 0.0                # weight of the smooth metrics combined
kneemagw = 1.00              # weight of the bmknee mean/median metrics combined
kneedevw = 1 - kneemagw       # weight of the bmknee std/mad metrics combined
squeezemagw = 1.00             # weight of the squeeze mean/median metrics combined
squeezedevw = 1 - squeezemagw     # weight of the squeeze std/mad metrics combined
smoothmagw = 0.50             # weight of the smooth mean/median metrics combined
smoothdevw = 1 - smoothmagw     # weight of the smooth std/mad metrics combined
medmad = 0.50                   # weight of mean std statistics versus median/mad equivalents
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
                'metricweight': sqaw,
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
            },
            {
                'metricname': 'psegnegsegratio',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': pnegsegw*(1/3),
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'avgpseglen',
                'rankascending': 0,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': pnegsegw*(1/3),
                'mode': 'positive',
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'avgnegseglen',
                'rankascending': 1,
                'threshold': 0,
                'thresholdtype': 'absolute',
                'filterdirection': 'no',
                'metricweight': pnegsegw*(1/3),
                'mode': 'negative',
                'stat_type': 'avg',
                'calibration': 'nonzeroraw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmag_neg',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'neg',
                'stat_type': 'avg',
                'metricweight': posnegmagw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmag_pos',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'changetype': 'pos',
                'stat_type': 'avg',
                'metricweight': posnegmagw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegmagratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'stat_type': 'avg',
                'metricweight': posnegmagw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            },
            {
                'metricname': 'posnegprevratio',
                'rankascending': 0,
                'thresholdtype': 'absolute',
                'threshold': 0,
                'filterdirection': 'no',
                'metricweight': posnegprevw*(1/3),
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
                'metricweight': posnegprevw*(1/3),
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
                'metricweight': posnegprevw*(1/3),
                'calibration': 'raw',
                'look_back': 0
            }
            ],
        'batchtype': 'layercake',
        'batchname': 'summer2020temp_stage3v13'
    }
]

# STORE
stage3_params = [{'method_specific_params': {'fnlbatches': fnlbatches}}]
