# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from abc import ABC
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from Modules.datetime_functions import TimeStamp


class AbstractDatabaseItem(ABC):
    '''
    An abstract class for an object that is an item to be added to a database.
    '''
    @property
    def creationdate(self):
        return self._creationdate

    def _set_creationdate(self):
        creationdate = TimeStamp()
        print(f"{self._item_term} creation date set to '{creationdate.dtobject}'.")
        return creationdate

    @property
    def nickname(self):
        return self._nickname

    def _set_nickname(self, nickname):
        self._nickname = nickname
        print(f"{self._item_term} nickname set to '{self.nickname}'.")

    @property
    def description(self):
        return self._description

    def _set_description(self, description):
        self._description = description
        print(f"{self._item_term} description set to '{self.description}'.")

    @property
    def itemdata(self):
        return self._itemdata

    @property
    def itemcode(self):
        return self._itemcode

    def _set_itemcode(self, itemcode):
        self._itemcode = itemcode
        print(f"{self._item_term} item code set to '{self.itemcode}'.")

    @property
    def itemtype(self):
        return self._itemtype

    def _set_itemtype(self, itemtype):
        self._itemtype = itemtype
        print(f"{self._item_term} item type set to '{self.itemtype}'.")
