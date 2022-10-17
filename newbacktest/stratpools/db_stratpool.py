# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_hierarchy import DirPaths, FileNames
from newbacktest.abstractclasses.db_abstract_keyval import AbstractKeyValDatabase
from file_functions import savedftocsv_fullpath, join_str


class StratPoolDatabase(AbstractKeyValDatabase):
    '''
    When a Strategy and startdate is proposed, this database is searched by stratcode to see whether a stratpool already exists.  If it doesnt exist, the stratpool is added.
    A stratpool consists of a resulting dataframe of stocks after a given strategy has been applied to the existing stocks as of the date given.  If the strategy is a sorter, then it'll be a ranking.  If the strategy is a filter, it would simply be a list of stocks that satisfied the strategy's filter criteria.
    database structure = {
            stratcode: {
                <invest_startdate>: <stratpoolobject>,
                <invest_startdate>: <stratpool>,
                ...
            },
            stratcode: {...},
            ...
        }
    '''
    _emptydb = {
        'properties': {'num_pools': 0},
        'data': {}
        }

    def __init__(self):
        self._dbname = "Strategy Pool Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_stratpool
        self._keyname_term = "stratcode"
        self._item_term = "Stratpool"

    @property
    def num_pools(self):
        return self._open_database()['properties']['num_pools']

    def _add_to_num_pools(self, dbdata):
        dbdata['properties']['num_pools'] = self.num_pools + 1

    def view_item(self, stratcode):
        return self._open_database()["data"].get(stratcode, 0)

    def view_stratpool(self, stratcode, invest_startdate):
        stratcode_exist = self.view_item(stratcode)
        if stratcode_exist:
            return self._open_database()["data"][stratcode].get(invest_startdate, 0)
        return stratcode_exist

    def save_stratpool_todisk(self, stratcode, invest_startdate):
        saveloc = Path(join_str([DirPaths().bot_dump, f"stratpool{invest_startdate}.csv"]))
        stratpool = self.view_stratpool(stratcode, invest_startdate)
        if stratpool:
            savedftocsv_fullpath(saveloc, stratpool.itemdata)
            print(f'Succesfully saved stratpool with code "{stratcode}" and invest_startdate of {invest_startdate} to disk at location "{saveloc}".')
        else:
            print(f'Stratpool with code "{stratcode}" and invest_startdate of {invest_startdate} not found in {self._dbname}.')

    # add item to database
    def add_item(self, item):
        stratcode = item.itemcode
        invest_startdate = item.invest_startdate
        db_data = self._open_database()
        db_contents = db_data["data"]
        if not db_contents or not db_contents.get(stratcode, 0):
            db_contents[stratcode] = {invest_startdate: item}
        elif not db_contents[stratcode].get(invest_startdate, 0):
            db_contents[stratcode][invest_startdate] = item
        else:
            existing = self.view_stratpool(stratcode, invest_startdate)
            print(f"A {self._item_term} for the invest_startdate of {invest_startdate} and stratcode of '{stratcode}' already exists in the {self._dbname}:\n : {self._item_term}: {existing.itemdata}\ncreated on: {existing.creationdate.dtobject}.")
            return
        self._add_to_num_pools(db_data)
        self._save_changes(db_data)
        print(f"{self._item_term} with code '{stratcode}' and invest_startdate of {invest_startdate} successfully saved to {self._dbname}!")

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
