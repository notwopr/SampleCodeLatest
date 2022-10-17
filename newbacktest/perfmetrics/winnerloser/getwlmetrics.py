# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.perfmetrics.winnerloser.winnerlosergenerator import WinLoseGenerator
from newbacktest.portfolios.portfoliogenerator import PortfolioGenerator


class GetWLMetrics:

    def get_wlperfmetrics(self, wlprofile, strategy, num_trials, periodlen, portsize, batchstart, earliest_date='', latest_date=''):
        '''given a strategy, invest plan, and wlprofile, generates win lose performance metrics for those strategy trials'''
        '''generate portfolios'''
        allinvest_startdates = PortfolioGenerator().generate(strategy, num_trials, periodlen, portsize, batchstart)
        '''add wlprofile and generate wlpools'''
        WinLoseGenerator().generate_bywlprofile(wlprofile, periodlen, allinvest_startdates)
