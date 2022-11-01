# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from inspect import getmembers, isfunction
import importlib
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.module_operations import ModuleOperations
import newbacktest.ingredients_funclib
from newbacktest.abstractclasses.db_abstract import AbstractDatabase
from file_hierarchy import DirPaths, FileNames


class MetricFunctionDatabase(AbstractDatabase):
    '''
    db_structure = {
        <metricfuncname>: (<mfcode>, <metricfunclocation>),
        <metricfuncname>: (<mfcode>, <metricfunclocation>),
        ...
    }
    '''
    _emptydb = {}
    pkgimport = newbacktest.ingredients_funclib
    pgkimportstringform = 'newbacktest.ingredients_funclib'

    def __init__(self):
        self._dbname = "Metric Function Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_metricfunction
        self._keyname_term = "metricfuncname"
        self._item_term = "Metric Function Profile"

    def view_item(self, keyname):
        return self._open_database().get(keyname, 0)

    def add_item(self, item):
        pass

    def update_mfdb(self):
        '''
        return dict = {
            <metricfuncstringname> : tuple(ID#, <stringnameofmoduleloc>),
            ...
        }
        pgkimport is the folder containing the files containing the metricfunctions in the form of an import e.g. Modules.metriclibrary
        warning: for the os.path.dirname(<modulefolder>.__file__) attribute to work, make sure you have an __init__.py file in that modulefolder'''

        filenamelist = ModuleOperations().get_filenameslist_within_modulefolder(self.pkgimport)
        for filename in filenamelist:
            module = importlib.import_module(f'{self.pgkimportstringform}.{filename}')
            for e in getmembers(module, lambda member: isfunction(member) and member.__module__ == module.__name__):
                '''member.__module__ == module.__name__ means to only include objects within the module that were defined within the module and not imported'''
                '''getmembers retrieves all objects with the given module as a list of tuples.  Each tuple is of the form (objectname, object)'''
                allfuncnames = self._open_database()
                if allfuncnames and allfuncnames.get(e[0], 0):
                    print(f'Metricfunction "{e[0]}" already in database.')
                else:
                    allfuncnames[e[0]] = (len(allfuncnames), f'{self.pgkimportstringform}.{filename}')
                    self._save_changes(allfuncnames)
                    print(f"Metric Function {e[0]}: {allfuncnames[e[0]]} successfully saved to {self._dbname}!")

    def metricfuncname_to_metricfuncobj(self, metricfuncname):
        '''given metricfuncname in string form, return the function object'''
        return ModuleOperations().getobject_byvarname(self.view_item(metricfuncname)[1], metricfuncname)

    def get_metricfuncargnames(self, metricfuncname):
        '''returns list of strings representing the parameter names of the given metricfunction name'''
        metricfuncobj = self.metricfuncname_to_metricfuncobj(metricfuncname)
        return ModuleOperations().get_function_parameternames(metricfuncobj)

    def get_metricfuncargdict(self, metricfuncname, igsettingsdict, date, seriesdata):
        '''given metricfuncname, ingredient and iterable specific input data, return dictionary of metricfunc args'''
        '''all metricfunctions across the entire codebase that require seriesdata as input needs to use the name 'seriesdata' in its definition'''
        argdict = {}
        for argname in self.get_metricfuncargnames(metricfuncname):
            argval = igsettingsdict.get(argname, 0)
            if argname != "seriesdata" and argname != 'invest_startdate' and not argval:
                raise ValueError(f'The metricfunc "{metricfuncname}" requires a "{argname}" parameter, but it is not found in the ingredient settings dict.\nOffending ingredient:\n{igsettingsdict}')
            if argname == 'seriesdata':
                argval = seriesdata
            if argname == 'invest_startdate':
                argval = date
            argdict[argname] = argval
        return argdict
