from newbacktest.baking.baker_stratpool import Baker
from newbacktest.stratpools.db_stratpool import StratPoolDatabase
from newbacktest.portfolios.db_portfolio import PortfolioDatabase
from newbacktest.symbology.sampcode import SampCode
from newbacktest.symbology.investplancode import InvestPlanCode
from newbacktest.dategenerator import DateGenerator
from newbacktest.strategies.strategygenerator import StrategyGenerator


class PortfolioGenerator:
    '''takes parameters for a strategy and investplan number of trials you want to run, and it returns and adds portfoliodfs composed of the resulting tickers and their eodprices for the prescribed investment period length for each trial.
    '''

    def generate_single(self, stratcode, ipcode, invest_startdate):
        '''check if sampcode exists'''
        sampcode = SampCode().generate(stratcode, ipcode, invest_startdate)
        print(f'Checking if sampcode "{sampcode}" exists in the Portfolio Database...', end='')
        if PortfolioDatabase().view_item(sampcode):
            print('it does.\nMoving on to the next trial...\n\n')
            return

        '''check if stratpooldf exists for stratcode+datecombo'''
        scobj = SampCode().decode(sampcode)
        stratcode = scobj['stratcode']
        invest_startdate = scobj['invest_startdate']
        print(f'it does not.\nChecking if a Stratpooldf exists for stratcode "{stratcode}" plus invest_startdate "{invest_startdate}"...', end='')
        if StratPoolDatabase().view_stratpool(stratcode, invest_startdate):
            print('it does.  Generating portfoliodf...')
            '''generate portfoliodf'''
            PortfolioDatabase().add_item(sampcode)
        else:
            '''bake strategy (convert to stratpooldf and store) given date'''
            print('it does not. Generating stratpooldf...')
            Baker()._bake_strategy(stratcode, invest_startdate)
            print(StratPoolDatabase())
            print(StratPoolDatabase().view_stratpool(stratcode, invest_startdate).itemdata)

            '''generate and save portfoliodf'''
            print('Generating Portfoliodf...')
            '''create and store portfoliodf'''
            PortfolioDatabase().add_item(sampcode)
            print(PortfolioDatabase().view_item(sampcode))

    def generate(self, strategydict, num_trials, periodlen, portsize, batchstart, earliest_date='1971-02-05', latest_date=''):
        '''
        Note: default earliest date is '1971-02-05'.  The reason for that is that of all the available data, the bench indice data are all younger than the oldest stock data available.  So we wont be able to get metrics comparing the two for dates before the earliest index date.  So setting the earliest invest_startdate to NASDAQ IPO would ensure that we will have data to compare bench to stock because NASDAQ is the youngest of the 3 benchmarks. If our datasource changes and the previous facts no longer apply, we need to revisit whether we should set a different earliest_date or remove it altogether.
        '''
        '''system gets N randomized invest_startdate'''
        allinvest_startdates = DateGenerator().getrandomexistdate_multiple(num_trials, periodlen, earliest_date, latest_date)
        print(allinvest_startdates)

        stratcode = StrategyGenerator().generate(strategydict).itemcode
        ipcode = InvestPlanCode().generate(portsize, periodlen, batchstart)

        '''run trials'''
        for i, invest_startdate in enumerate(allinvest_startdates):
            print(f'Trial No: {i}: {invest_startdate}\n')
            self.generate_single(stratcode, ipcode, invest_startdate)
            print('Moving on to the next trial...\n\n')
        print('All trials complete.')
        return allinvest_startdates
