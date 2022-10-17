# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.symbology.symbology import Symbology
# from newbacktest.class_abstract_dbitem import AbstractDatabaseItem
from type_checking import TypeChecker


class InvestPlanCode:
    # _item_term = "Investment Plan"

    # def __init__(self, portsize, periodlen, batchstart, numperiods=1):
    #     '''
    #     portsize = portfolio size
    #     periodlen = duration in days of an investment period of the portfolio
    #     batchstart = the rank number from the stratpool from which to derive your portfolio.  E.g. batchstart = 0 and portsize = 5, means portfolio would be comprised of ranks 0 thru 4 of a given stratpool.
    #     numperiods = number of contiguous investment periods to invest in.  Optional.
    #     '''
        # self._portsize = portsize
        # self._periodlen = periodlen
        # self._batchstart = batchstart
        # self._numperiods = numperiods
        # self._itemcode = self._set_itemcode()
        # self._creationdate = self._set_creationdate()

    # @property
    # def portsize(self):
    #     return self._portsize
    #
    # @property
    # def periodlen(self):
    #     return self._periodlen
    #
    # @property
    # def batchstart(self):
    #     return self._batchstart
    #
    # @property
    # def numperiods(self):
    #     return self._numperiods
    #
    # def _set_itemtype(self, itemdata):
    #     pass

    def generate(self, portsize, periodlen, batchstart):
        for inputobj in [portsize, periodlen, batchstart]:
            TypeChecker().is_valid(inputobj, 'integer')
        ipcode = f'{Symbology().ipcode_pred}{portsize}.{periodlen}.{batchstart}'
        print(f"Investment Plan code set to {ipcode}.")
        return ipcode

    def decode(self, ipcode):
        answer = {
            'portsize': None,
            'periodlen': None,
            'batchstart': None
        }
        trackerkey = ['prefix', 'portsize', 'periodlen', 'batchstart']
        substr = ipcode
        for tkey in trackerkey:
            hit = substr.find('.')
            if hit == -1:
                answer[tkey] = int(substr)
                break
            if tkey != 'prefix':
                answer[tkey] = int(substr[:hit])
            substr = substr[hit+1:]
        return answer
