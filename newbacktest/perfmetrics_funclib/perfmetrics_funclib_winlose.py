# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS
from newbacktest.portfolios.db_portfolio import PortfolioDatabase
from newbacktest.perfmetrics.winnerloser.db_wlpool import WinLosePoolDatabase
from newbacktest.perfmetrics.winnerloser.db_wlprofile import WinLoseProfDatabase
from newbacktest.symbology.sampcode import SampCode
from newbacktest.symbology.investplancode import InvestPlanCode


def winlose_accuracy(wlprofcode, sampcode):
    '''returns the proportion that a sample portfolio (sampcode) contained winners or losers according to provided criteria (wlprofcode).
    Note: this metric is only relevant if the periodlen for both sampcode and the winloseprofile underlying the wlprofcode match'''
    # check periodlen match
    sampobj = SampCode().decode(sampcode)
    invest_startdate = sampobj['invest_startdate']
    samp_periodlen = InvestPlanCode().decode(sampobj['ipcode'])['periodlen']
    if samp_periodlen != WinLoseProfDatabase().view_item(wlprofcode).periodlen:
        return np.nan

    portdf = PortfolioDatabase().view_item(sampcode)
    if type(portdf) == int:
        return 0

    portfolio = [c for c in portdf.columns if c != 'date']
    if len(portfolio) == 0:
        return 0
    else:
        wlpool = WinLosePoolDatabase().view_wlpool(wlprofcode, invest_startdate).itemdata['stock'].tolist()
        hits = set(wlpool).intersection(set(portfolio))
        return len(hits) / len(portfolio)
