from file_hierarchy import DirPaths, FileNames
from newbacktest.abstractclasses.db_abstract_keyval import AbstractKeyValDatabase


class CloudSampleDatabase(AbstractKeyValDatabase):
    '''
    When a Stage Recipe is proposed, this database is searched by srcode to see whether it already exists.  If it doesnt exist, the stagerecipe is added.
    A stage recipe's main data consists of a list of igcodes that point to actual ingredients and their settings.  The recipe itself doesnt contain the ingredient data.
    database structure = {
            cloudsampcode: <cloudsampleobject>,
            cloudsampcode: <cloudsampleobject>,
            ...
        }
    <stagerecipeobject>.itemdata = <list of ingredient codes>
    '''
    _emptydb = {}

    def __init__(self):
        self._dbname = "Cloud Sample Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_cloudsample
        self._keyname_term = "cloudsampcode"
        self._item_term = "Cloud Sample"

    def _verify_item(self, item):
        pass

    def _prep_item(self, item):
        pass
