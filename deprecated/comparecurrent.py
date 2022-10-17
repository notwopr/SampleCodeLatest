def allmetricval_cruncher(datasourcetype, scriptname, scriptparams, beg_date, end_date, tickerlist, rankmeth, rankregime, chunksize):
    nonwinratemetrics_to_run = scriptparams
    # load marketbeater benchmarkdf if metric chosen
    benchmatrixchangesdf = ''
    # run metricsval multiprocessor
    if scriptname == 'recoverybotv9':
        mpfunc = recoverybotshell_old_single
    elif scriptname.startswith('recoverybot'):
        mpfunc = recoverybotshell_single
    else:
        mpfunc = lookbackshell_single
    # run multiprocessor
    table_results = multiprocessorshell_mapasync_getresults(mpfunc, tickerlist, 'no', (datasourcetype, nonwinratemetrics_to_run, benchmatrixchangesdf, beg_date, end_date), chunksize)
    masterdf = pd.DataFrame(data=table_results)
    # RANK DATA
    sumcols = []
    weight_total = 0
    for metricitem in scriptparams:
        # DEFINE RANK PARAMS
        metricweight = metricitem['metricweight']
        metcolname = getmetcolname(metricitem)
        # RANK METRIC DATA COLUMN
        rankcolname = f'RANK_{metcolname} (w={metricweight})'
        subjectcolname = metcolname
        # SET METRIC COLUMN RANK DIRECTION
        rankdirection = metricitem['rankascending']
        if rankmeth == 'minmax':
            masterdf[rankcolname] = mmcalibrated(masterdf[subjectcolname].to_numpy(), rankdirection, rankregime)
        elif rankmeth == 'standard':
            masterdf[rankcolname] = masterdf[subjectcolname].rank(ascending=rankdirection)
        # GET EACH RANKCOLUMN'S WEIGHTED RANK VALUE
        wrankcolname = f'w_{rankcolname}'
        masterdf[wrankcolname] = (masterdf[rankcolname] * metricweight)
        # KEEP TRACK OF THE WEIGHTED RANK COLUMN TO SUM LATER
        sumcols.append(wrankcolname)
        # ADD WEIGHT TO WEIGHT TOTAL
        weight_total += metricweight
    # sum weighted rankcols
    masterwrankcolname = f'MASTER WEIGHTED RANK {weight_total}'
    masterdf[masterwrankcolname] = masterdf[sumcols].sum(axis=1, min_count=len(sumcols))
    # rank overall weighted rankcol
    if rankmeth == 'minmax':
        if rankregime == '1isbest':
            finalrankascend = 0
        elif rankregime == '0isbest':
            finalrankascend = 1
    elif rankmeth == 'standard':
        finalrankascend = 1
    finalrankcolname = f'MASTER FINAL RANK as of {end_date}'
    masterdf[finalrankcolname] = masterdf[masterwrankcolname].rank(ascending=finalrankascend)
    # RE-SORT AND RE-INDEX
    masterdf.sort_values(ascending=True, by=[finalrankcolname], inplace=True)
    masterdf.reset_index(drop=True, inplace=True)
    return masterdf
