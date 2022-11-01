from newbacktest.ingredients.db_metricfunction import MetricFunctionDatabase
from Modules.comparator import Comparator


class IngredientSettingsDatabase:
    '''
    The contents of this database must be hard coded and should not be programmatically generated.  Nothing should be removed from this database.  Only added to.
    '''
    _igsdb_source = [
        ('metricfunc', '0a', 'string', 'choices', 'metricfuncdetails'),
        # function objects arent stored but instead string identifier links to the metric function database which contains instructions to find the actual function object.
        ('sourcedata', '0b', 'string', 'choices', ['eodprices', 'marketcap', 'fundies']),
        ('look_back', '0c', 'integer', 'range', [['>=', 0]]),
        # integer. how many rows from present backwards in time, of the time-series source data do you want to consider when applying the metric function on it. Entering a zero means include everything.  A look_back of 1 means one day into the past, so it would result in 2 rows returned (1 for the present day, and 1 for yesterday).
        ('curvetype', '0d', 'string', 'choices', ['raw', 'true', 'straight', 'baremin', 'baremax', 'ppc_raw', 'ppc_true', 'ppc_baremin', 'ppc_baremax', 'ppc_raw_abs', 'ppc_raw_nonzero', 'ppc_raw_>0', 'ppc_raw_<0', 'ppc_raw_<=0', 'ppc_true_nonzero', 'ppc_baremin_nonzero', 'ppc_baremax_nonzero', 'ppc_raw_abs_nonzero']),
        # 'ppc' = period percent change. E.g. is daily percent change.  Given time-series data, ppc data representing the percent change from one row to the next. 'abs' = absolute value. All negative data points are converted to positive ones.
        # nonzero means only nonzero ppc datapoints are included. '>0' means only include positives. '<=0' means do not include positives.
        ('nantreatment', '0e', 'string', 'choices', ['removeall', 'ffillandremove']),
        # 'removeall' removes all nans in a series no matter where in the series. 'ffillandremove' fills in gaps by forward fill, but removes any and all leading nans.
        ('weight', '2a', 'number', 'range', [['>=', 0], ['<=', 1]]),
        ('rankdirection', '2b', 'string', 'choices', ['a', 'd']),
        ('ranktype', '2c', 'string', 'choices', ['ordinal', 'percentile']),
        # 100th percentile is best.
        ('filterby', 'f1', 'string', 'choices', ['value', 'rank']),
        ('threshold_value', 'f2', 'str_or_num', None, None),
        ('threshold_buffer', 'f3', 'number', None, None),
        ('threshold_type', 'f4', 'string', 'choices', ['byticker', 'bybestbench', 'byvalue']),
        ('threshold_bybestbench_better', 'f5', 'string', 'choices', ['bigger', 'smaller']),
        ('filterdirection', 'f6', 'string', 'choices', ['nofilter', '>', '>=', '<', '<=', '><', '><=', '>=<', '>=<=', '!=', '==']),
        ('focuscol', 'c1', 'string', 'choices', ['raw', 'true', 'straight', 'baremin', 'baremax']),
        ('idealcol', 'c2', 'string', 'choices', ['raw', 'true', 'straight', 'baremin', 'baremax']),
        ('uppercol', 'c3', 'string', 'choices', ['raw', 'true', 'straight', 'baremin', 'baremax']),
        ('lowercol', 'c4', 'string', 'choices', ['raw', 'true', 'straight', 'baremin', 'baremax']),
        ('stat_type', 'm1', 'string', 'choices', ['mean', 'median', 'avg', 'std', 'mad', 'dev', 'prev', 'min', 'max', 'sum', '1q', '3q']),
        ('ath_occur', 'rb1', 'string', 'choices', ['first', 'last']),
        # ath_occur designates how to calculate the preATH period.  'first' means take the date where the first ATH occur if there are several occurrences of the ATH price.  'last' means take the last occurrence.
        ('min_preath_age', 'rb2', 'integer', 'range', [['>=', 0]]),
        ('valtype', 'm0', 'string', 'choices', ['min', 'max', 'first', 'last']),
        ('occurtype', 'm1', 'string', 'choices', ['first', 'last']),
        ('compmode', 'm2', 'string', 'choices', ['first', 'last']),
        ('firstval', 'm3', 'string', 'choices', ['min', 'max', 'first', 'last']),
        ('secondval', 'm4', 'string', 'choices', ['min', 'max', 'first', 'last']),
        ('seglenmode', 'm5', 'string', 'choices', ['flat', 'positive', 'negative']),
        ('changetype', 'm6', 'string', 'choices', ['pos', 'neg']),
        ('accret_type', 'm7', 'string', 'choices', ['pos', 'neg', 'zero']),
        ('benchticker', 'm8', 'string', 'choices', ['^DJI', '^INX', '^IXIC']),
    ]

    def __init__(self):
        self.__igsdb = {
            t[0]: {
                'id': t[1],
                'vtype': t[2],
                'vlimit_type': t[3],
                'vlimit_details': t[4]
            }
            for t in self._igsdb_source
        }

    # list of required settings for any valid ingredient
    @property
    def required(self):
        return {k for k, v in self.igsdb.items() if v['id'].startswith('0')}

    @property
    def igsdb(self):
        return self.__igsdb

    # checks validity of an individual ingredient setting
    def is_value_valid(self, ingredient_setting_type, value):
        limit_type = self.igsdb[ingredient_setting_type]['vlimit_type']
        limit_details = self.igsdb[ingredient_setting_type]['vlimit_details']
        if limit_details == 'metricfuncdetails':
            limit_details = MetricFunctionDatabase().view_database().keys()
        if limit_type == "choices" and value not in limit_details:
            raise ValueError(f"The value {value} set for the ingredient setting {ingredient_setting_type} is not a permissible value. It must be one of the following: {limit_details}")
        elif limit_type == "range":
            for bound in limit_details:
                bound_type = bound[0]
                bound_value = bound[1]
                if not Comparator().is_valid(value, bound_value, bound_type):
                    raise ValueError(f"The value {value} set for the ingredient setting '{ingredient_setting_type}' is not a permissible value. It must be {bound_type} {bound_value}")
