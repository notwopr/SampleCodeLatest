# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS

from abc import abstractmethod
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.abstractclasses.db_abstract import AbstractDatabase


class AbstractKeyValDatabase(AbstractDatabase):

    # lookup item by keyname
    def view_item(self, keyname):
        return self._open_database().get(keyname, 0)

    def view_item_details(self, keyname):
        return self._open_database().get(keyname, 0).__dict__

    def _check_existence(self, keyname):
        item = self.view_item(keyname)
        if item:
            print(f"An identical {self._item_term} already exists in the {self._dbname} with the code '{item.itemcode}'.\nPlease strive where possible to instantiate the desired {self._item_term} from the {self._dbname} for your use rather than use your current duplicate instantiation.  Otherwise, attributes of your duplicate instantiation that may differ from the original (e.g. creationdate) may unintentionally be attributed to the original, which could lead to inaccuracies.")
            return 1
        else:
            return 0

    # verify item before adding to database
    @abstractmethod
    def _verify_item(self, item):
        pass

    # prepare item before adding to database
    @abstractmethod
    def _prep_item(self, item):
        pass

    # add item to database
    def _add_item_to_db_data(self, item, keyname):
        db_contents = self._open_database()
        db_contents[keyname] = item
        self._save_changes(db_contents)
        print(f"{self._item_term} with code '{keyname}' successfully saved to {self._dbname}!")

    # add item to database
    def add_item(self, item):
        if self._check_existence(item.itemcode):
            return
        else:
            self._verify_item(item)
            self._prep_item(item)
            self._add_item_to_db_data(item, item.itemcode)

    # modify nickname/description
    def modify_nickname_or_description(self, keyname, newstring, switch):
        item = self.view_item(keyname)
        if not item:
            raise ValueError(f"The {self._item_term} with code '{keyname}' you wanted to modify was not found in the {self._dbname}.")
        if switch == 'nickname':
            oldstring = item.nickname
            item._set_nickname(newstring)
        elif switch == 'description':
            oldstring = item.description
            item._set_description(newstring)
        db_contents = self._open_database()
        db_contents[keyname] = item
        self._save_changes(db_contents)
        print(f"{switch.capitalize()} for {self._item_term} with code '{keyname}' successfully modified from '{oldstring}' to '{newstring}'.")
