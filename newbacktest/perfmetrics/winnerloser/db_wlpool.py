# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_hierarchy import DirPaths, FileNames
from newbacktest.baking.baker_wlpool import BakerWLPool
from newbacktest.abstractclasses.db_abstract_keyval import AbstractKeyValDatabase


class WinLosePoolDatabase(AbstractKeyValDatabase):
    '''
    The Winner Loser Pool Database contains dataframes of winner and loser pools sorted by winloseprofile code and then by invest_startdate.
    structure = {
        <sampcode>: {
                invest_startdate: <wlpoolobj>,
                invest_startdate: <wlpoolobj>,
                ...

            }
        ....
    }
    '''
    _emptydb = {
        'properties': {'num_pools': 0},
        'data': {}
        }

    def __init__(self):
        self._dbname = "Winner Loser Pool Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_wlpool
        self._keyname_term = "wlprofcode"
        self._item_term = "WLPool"

    @property
    def num_pools(self):
        return self._open_database()['properties']['num_pools']

    def _add_to_num_pools(self, dbdata):
        dbdata['properties']['num_pools'] = self.num_pools + 1

    def view_item(self, wlprofcode):
        return self._open_database()["data"].get(wlprofcode, 0)

    def view_wlpool(self, wlprofcode, invest_startdate):
        wlprofcode_exist = self.view_item(wlprofcode)
        if wlprofcode_exist:
            return self._open_database()["data"][wlprofcode].get(invest_startdate, 0)
        return wlprofcode_exist

    def add_item(self, wlprofcode, invest_startdate):
        db_data = self._open_database()
        db_contents = db_data["data"]
        if not db_contents or not db_contents.get(wlprofcode, 0):
            wlpoolobj = BakerWLPool()._bake_wlprofile(wlprofcode, invest_startdate)
            db_contents[wlprofcode] = {invest_startdate: wlpoolobj}
        elif not db_contents[wlprofcode].get(invest_startdate, 0):
            wlpoolobj = BakerWLPool()._bake_wlprofile(wlprofcode, invest_startdate)
            db_contents[wlprofcode][invest_startdate] = wlpoolobj
        else:
            existing = self.view_wlpool(wlprofcode, invest_startdate)
            print(f"A {self._item_term} for the invest_startdate of {invest_startdate} and stratcode of '{wlprofcode}' already exists in the {self._dbname}:\n : {self._item_term}: {existing.itemdata}\ncreated on: {existing.creationdate.dtobject}.")
            return
        self._add_to_num_pools(db_data)
        self._save_changes(db_data)
        print(f"{self._item_term} with code '{wlprofcode}' and invest_startdate of {invest_startdate} successfully saved to {self._dbname}!")

    def _check_existence(self):
        pass

    def _add_item_to_db_data(self, item, keyname):
        pass

    def _verify_item(self, item):
        pass

    def _prep_item(self, item):
        pass

    def __str__(self):
        return f'The {self._dbname} contains:\n{self._keyname_term}s: {len(self._open_database()["data"])}\n{self._item_term.lower()}s: {self.num_pools}'
