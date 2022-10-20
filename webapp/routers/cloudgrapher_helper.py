"""
Title: Cloud Grapher Bot Helper
Date Started: Oct 19, 2022
Version: 1.00
Version Start: Oct 19, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  .

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS
from newbacktest.cloudgrapher.cloudgrapher_data import CloudGrapherData
from newbacktest.symbology.cloudsampcode import CloudSampCode
from newbacktest.datasource import DataSource
from newbacktest.dataframe_operations import DataFrameOperations
from newbacktest.growthcalculator import GrowthCalculator
from newbacktest.symbology.investplancode import InvestPlanCode


def gen_clouddf_single(idcodesuffix, misc, stake, benchmarks, csc_id, cloudsampcode):
    idcode = csc_id[cloudsampcode]
    df = CloudGrapherData().gen_cloudgraph_singlesample(cloudsampcode)
    portcols = [i for i in df.columns if i not in ['date', 'Days Invested', 'portcurve']]

    '''benchmark options'''
    if benchmarks:
        bdf = DataSource().opends('eodprices_bench')
        bdf.ffill(inplace=True)
        bdf = DataFrameOperations().filter_column(bdf, ['date']+benchmarks)
        df = df.join(bdf.set_index('date'), how='left', on="date")
        GrowthCalculator().getnormpricesdf(df, benchmarks)

    '''stake calculations'''
    cso = CloudSampCode().decode(cloudsampcode)
    portsize = InvestPlanCode().decode(cso['ipcode'])['portsize']
    periodlen = InvestPlanCode().decode(cso['ipcode'])['periodlen']
    num_periods = cso['num_periods']
    if stake:
        nonportfoliocurves = ['portcurve'] + benchmarks
        df[nonportfoliocurves] = stake * (1 + df[nonportfoliocurves])
        for p in range(num_periods):
            periodcols = [i for i in df.columns if i.endswith(str(p))]
            periodstake = df['portcurve'].iloc[p * periodlen]
            df[periodcols] = (periodstake / portsize) * (1 + df[periodcols])
    else:
        allcurves = portcols + ['portcurve'] + benchmarks
        df[allcurves] = df[allcurves] * 100

    '''misc options'''
    if misc:
        allcurves = portcols + ['portcurve'] + benchmarks
        if 'pco' in misc:
            df = df[[i for i in df.columns if i not in portcols]]
            allcurves = ['portcurve'] + benchmarks
        if 'epo' in misc:
            df.loc[~df['Days Invested'].isin([i*periodlen for i in range(num_periods+1)]), allcurves] = np.nan

    '''add idcode to every column in cloudsampcode df'''
    df.rename(columns={k: f"{idcode}{idcodesuffix}{k}" for k in [i for i in df.columns if i != 'Days Invested']}, inplace=True)
    df.set_index('Days Invested', inplace=True)
    return df


def aggregate_sipcols(aggmode, groupby, mdf, idcodesuffix, sicprefix, sic_id, coltype, stratipcode):
    sipcols = [n for n in mdf.columns if (n.endswith(coltype) and int(n[:n.find(idcodesuffix)]) in sic_id[stratipcode])]
    if len(sipcols) > 1:
        if aggmode == 'mean':
            mdf[f"{aggmode}_{coltype}_{sicprefix}"] = mdf[sipcols].mean(axis=1)
        if aggmode == 'median':
            mdf[f"{aggmode}_{coltype}_{sicprefix}"] = mdf[sipcols].median(axis=1)
        if 'std' in groupby:
            mdf[f"upper_std_{coltype}_{sicprefix}"] = mdf[f"{aggmode}_{coltype}_{sicprefix}"] + mdf[sipcols].std(axis=1)
            mdf[f"lower_std_{coltype}_{sicprefix}"] = mdf[f"{aggmode}_{coltype}_{sicprefix}"] - mdf[sipcols].std(axis=1)
