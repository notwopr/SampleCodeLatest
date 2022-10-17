# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.abstractclasses.class_abstract_dbitem import AbstractDatabaseItem


class WLPool(AbstractDatabaseItem):
    '''
    self._itemdata = dataframe of winners/losers including the metricvals used in the corresponding WLProfile filtering stage.
    ...
    }
    '''
    _item_term = "WLPool"

    def __init__(self, wlprofcode, invest_startdate, invest_enddate, periodlen, wlpooldf):
        self._itemdata = wlpooldf
        self._periodlen = periodlen
        self._itemcode = wlprofcode
        self._invest_startdate = invest_startdate
        self._invest_enddate = invest_enddate
        self._creationdate = self._set_creationdate()

    @property
    def invest_startdate(self):
        return self._invest_startdate

    @property
    def invest_enddate(self):
        return self._invest_enddate

    @property
    def periodlen(self):
        return self._periodlen
