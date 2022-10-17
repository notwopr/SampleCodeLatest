from file_hierarchy import DirPaths, FileNames
from newbacktest.abstractclasses.db_abstract_keyval import AbstractKeyValDatabase


class WinLoseProfDatabase(AbstractKeyValDatabase):
    '''
    When a Win Lose Profile is proposed, this database is searched by wlprofcode to see whether it already exists.  If it doesnt exist, the profile is added.
    A win lose profile's main data consists of a list of igcodes that point to actual ingredients and their settings.  The profile itself doesn't contain the ingredient data.
    database structure = {
            wlprofcode: <wlprofileobject>,
            wlprofcode: <wlprofileobject>,
            ...
        }
    <wlprofileobject>.itemdata = <list of ingredient codes>
    '''
    _emptydb = {}

    def __init__(self):
        self._dbname = "Winner Loser Profile Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_wlprofile
        self._keyname_term = "wlprofcode"
        self._item_term = "Win Lose Profile"

    def _verify_item(self, item):
        pass

    def _prep_item(self, item):
        pass
