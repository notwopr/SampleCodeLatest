# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
from abc import ABC, abstractmethod
import os
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl_fullpath
from file_functions import join_str, savetopkl_fullpath


class AbstractDatabase(ABC):

    @property
    def _filepath_to_db(self):
        return Path(join_str([self._parentdirpathstring, f'{self._dbfilenamestring}.pkl']))

    # open database
    def _open_database(self):
        return readpkl_fullpath(self._filepath_to_db) if os.path.exists(self._filepath_to_db) else self._emptydb

    # save item to database
    def _save_changes(self, db_contents):
        savetopkl_fullpath(self._filepath_to_db, db_contents)

    # return list of all keys in the database
    def view_database(self):
        return self._open_database()

    # lookup item
    @abstractmethod
    def view_item(self, term):
        pass

    # add item to database
    @abstractmethod
    def add_item(self, item):
        pass

    def __str__(self):
        return f'The {self._dbname} contains:\n{self._item_term}s: {len(self._open_database())}'
