# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.ingredients.class_ingredient import Ingredient


class VolStatProfile:
    def __init__(self):
        self.volstatprofile = [[
            {
                'metricfunc': 'unifatshell_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'a',
                'focuscol': 'raw',
                'idealcol': 'baremax',
                'stat_type': 'avg',
            },
            {
                'metricfunc': 'unifatshell_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'a',
                'focuscol': 'baremin',
                'idealcol': 'baremax',
                'stat_type': 'avg',
            },
            {
                'metricfunc': 'allpctdrops_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'd',
                'lowercol': 'raw',
                'uppercol': 'baremax',
                'stat_type': 'avg'
            },
            {
                'metricfunc': 'allpctdrops_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'a',
                'lowercol': 'raw',
                'uppercol': 'baremax',
                'stat_type': 'prev'
            },
            {
                'metricfunc': 'dropscore_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'd',
                'lowercol': 'raw',
                'uppercol': 'baremax'
            },
            {
                'metricfunc': 'dropscoreratio_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'a',
                'lowercol': 'raw',
                'uppercol': 'baremax',
                'benchticker': '^DJI'
            },
            {
                'metricfunc': 'dropscoreratio_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'a',
                'lowercol': 'raw',
                'uppercol': 'baremax',
                'benchticker': '^INX'
            },
            {
                'metricfunc': 'dropscoreratio_single',
                'sourcedata': 'eodprices',
                'nantreatment': 'ffillandremove',
                'look_back': 0,
                'curvetype': 'raw',
                'weight': 1/8,
                'ranktype': 'percentile',
                'rankdirection': 'a',
                'lowercol': 'raw',
                'uppercol': 'baremax',
                'benchticker': '^IXIC'
            }
        ]]
        self.volstat_definitions = {
            'fatscore_baremaxtoraw': 'Fatscore is the average area per unit time between two line graphs A and B.  For every value on the x-axis (date), |A_x - B_x|/B_x is calculated, where A_x/B_x is the y-value at point x on graph A/B respectively.  Thus, the fatscore_AtoB equals the average of the set of {|A_x - B_x|/B_x for all x on the x-axis}.',
            'fatscore_baremaxtobaremin': 'Fatscore is the average area per unit time between two line graphs A and B.  For every value on the x-axis (date), |A_x - B_x|/B_x is calculated, where A_x|B_x is the y-value at point x on graph A|B respectively.  Thus, the fatscore_AtoB equals the average of the set of {|A_x - B_x|/B_x for all x on the x-axis}.',
            'drop_mag': 'Drop_mag measures how much the actual price is below the baremaxraw price on average, expressed as a proportion of the baremaxraw price.  This is calculated by averaging the set of all (actualprice_i - baremaxprice_i)/baremaxprice_i, where i is a point on the x-axis where that expression is nonzero.',
            'drop_prev': 'Drop_prev measures how often the actual price of a stock does not equal the baremaxraw price of the stock, expressed as a proportion of the entire date range in question.  A drop_prev of 0.70, for example, means the actual price of the stock is below the baremaxprice of the stock 70% of the time.',
            'dropscore': 'The dropscore is simply the drop_mag * drop_prev.  See drop_mag and drop_prev column headers for their respective meanings.',
            'dropscoreratio_Dow Jones': 'The dropscore ratio is the ratio of the dropscore of a given stock to a chosen benchmark.  For example, dropscoreratio_NASDAQ is the ratio of the dropscore of the stock in question to the dropscore of the NASDAQ.  Thus, a dropscoreratio of 1 means the stock does not dip below its own baremaxraw price anymore frequently and drastically than NASDAQ.  One could interpret this as one measure of how volatile the stock is as compared to the benchmark chosen.',
            'dropscoreratio_S&P 500': 'The dropscore ratio is the ratio of the dropscore of a given stock to a chosen benchmark.  For example, dropscoreratio_NASDAQ is the ratio of the dropscore of the stock in question to the dropscore of the NASDAQ.  Thus, a dropscoreratio of 1 means the stock does not dip below its own baremaxraw price anymore frequently and drastically than NASDAQ.  One could interpret this as one measure of how volatile the stock is as compared to the benchmark chosen.',
            'dropscoreratio_NASDAQ': 'The dropscore ratio is the ratio of the dropscore of a given stock to a chosen benchmark.  For example, dropscoreratio_NASDAQ is the ratio of the dropscore of the stock in question to the dropscore of the NASDAQ.  Thus, a dropscoreratio of 1 means the stock does not dip below its own baremaxraw price anymore frequently and drastically than NASDAQ.  One could interpret this as one measure of how volatile the stock is as compared to the benchmark chosen.'
            }
        self.indextonickname = {
            0: 'fatscore_baremaxtoraw',
            1: 'fatscore_baremaxtobaremin',
            2: 'drop_mag',
            3: 'drop_prev',
            4: 'dropscore',
            5: 'dropscoreratio_Dow Jones',
            6: 'dropscoreratio_S&P 500',
            7: 'dropscoreratio_NASDAQ'
            }
        self.ingredientobjects = {i: Ingredient(ingredient, self.indextonickname[i], self.volstat_definitions[self.indextonickname[i]]) for i, ingredient in enumerate(self.volstatprofile[0])}
        self.colnametonickname = {ig.colname: ig.nickname for ig in self.ingredientobjects.values()}
        self.igcodedict = {'eodprices': [ig.itemcode for ig in self.ingredientobjects.values()]}
