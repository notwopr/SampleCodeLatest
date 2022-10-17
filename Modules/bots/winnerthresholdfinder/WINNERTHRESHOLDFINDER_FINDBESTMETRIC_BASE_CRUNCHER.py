"""
Title: WINNER THRESHOLD FINDER BASE - BEST METRIC
Date Started: Feb 7, 2021
Version: 1.00
Version Start: Feb 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Gets losers and winners for each trial.  For each metric requested, find min and max values for that trial for both loser and winner groups.  If neither group ranges overlap, go to next trial.  If the two groups never overlap for all trials requested, then record metricname with each of its trial's records. Go to next metric in list.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from tickerportalbot import tickerportal3
from UPDATEPRICEDATA_FILELOCATIONS import daterangedb_source, tickerlistcommon_source
from WINNERTHRESHOLDFINDER_BASE_GETWINNERSLOSERS import getnormprices, winnerloserdefiner
from filelocations import readpkl, savetopkl, buildfolders_singlechild
from WINNERTHRESHOLDFINDER_BASE_GETMETRICVALS import getallwinnermetricvals_single


# get winners/loser for each trial
def getwinnerloserpools_singletrial(winnerpoolsdir, pricematrixdf, benchpricematrixdf, benchticker, testlen, winnerdefined, loserdefined, minimumage, trial):
    trialno = trial[0]
    exist_date = trial[1]
    # get testperiod
    test_beg = exist_date
    test_end = str(dt.date.fromisoformat(exist_date) + dt.timedelta(days=testlen))
    # get existing stocks
    startpool = tickerportal3(exist_date, 'common', minimumage)
    # get df of normalized bench and pool prices
    normpricesdf = getnormprices(pricematrixdf, benchpricematrixdf, startpool, benchticker, test_beg, test_end)
    # define winners
    winnerpool = winnerloserdefiner(startpool, winnerdefined, normpricesdf, benchticker, test_beg, test_end)
    # define losers
    loserpool = winnerloserdefiner(startpool, loserdefined, normpricesdf, benchticker, test_beg, test_end)
    trialdata = {
        'trialno': trialno,
        'exist_date': exist_date,
        'test_beg': test_beg,
        'test_end': test_end,
        'testlen': testlen,
        'winnerpool': winnerpool,
        'loserpool': loserpool
    }
    # save to file
    savetopkl(f'winnerloserpools_trial{trialno}', winnerpoolsdir, trialdata)


# evaluate whether loser winner group minmaxvals overlap for all trials requested
def metricfuncoverlaptester(metricitemdump, summarydfsavedir, metricitem, metcolname, alltrialexistdates, winnerloserpoolsdir, savemode, chunksize):
    allsummaries = []
    # for each trial, get minmax vals for winner and loser groups
    for trial in enumerate(alltrialexistdates):
        trialno = trial[0]
        exist_date = trial[1]
        # get winnerloser data file
        winnerloserdict = readpkl(f'winnerloserpools_trial{trialno}', winnerloserpoolsdir)
        # create trial summary object
        trialsummary = {'trialno': trialno, 'exist_date': exist_date, 'test_beg': winnerloserdict['test_beg'], 'test_end': winnerloserdict['test_end'], 'testlen': winnerloserdict['testlen'], 'metricname': metcolname}
        # create metval dump folder
        metvaldump = buildfolders_singlechild(metricitemdump, f'trialno{trialno}_edate{exist_date}')
        # get minmax vals for each group
        for groupname in ['winner', 'loser']:
            # get pool
            stockpool = winnerloserdict[f'{groupname}pool']
            # create folder for group metval dump
            groupmetvaldump = buildfolders_singlechild(metvaldump, f'metvaldump_{groupname}')
            # get group metvals df
            groupmetricvalsdf = getallwinnermetricvals_single(groupmetvaldump, '', [metricitem], '', exist_date, stockpool, '', '', savemode, chunksize)
            # get min and max val
            minval = groupmetricvalsdf[metcolname].min()
            maxval = groupmetricvalsdf[metcolname].max()
            # add vals to summary
            trialsummary.update({
                f'{groupname}_min': minval,
                f'{groupname}_max': maxval
                })
        # add summary to masterlist
        allsummaries.append(trialsummary)
        # check for overlap
        if trialsummary['loser_min'] >= trialsummary['winner_max'] or trialsummary['loser_max'] <= trialsummary['winner_min']:
            continue
        else:
            break
    # save trialsummary df regardless whether overlap occurs
    allsummariesdf = pd.DataFrame(data=allsummaries)
    allsummariesdf.to_csv(index=False, path_or_buf=summarydfsavedir / f"{metcolname}_alltrialsummaries.csv")
    return allsummariesdf
