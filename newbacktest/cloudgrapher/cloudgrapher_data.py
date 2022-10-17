# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from newbacktest.portfolios.db_portfolio import PortfolioDatabase
from newbacktest.growthcalculator import GrowthCalculator
from newbacktest.cloudgrapher.db_cloudsample import CloudSampleDatabase


class CloudGrapherData:

    def convert_to_clouddf(self, portfoliodf):
        portfolio = portfoliodf.columns[1:]
        GrowthCalculator().getnormpricesdf(portfoliodf, portfolio)

    def gen_cloudgraph_singleperiod(self, period, sampcode):
        portfoliodf = PortfolioDatabase().view_item(sampcode)
        portfoliodf.rename(columns={k: f"{k}_{period}" for k in portfoliodf.columns[1:]}, inplace=True)
        self.convert_to_clouddf(portfoliodf)
        return portfoliodf

    def gen_cloudgraph_singlesample(self, cloudsampcode):
        '''sample = if stratcode+ipcode consists of 20 periods of X days each, a single sample would be the entire 20 period stretch for that one stratcode+ipcode and given invest_startdate

        '''
        cso = CloudSampleDatabase().view_item(cloudsampcode).itemdata
        alldfs = []
        periodscalar = 1
        portcurve_periodchange = 0
        for period, sampcode in cso.items():
            portfoliodf = self.gen_cloudgraph_singleperiod(period, sampcode)
            portfolio = portfoliodf.columns[1:]
            portfoliodf[f'portcurve_{period}'] = portfoliodf[portfolio].mean(axis=1)
            portcurve_periodchange = portfoliodf[f'portcurve_{period}'].iloc[-1]
            portfoliodf[f'portcurve_{period}'] = periodscalar * (1 + portfoliodf[f'portcurve_{period}']) - 1
            periodscalar = periodscalar * (1 + portcurve_periodchange)
            '''See notes on periodscalar below'''
            portfoliodf.set_index('date', inplace=True)
            alldfs.append(portfoliodf)

        mdf = pd.concat(alldfs, ignore_index=False, axis=1)
        mdf.sort_values(by='date', inplace=True)
        mdf.reset_index(inplace=True)
        allportcurvecols = [i for i in mdf.columns if i.startswith('portcurve')]
        mdf = mdf.assign(portcurve=mdf[allportcurvecols].max(1)).drop(allportcurvecols, axis=1)
        mdf['Days Invested'] = mdf.index
        return mdf


'''
A note on periodscalar.
Each period portfoliodf is represented in normalized figures, meaning it shows the percent change in price from the beginning of that portfoliodf.
If we have several contiguous dfs of this kind, it is hard to calculate the cumulative effect.
To figure this out, we know that P * (1 + r) = the amount you have after 1 period.  We also know the amount you have after n periods is P * (1+r)^n.  However, for each period the "r" is different.
Each day or row in the df represents the percent change respect to the first row of that df.  So for the first period to get the percent change of P dollars on day x in the df, you simply take the rate found in that row (call it c), and do P * (1 + c).
How much will we have at the end of period 1?  Let's say day end_p1 in the df is the last day in the period 1 df, and its rate with respect to day 1 of the period is c_end_p1.  Then by the end of period 1 the amount we have is P * (1 + c_end_p1).
Now let's say there is a following adjacent period, period 2.  And day y is some y days from the beginning of period 2. How much money will we have by day y?
    Well, we need to know the amount we have at the end of period 1.  We also need to calculate how much that amount will change from the start of period 2 to day y.  We know the amount of change from day 1 of period 2 to day y is P * (1+c_y).  But here P is the amount we have at the end of period 1.
    Thus the amount we have at day y is P * (1 + c_end_p1) * (1+c_y).
What we want is to calculate what is the cumulative percent change for an arbitrary day x, where day x can be any day in a multi-period time span.
We know the formula for the total amount of money would be P * (1 + r_x), where P is the amount we have at the beginning of the period that day x is apart of.
So it'll be P * (1 + r_endp1) * (1 + r_endp2) * ... * (1 + r_x).  What we need is just the overall rate q such that it will give us the amount we will have by day x with respect to the beginning of the entire time span, so we can rewrite the problem as:
P * (1 + r_endp1) * (1 + r_endp2) * ... * (1 + r_x) = P * (1 + q)
solve for q.
 (1 + r_endp1) * (1 + r_endp2) * ... * (1 + r_x) = (1 + q)
  q = (1 + r_endp1) * (1 + r_endp2) * ... * (1 + r_x) - 1
  the last portfoliodf (the one containing day x) we know contains in its for for day x, the value r_x in its cell.
  So the periodscalar is simply the expression chunk before (1 + r_x) in the q expression above, or:
  periodscalar = (1 + r_endp1) * (1 + r_endp2) * ...
  Period 1's df is fine, there is no need to calibrate the percentchange values because its the first period.  But for any subsequent period df, we need to calibrate them to account for the cumulative changes that occurred before them.
  So q here represents the recalibrated value for a given day in a portfoliodf.
  What is the q for a day in period 2?  Let's say we have day x in period 2.
  new_x_rate = (1 + r_endp1) * (1 + orig_x_rate) - 1
  What about q for a day z in period m?
  new_z_rate = periodscalar * (1 + orig_z_rate) - 1
  so periodscalar for each subsequent period, grows via loop:
  period 2: (1 + r_endp1)
  period 3: (1 + r_endp1) * (1 + r_endp2)
  period 4: (1 + r_endp1) * (1 + r_endp2) * (1 + r_endp3)
  ...
  The "r_endp_" is represented in the code above as "portcurve_periodchange".
'''
