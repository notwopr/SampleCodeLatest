from newbacktest.abstractclasses.db_abstract import AbstractDatabase
from file_hierarchy import DirPaths, FileNames


class PerfMetricNameDatabase(AbstractDatabase):
    '''
    db_structure = [
        <perfmetricnamestring>,
        <perfmetricnamestring>,
        ...
    ]
    '''
    _emptydb = set()

    def __init__(self):
        self._dbname = "Performance Metric Function Names Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_perfmetricnames
        self._item_term = "perfmetricname"

    # return list of all keys in the database
    def view_database(self):
        return self._open_database()

    def view_item(self, term):
        pass

    def add_item(self, newperfmetricnames):
        '''when you want to add a list of new perfmetricnames'''
        setofpmn = self._open_database()
        old_len = len(setofpmn)
        toadd = set(newperfmetricnames).difference(setofpmn)
        setofpmn.update(newperfmetricnames)
        self._save_changes(setofpmn)
        print(f'{len(setofpmn)-old_len} new perfmetricnames added to current set of perfmetricnames.  The following were added:\n{toadd}.')
