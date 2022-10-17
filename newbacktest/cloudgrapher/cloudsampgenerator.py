from newbacktest.symbology.sampcode import SampCode
from newbacktest.dategenerator import DateGenerator
from newbacktest.symbology.cloudsampcode import CloudSampCode
from newbacktest.cloudgrapher.db_cloudsample import CloudSampleDatabase
from newbacktest.cloudgrapher.class_cloudsample import CloudSample
from newbacktest.portfolios.portfoliogenerator import PortfolioGenerator
from newbacktest.symbology.investplancode import InvestPlanCode
from newbacktest.strategies.strategygenerator import StrategyGenerator


class CloudSampleGenerator:
    '''takes parameters for a strategy and investplan number of trials you want to run, and it returns and adds portfoliodfs composed of the resulting tickers and their eodprices for the prescribed investment period length for each trial.
    '''
    def generate_single_cloudsample(self, stratcode, ipcode, num_periods, cloudsamp_startdate):
        '''generate cloudsampcode'''
        cloudsampcode = CloudSampCode().generate(stratcode, ipcode, num_periods, cloudsamp_startdate)
        print(f'Checking if cloudsampcode "{cloudsampcode}" exists in the Cloud Sample Database...', end='')
        if CloudSampleDatabase().view_item(cloudsampcode):
            print('it does.\nMoving on to the next trial...\n\n')
            return
        print(f'it does not.\nGenerating a portfoliodf for all {num_periods} periods in cloud sample {cloudsampcode}, consisting of stratcode "{stratcode}", ipcode "{ipcode}" beginning with the period starting on "{cloudsamp_startdate}"...')
        '''get all startdates for all periods in cloud sample'''
        allinvest_startdates = DateGenerator().getevenlyspaced_dates(num_periods, InvestPlanCode().decode(ipcode)['periodlen'], cloudsamp_startdate)
        cloudsampledata = {}
        for j, invest_startdate in enumerate(allinvest_startdates):
            print(f'Period {j}: Invest Start Date: {invest_startdate}\n')
            '''generate portfoliodf'''
            PortfolioGenerator().generate_single(stratcode, ipcode, invest_startdate)
            '''add cloudsampcode to cloudsample itemdata dict'''
            cloudsampledata.update({j: SampCode().generate(stratcode, ipcode, invest_startdate)})
        '''create cloudsample object'''
        cso = CloudSample(cloudsampledata, cloudsampcode)
        '''add cloudsample to database'''
        CloudSampleDatabase().add_item(cso)

    def generate(self, strategydict, periodlen, portsize, batchstart, num_trials, num_periods, earliest_date='1971-02-05', latest_date=''):
        '''
        Note: default earliest date is '1971-02-05'.  The reason for that is that of all the available data, the bench indice data are all younger than the oldest stock data available.  So we wont be able to get metrics comparing the two for dates before the earliest index date.  So setting the earliest invest_startdate to NASDAQ IPO would ensure that we will have data to compare bench to stock because NASDAQ is the youngest of the 3 benchmarks. If our datasource changes and the previous facts no longer apply, we need to revisit whether we should set a different earliest_date or remove it altogether.
        '''
        stratcode = StrategyGenerator().generate(strategydict).itemcode
        ipcode = InvestPlanCode().generate(portsize, periodlen, batchstart)
        self.generate_bycode(stratcode, ipcode, num_trials, num_periods, earliest_date, latest_date)

    def generate_bycode(self, stratcode, ipcode, num_trials, num_periods, earliest_date='1971-02-05', latest_date=''):
        periodlen = InvestPlanCode().decode(ipcode)['periodlen']
        alltrialstartdates = DateGenerator().get_alltrialstartdates(num_trials, num_periods, periodlen, earliest_date, latest_date)
        '''run trials'''
        print(f"Running {num_trials} trials, each trial generating a cloud sample.  The following are the cloud sample start dates:\n {alltrialstartdates}")
        for i, cloudsamp_startdate in enumerate(alltrialstartdates):
            print(f'Trial {i}: Cloud Sample Start Date: {cloudsamp_startdate}\n')
            self.generate_single_cloudsample(stratcode, ipcode, num_periods, cloudsamp_startdate)
            print('Moving on to the next trial...\n\n')
        print('All cloud sample trials complete.')
