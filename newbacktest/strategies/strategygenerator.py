from newbacktest.strategies.class_strategy import Strategy
from newbacktest.strategies.db_strategycookbook import StrategyCookBook
from newbacktest.ingredients.db_metricfunction import MetricFunctionDatabase


class StrategyGenerator:
    '''takes parameters for a strategy, updates metricfunc database, creates strategyobject, adds object to strat database and returns the strat object.
    '''
    def generate(self, strategydict):
        '''make sure metricfunctiondatabase is up to date'''
        MetricFunctionDatabase().update_mfdb()
        '''create strategy you want to test'''
        strat = Strategy(strategydict)
        StrategyCookBook().add_item(strat)
        return strat
