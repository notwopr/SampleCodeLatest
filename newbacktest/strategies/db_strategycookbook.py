from file_hierarchy import DirPaths, FileNames
from newbacktest.abstractclasses.db_abstract_keyval import AbstractKeyValDatabase


class StrategyCookBook(AbstractKeyValDatabase):
    '''
    When a Stage Recipe is proposed, this database is searched by srcode to see whether it already exists.  If it doesnt exist, the stagerecipe is added.
    A stage recipe's main data consists of a list of igcodes that point to actual ingredients and their settings.  The recipe itself doesnt contain the ingredient data.
    database structure = {
            stratcode: <strategyobject>,
            stratcode: <strategyobject>,
            ...
        }
    '''
    _emptydb = {}

    def __init__(self):
        self._dbname = "Strategy Cook Book"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_strategycookbook
        self._keyname_term = "stratcode"
        self._item_term = "Strategy"

    def _verify_item(self, item):
        pass

    def _prep_item(self, item):
        pass
