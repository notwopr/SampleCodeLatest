# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.symbology.symbology import Symbology
# from newbacktest.class_abstract_dbitem import AbstractDatabaseItem


class SampCode: #(AbstractDatabaseItem):
    # _item_term = "Sample Code"
    # #
    # # def __init__(self, stratcode, ipcode, invest_startdate):
    # #     '''
    # #     portsize = portfolio size
    # #     periodlen = duration in days of an investment period of the portfolio
    # #     batchstart = the rank number from the stratpool from which to derive your portfolio.  E.g. batchstart = 0 and portsize = 5, means portfolio would be comprised of ranks 0 thru 4 of a given stratpool.
    # #     numperiods = number of contiguous investment periods to invest in.  Optional.
    # #     '''
    # #     self._stratcode = stratcode
    # #     self._ipcode = ipcode
    # #     self._invest_startdate = invest_startdate
    # #     self._itemcode = self._set_itemcode()
    # #     self._creationdate = self._set_creationdate()
    #
    # @property
    # def ipcode(self):
    #     return self._ipcode
    #
    # @property
    # def stratcode(self):
    #     return self._stratcode
    #
    # @property
    # def invest_startdate(self):
    #     return self._invest_startdate

    def decode(self, sampcode):
        stratipcode = sampcode[:-11]
        invest_startdate = sampcode[-10:]
        ipcodestartindex = sampcode.find(Symbology().ipcode_pred)
        ipcode = sampcode[ipcodestartindex:-11]
        stratcode = sampcode[len(Symbology().sampcode_pred):ipcodestartindex-1]
        return {
            'stratcode': stratcode,
            'ipcode': ipcode,
            'invest_startdate': invest_startdate,
            'stratipcode': stratipcode
        }

    def generate(self, stratcode, ipcode, invest_startdate):
        sampcode = f'{Symbology().sampcode_pred}{stratcode}.{ipcode}.{invest_startdate}'
        print(f"Sample Code set to '{sampcode}'.")
        return sampcode
