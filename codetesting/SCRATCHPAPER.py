from pricehistorybot import grabsinglehistory, grabsinglehistory_fundies
from fillgapbot import fill_gaps2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import numpy as np
import math
from pathlib import Path
import seaborn as sns
import datetime as dt
from STRATTEST_FUNCBASE_RAW import globalpricegrab_single, getpricedate_single, slopescorefocus_single
from STRATTEST_FUNCBASE_MMBM import smoothsqueezeshell, dropscore_single
from STRATTEST_FUNCBASE import allpctchanges, priceslicer
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher
from filelocations import readpkl, savetopkl
from growthcalcbot import period_growth_portfolio_fulldf, period_growth_portfolio
from STRATTEST_FUNCBASE_PERFORMANCE import mktbeatpoolstats, mktbeatpooldf, benchplusportfolioprices
from QUICKREFERENCE_BASE import stockrankerdf
from computersettings import computerobject
from statresearchbot import stat_profiler
#from Screenparams.SCREENPARAMS_STAGE3_LOSSCONTROLv1 import stage3_params
import importlib
from timeperiodbot import alldatewithtestlen, dipdates
from growthcalcbot import replaceleadzeros, getnormpricesdf, getportgrowthrate, getportfoliopricecol, getportfoliopricesdf
from STRATTEST_FUNCBASE_MMBM import allpctdrops_single
from correlationresearch import twolistcorr
from SCRATCHPAPER_GRAPHING import graphtopbottom, graphdataframe_setdatecolasindex
from genericfunctionbot import scriptjoiner, mmcalibrated
from tickerportalbot import tickerportal3, tickerportal4, tickerportal5
from computersettings import computerobject
#from Screenparams.SCREENPARAMS_STAGE3_WINRATERANKERv19 import stage3_params
from genericfunctionbot import graphbestfitformula, getprojectedyval
from STRATTEST_SINGLE_BASE_CRUNCHER_ALLMETRICVALS import getbenchmatrixchangedf
from STRATTEST_FUNCBASE_SMOOTHNESS import accretionscore_single, accretiontally_single
from UPDATEPRICEDATA_TIINGO import getindexofavailablefundamentals, fundamentalretrieval, marketcapretrieval, stockpriceretrieval, gettickerswithavailablefundamentals
from UPDATEPRICEDATA_FILELOCATIONS import PRICES, STOCKPRICES, tickerlistall_source, FUNDIES, daterangedb_source_fundies, daterangedb_source, tickerlistcommon_source
from UPDATEPRICEDATA_BASE import store_allmarketcap, store_allfundies, download_fundamentals
from UPDATEPRICEDATA_BASE_DATERANGES import create_daterangedb
from STRATTEST_FUNCBASE_FUNDAMENTALS import currmarketcap_single, fundypositiveslope_single
import dateutil.parser as dup
s = PRICES / 'allpricematrix_common'
print(s)
'''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# GET PRICE HISTORIES OF EACH
stock = 'HCTI'
s1hist = grabsinglehistory(stock)
s1hist = s1hist[s1hist['date'] <= dt.date.fromisoformat('2016-10-29')]
#print(s1hist)
print(getpricedate_single(s1hist, stock, 'first'))
print(globalpricegrab_single(s1hist, stock, 'first'))
print(getpricedate_single(s1hist, stock, 'min'))
print(globalpricegrab_single(s1hist, stock, 'min'))
#print(slopescorefocus_single(s1hist, stock))
#graphdataframe_setdatecolasindex(s1hist)
exit()



runsetdir = computerobject.bot_dump / 'multitrialsnew' / 'D20210423T8'/ 'finalpooltrialrunsetdump'
runsetdatalist = readpkl('finalpool_trial10', runsetdir)
print(len(runsetdatalist['startpool']))
datadf = fundamentalretrieval('UA', '1962-02-01', '2021-04-11', 'no', 'true')
print(datadf)
#datadf = grabsinglehistory_fundies('TSLA', 'fundies')
#print(datadf)

testdict = {
    'Stage 2 Part I': 13,
    #'Stage 2 Part II': 23,
    'Stage 3 Part III': 1,
    'test1': 3
}
print(testdict)
stage2keys = []
for keyname in testdict.keys():
    if keyname.startswith('Stage 2'):
        stage2keys.append(keyname)
for keyname in stage2keys:
    del testdict[keyname]
print(testdict)
teststr = 'I'
teststr += 'I'
counter = 'I'
for iterable in ['s2p', 's2', 's3']:
    print(counter)
    counter += 'I'


stock = 'ADBE'

prices = grabsinglehistory(stock)
prices = fill_gaps2(prices, '', '')
prices.reset_index(drop=True, inplace=True)

#datadf = marketcapretrieval('AACQ', '1962-02-01', '2021-03-03')
datadf = grabsinglehistory_fundies(stock, 'marketcap')
for dfobj in [datadf]:
    #dfobj['date'] = dfobj['date'].apply(dup.parse)
    #dfobj['date'] = dfobj['date'].apply(dt.datetime.date)
    dfobj = fill_gaps2(dfobj, '', '')
    dfobj.reset_index(drop=True, inplace=True)
    prices = prices.join(dfobj.set_index('date'), how="left", on="date")
sns.lineplot(data=prices[[stock]])
ax2 = plt.twinx()
sns.lineplot(data=prices[[f'marketcap_{stock}']], ax=ax2)
#sns.lineplot(data=prices[[f'revenue_{stock}', f'freecashflow_{stock}']], ax=ax2)
plt.show()
stagescript = {
    'test1': 1,
    'test2': 3,
    #'datasourcetype': 4
}
if 'datasourcetype' in stagescript.keys():
    print(stagescript.keys())
    print('yes')


#gettickerswithavailablefundamentals(computerobject.bot_dump)
stock = 'ADBE'

prices = grabsinglehistory(stock)
prices = fill_gaps2(prices, '', '')
prices.reset_index(drop=True, inplace=True)

#datadf = marketcapretrieval('AACQ', '1962-02-01', '2021-03-03')
datadf = fundamentalretrieval(stock, '1962-02-01', '2021-03-11', 'no', 'true')
datadf_false = fundamentalretrieval(stock, '1962-02-01', '2021-03-11', 'no', 'false')
datadf_false.rename(columns={f'revenue_{stock}': f'revenue_{stock}_false', f'freecashflow_{stock}': f'freecashflow_{stock}_false'}, inplace=True)
for dfobj in [datadf, datadf_false]:
    dfobj['date'] = dfobj['date'].apply(dup.parse)
    dfobj['date'] = dfobj['date'].apply(dt.datetime.date)
    dfobj = fill_gaps2(dfobj, '', '')
    dfobj.reset_index(drop=True, inplace=True)
    prices = prices.join(dfobj.set_index('date'), how="left", on="date")

print(prices)
sns.lineplot(data=prices[[stock]])
ax2 = plt.twinx()
sns.lineplot(data=prices[[f'revenue_{stock}', f'freecashflow_{stock}', f'revenue_{stock}_false', f'freecashflow_{stock}_false']], ax=ax2)
plt.show()

#download_fundamentals('', '1962-02-01', '2021-03-04', 'STOR')
datadf = readpkl('SCOR_fundies', FUNDIES)
#print(datadf)
stock = 'SCOR'
prices = grabsinglehistory(stock)
prices = fill_gaps2(prices, '', '2021-03-01')
prices.reset_index(drop=True, inplace=True)
#print(prices)
#fundypositiveslope_single(prices, stock, 'revenue')

existdate = '2003-01-01'
print(len(tickerportal4(daterangedb_source, tickerlistcommon_source, existdate, existdate, 'common', 2)))
print(len(tickerportal5(daterangedb_source, tickerlistcommon_source, daterangedb_source_fundies, existdate, existdate, 'common', 2)))


stock = 'ADBE'
prices = grabsinglehistory(stock)
prices = fill_gaps2(prices, '2015-01-01', '2017-01-01')
prices.reset_index(drop=True, inplace=True)
print(prices)
fundypositiveslope_single(prices, stock, 'revenue')

fundydump = computerobject.bot_dump / 'testfundies'
marketcapsourcedata = fundydump / 'sourcedata'
marketcapdatedump = fundydump / 'datedump'
marketcapdateresults = fundydump / 'dateresults'
datadf = readpkl('AAPL_fundies', marketcapsourcedata)
print(datadf)
datadf = fill_gaps2(datadf, '', '2021-03-03')
datadf.reset_index(drop=True, inplace=True)
print(datadf)

chunksize = 5
if __name__ == '__main__':
    #store_allfundies(marketcapsourcedata, tickerlistall_source, chunksize)
    create_daterangedb(marketcapdatedump, tickerlistall_source, marketcapsourcedata, marketcapdateresults, 'daterangedb_name_fundies', 'fundies', chunksize)

print(readpkl('AA_prices', STOCKPRICES))


accretionscore2_single
stock = 'ADBE'
prices = grabsinglehistory(stock)
prices = fill_gaps2(prices, '', '')
prices.reset_index(drop=True, inplace=True)

print(prices)
print(accretionscore_single(prices, stock), accretionscore2_single(prices, stock))
staticdatesource = r'D:\BOT_DUMP\strattest_singles\D20210205T1\Stage1_parent\nonwinratemetricvals_as_of_2021-01-29.csv'
sourcedf = pd.read_csv(staticdatesource)
# for each column get min and max vals
# get stats
nonmetricolnames = ['stock']
metricolnames = [item for item in list(sourcedf.columns) if item not in nonmetricolnames]
masteroverallstatdata = []
for category in metricolnames:
    minval = np.min(sourcedf[category].dropna().to_numpy())
    maxval = np.max(sourcedf[category].dropna().to_numpy())
    statdict = {'category': category, 'min': minval, 'max': maxval}
    masteroverallstatdata.append(statdict)
# save final df
masteroverallstats = pd.DataFrame(data=masteroverallstatdata)
masteroverallstats.to_csv(index=False, path_or_buf=computerobject.bot_dump / "masteroverallstats.csv")

tradedates = getalltradedays('KO')
prices = grabsinglehistory('KO')
prices = fill_gaps2(prices, '', '')
prices.reset_index(drop=True, inplace=True)
print(prices)
# remove row if date is a holiday
prices = prices[prices['date'].isin(tradedates)].copy()
print(prices)

staticdatesource = r'D:\BOT_DUMP\strattest_singles\D20210102T6\Stage2_parent\Stage2_summer2020vM_multithresh_24_finalists_as_of_2020-01-01.csv'
stocklistdf = pd.read_csv(staticdatesource)
portfolio = stocklistdf['stock'].tolist()
beg_date = ''
end_date = '2020-01-01'
metrifunc = unifatshell_single

for stock in portfolio:
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, '2020-01-01')
    prices.reset_index(drop=True, inplace=True)
    #prices = priceslicer(prices, 360)
    metricfuncinputs = (prices, idealcol, focuscol, stat_type)
    print(stock, metrifunc(*metricfuncinputs))
    #sns.lineplot(data=prices)
    #plt.show()

def convertpricearr(origarr, convert_type):
    if convert_type == 'oldbareminraw':
        newarr = oldbaremin_cruncher(origarr)
    elif convert_type == 'baremaxraw':
        newarr = baremax_cruncher(origarr)
    elif convert_type == 'trueline':
        oldbareminrawpricearr = np.array(oldbaremin_cruncher(origarr))
        baremaxrawpricearr = np.array(baremax_cruncher(origarr))
        newarr = ((baremaxrawpricearr - oldbareminrawpricearr) / 2) + oldbareminrawpricearr
    elif convert_type == 'straight':
        origarr = origarr.array
        age = len(origarr) - 1
        price_start = origarr[0]
        price_end = origarr[-1]
        slope = (price_end - price_start) / age
        newarr = [(slope * x) + price_start for x in range(age + 1)]
    elif convert_type == 'rawprice':
        newarr = origarr
    return newarr


# return array of all drop values
def alldropshell(pricecol, uppercol, lowercol):
    # assign upper and lower arrays
    upperarr = convertpricearr(pricecol, uppercol)
    lowerarr = convertpricearr(pricecol, lowercol)
    pctdrops = (lowerarr - upperarr) / upperarr
    nonzerodrops = pctdrops[pctdrops < 0]
    return nonzerodrops


# calculates drop prevalence
def dropprev(pricecol, uppercol, lowercol):
    nonzerodrops = alldropshell(pricecol, uppercol, lowercol)
    dropprevalence = len(nonzerodrops) / len(pricecol)
    return dropprevalence


# calc magnitude of drops
def dropmag(pricecol, uppercol, lowercol, stat_type):
    nonzerodrops = alldropshell(pricecol, uppercol, lowercol)
    if stat_type == 'mean':
        dropmag = np.mean(nonzerodrops)
    elif stat_type == 'median':
        dropmag = np.median(nonzerodrops)
    elif stat_type == 'avg':
        dropmag = np.mean([np.mean(nonzerodrops), np.median(nonzerodrops)])
    return dropmag


portfolio = ['AAPL','ADSK', 'PYPL']
benchticker = '^IXIC'
beg_date = '2017-02-03'
end_date = '2018-02-03'
sliced = benchplusportfolioprices(portfolio, benchticker, beg_date, end_date)
print(sliced)
dropprevresults = sliced.iloc[:, 1:].apply(lambda x: dropprev(x, 'baremaxraw', 'rawprice'))
dropmagresults = sliced.iloc[:, 1:].apply(lambda x: dropmag(x, 'baremaxraw', 'rawprice', 'mean'))
print(dropprevresults)
print(dropmagresults)
print(dropprevresults*dropmagresults)

for stock in portfolio:
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)
    prices.reset_index(drop=True, inplace=True)
    # add cols
    allprices = prices[stock].tolist()
    oldbareminrawpricelist = oldbaremin_cruncher(allprices)
    prices['oldbareminraw'] = np.array(oldbareminrawpricelist)
    baremaxrawpricelist = baremax_cruncher(allprices)
    prices['baremaxraw'] = np.array(baremaxrawpricelist)
    prices['trueline'] = ((prices['baremaxraw'] - prices['oldbareminraw']) / 2) + prices['oldbareminraw']
    price_start = prices.iloc[0][stock]
    price_end = prices.iloc[-1][stock]
    age = len(prices) - 1
    slope = (price_end - price_start) / age
    prices['straight'] = [(slope * x) + price_start for x in range(age + 1)]
    dropprevsingle = dropprevalence_single(prices, 'baremaxraw', stock)
    dropmagsingle = allpctdrops_single(prices, 'baremaxraw', stock, 'mean')
    print(stock, dropprevsingle, dropmagsingle)
    graphtopbottom(prices, prices, 'date', 'date', [stock, 'baremaxraw'], ['pctdrops'], [2, 1], True, True)

print(getbenchmatrixchangedf(['^DJI', '^IXIC']))

timechunksignal = 0.70
if (buytrigger == "+" and timechunksignal == buytrigger) or (buytrigger != "+" and timechunksignal > buytrigger):
    print("buy")

y_data = [603, 33, 174]
x_data = [-0.008148238221, -0.002557338456, -0.004198786508]
print(getprojectedyval(-0.002941992511, x_data, y_data, 1))
graphbestfitformula(-0.01, 0.01, 0.001, x_data, y_data, 1)

bweights = {
    '^IXIC': 1,
    '^INX': 0,
    '^DJI': 0
}
print(list(bweights.values()))

# load price matrices into RAM
pricematrixdf = readpkl('allpricematrix_common', PRICES)
print(pricematrixdf)


existdate = '2000-01-04'
existpool = tickerportal3(daterangedb_source, tickerlistcommon_source, existdate, 'common', 2)[:5]
end_date = str(dt.date.fromisoformat(existdate) + dt.timedelta(days=365))
getidealslist_single(pricematrixdf, existpool, existdate, end_date, 0.10, ideal_profile)


staticdatesource = r'D:\BOT_DUMP\multitrials\D20201010T3\mktbeatpoolpctalltrialmasterdf_2018methodversions.csv'
stocklistdf = pd.read_csv(staticdatesource)
statictrialexistdates = stocklistdf['existdate'].to_list()
alltrialresults = []
for trial in enumerate(statictrialexistdates):
    trialno = trial[0]
    existdate = trial[1]
    trialfolder = f'\\trialno{trialno}_edate{existdate}'
    trialpath = trialfolder + global_params['subtrialfolderpath']
    fullbasepoolpath = global_params['testrunparentpath'] + trialpath
    basepoolfilename = global_params['basepoolfntemplate'] + existdate
    basepooldf = readpkl(basepoolfilename, Path(fullbasepoolpath))
    startpool = basepooldf['stock'].tolist()
    fixedtrialiterables = {
        'trialno': trialno,
        'existdate': existdate,
        'startpool': startpool
    }
    alltrialresults.append(fixedtrialiterables)
print(alltrialresults)
savetopkl('D20201010T3multitrialset', computerobject.bot_dump, alltrialresults)


print(stage3_params)
sourcetype = 'trueline'
stat_type = 'mad'
rankmeth = 'minmax_nan'
winlen_ceiling = 5
# update scriptname
stage3_params.update({
    'scriptname': f'winrateranker_{sourcetype}_{stat_type}_{rankmeth}_winlenceil{winlen_ceiling}'
})
# update scriptparams
stage3_params['scriptparams'][0].update({
    'metricname': f'winrateranker_{sourcetype}_{stat_type}_{rankmeth}_winlenceil{winlen_ceiling}',
    'stat_type': stat_type,
    'winlen_ceiling': winlen_ceiling,
    'rankmeth': rankmeth
})
# update rawvalrankdirection
if stat_type in ['std', 'mad', 'dev']:
    stage3_params['scriptparams'][0].update({
        'rawvalrankdirection': 1
    })
elif stat_type in ['mean', 'median', 'avg']:
    stage3_params['scriptparams'][0].update({
        'rawvalrankdirection': 0
    })

print(stage3_params)


sourcefolder =
fullsourceloc = sourcefolder
basepoolmasterprefix = r'D:\BOT_DUMP\multitrials\D20201110T5\alltrialsummaries_maxddchangepct.csv'
resultdf = pd.read_csv(fullsourceloc)
print(resultdf)

arr1 = np.array([1,2,1,np.nan,3,42,41,2,2])
print(1-arr1)


tickerportal3(daterangedb_source, tickerlistcommon_source, '1999-07-16', 'common', 2)

stock = '^IXIC'
beg_date = '1999-01-26'
end_date = '2000-01-26'
prices = grabsinglehistory(stock)
prices = fill_gaps2(prices, beg_date, end_date)
# graph
# get trueline
allprices = prices[stock].tolist()
oldbareminrawpricelist = oldbaremin_cruncher(allprices)
prices['lowestprice'] = np.array(oldbareminrawpricelist)
baremaxrawpricelist = baremax_cruncher(allprices)
prices['baremaxraw'] = np.array(baremaxrawpricelist)
prices['pctdrops'] = (prices['lowestprice'] - prices[stock]) / prices[stock]
# graph
graphtopbottom(prices, prices, 'date', 'date', [stock, 'lowestprice'], ['pctdrops'], [2, 1], True, True)
print(dipdates(prices, stock))



list1 = resultdf['maxddchangepct'].tolist()
list2 = resultdf['benchperf'].tolist()
print(twolistcorr(list1, list2, 'pearson'))

print(allpctdrops_single(prices, stock, 'oldbareminraw', stock, 'max'))

#pricematrixdf = readpkl('allpricematrix_common', PRICES)
beg_date = '2019-12-24'
end_date = '2020-01-10'
portfolio = ['PYPL']
#avgmeth = 'avg'
#portname = 'scratchtestport'
#pricedf = getportfoliopricesdf(pricematrixdf, portfolio, beg_date, end_date)
#normdf = getnormpricesdf(pricedf, portfolio)
#portprices = getportfoliopricecol(normdf, portfolio, avgmeth)
#portprices.rename(columns={f'portfolioprices_{avgmeth}': f'{portname}'}, inplace=True)
allprices = portprices[portname].tolist()
oldbareminrawpricelist = oldbaremin_cruncher(allprices)
portprices['oldbareminraw'] = np.array(oldbareminrawpricelist)
baremaxrawpricelist = baremax_cruncher(allprices)
portprices['baremaxraw'] = np.array(baremaxrawpricelist)
portprices['trueline'] = ((portprices['baremaxraw'] - portprices['oldbareminraw']) / 2) + portprices['oldbareminraw']

print(portprices)
exit()

iterparamname = 'Screenparams.SCREENPARAMS_STAGE3_LOSSCONTROLv1'
itermodule = importlib.import_module(iterparamname)
iterparams = itermodule.stage3_params
print(iterparams)

STOCKLISTS = computerobject.bot_important / 'stocklists'
GRAPHGRADEPARENT = STOCKLISTS / 'graphgrades'
CURRENT_SL = GRAPHGRADEPARENT / 'CURRENT'
gradesheet = readpkl('2015fallcandidates_2015-10-09', CURRENT_SL)
gradesheet.to_csv(index=False, path_or_buf=computerobject.bot_dump / 'gradesheet.csv')

# get projected daily percentage change


baremaxrawpricelist = baremax_cruncher(allprices)
prices['baremaxraw'] = np.array(baremaxrawpricelist)
prices['trueline'] = ((prices['baremaxraw'] - prices['oldbareminraw']) / 2) + prices['oldbareminraw']
prices['alldrops'] = (prices['oldbareminraw'] - prices[stock]) / prices[stock]
# calc drop stats
alldropsarr = prices['alldrops'].to_numpy()
allzerodropsarr = alldropsarr[alldropsarr < 0]
statdict = stat_profiler(allzerodropsarr)

# add std cushion
statdict.update({
    'stat_mean-1.5std': statdict['stat_mean'] - (statdict['stat_std'] * 1.5),
    'stat_mean+1.5std': statdict['stat_mean'] + (statdict['stat_std'] * 1.5),
})
# remove std, sharpe
del statdict['stat_std']
del statdict['stat_sharpe']
#createdf
dfdata = {'nonzerodrops': allzerodropsarr}
dfdata.update(statdict)
dropdf = pd.DataFrame(data=dfdata)

# graph
ax1 = plt.subplot(1, 2, 1)
sns.lineplot(data=prices[[stock, 'baremaxraw', 'oldbareminraw']])

plt.subplot(1, 2, 2)
sns.lineplot(data=dropdf)
plt.show()

reg1pct_single(prices, stock)



#reg1reg2ratio(prices, stock, 'baremaxraw', 'oldbareminraw', 'mean')

statanswer = getreg1stats_single(prices, stock, 'max')
print(statanswer)

pd.set_option("display.max_rows", None, "display.max_columns", None)
#print(prices)
prices['pctchanges'] = prices[stock].pct_change(periods=1, fill_method='ffill')
print(prices)
print(getallseglens(prices['pctchanges'].dropna().tolist(), 'positive'))
print(statseglen_single(prices['pctchanges'].dropna().tolist(), 'positive', 'mean'))

pricematrixdf = readpkl('allpricematrix_common', PRICES)

portfolio = ['PLMR', 'TEAM', 'KNSL', 'CDW']
package = [portfolio, [beg_date, end_date]]
print(period_growth_portfolio_fulldf('mean', 'no', 1.5, '', '', pricematrixdf, package))
print(period_growth_portfolio('mean', 'no', 1.5, '', '', pricematrixdf, package))

#print(kneescore_single(prices, stock))
#print(fatshell_single(prices, 'straight', stock))
prices['trueline'] = ((prices['baremaxraw'] - prices['oldbareminraw']) / 2) + prices['oldbareminraw']
unismoothsqueeze_single(prices, 'baremaxraw', 'oldbareminraw')





unisqueezefactor = prices['squeezeline'].sum() / (len(prices) - 1)
prices[[stock, 'squeezeline']].plot()
ax1 = plt.subplot(1, 2, 1)
plt.plot(prices[[stock, 'baremaxraw', 'oldbareminraw']])
plt.subplot(1, 2, 2, sharex=ax1)
plt.plot(prices[['squeezeline']])


#trialno = 99
#exist_date = '2019-06-20'
basepoolmasterprefix = r'D:\BOT_DUMP\summer2020tempvL6\D20200909T12\mktbeatpoolpctalltrialstats_metricset_summer2020vL7.csv'
#trialfolder = f'\\trialno{trialno}_edate{exist_date}'
#filelocsuffix = trialfolder + r'\Stage 1_dump\resultfiles'
#basepooldirstr = basepoolmasterprefix + filelocsuffix
#basepoolfileloc = Path(basepooldirstr)
#print(basepoolfileloc)
basepoolfilenametemplate = 'mktbeatpoolpctalltrialstats_metricset_summer2020vL7'
#basepoolfilename = basepoolfilenametemplate + exist_date
#basepooldf = readpkl(basepoolfilename, basepoolfileloc)
resultdf = pd.read_csv(basepoolmasterprefix)
avg_perf = resultdf[resultdf['category'] == 'mktfailmarginperf']['stat_mean'].item()
print(avg_perf)
'''
