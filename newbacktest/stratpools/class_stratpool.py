# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.abstractclasses.class_abstract_dbitem import AbstractDatabaseItem
from type_checking import TypeChecker


class Stratpool(AbstractDatabaseItem):
    '''
    self._itemdata = dataframe of metricvals for all stocks for the given data, resulting for baking the given strategy.
    ...
    }
    '''
    _item_term = "Stratpool"

    def __init__(self, stratcode, invest_startdate, stratpooldf):
        self._itemdata = stratpooldf
        self._itemcode = self._set_itemcode(stratcode)
        self._invest_startdate = self._set_invest_startdate(invest_startdate)
        self._creationdate = self._set_creationdate()

    @property
    def invest_startdate(self):
        return self._invest_startdate

    def _set_itemcode(self, stratcode):
        '''
        the stratpool inherits the code assigned to the strategy that produced the stratpool.
        '''
        print(f"Stratpool code set to '{stratcode}'.")
        return stratcode

    def _set_invest_startdate(self, invest_startdate):
        '''
        The invest_startdate is the date in the hypothetical world in which the strategy was run and stratpool generated.  E.g. an invest_startdate of 2001-03-04 means the stratpool created is one that would have existed had you run this strategy on that date.
        '''
        TypeChecker().is_valid(invest_startdate, 'string')
        print(f"Invest Start Date set to '{invest_startdate}'.")
        return invest_startdate
