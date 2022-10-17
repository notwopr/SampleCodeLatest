# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
import pkgutil
import importlib
import inspect
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS


class ModuleOperations:
    def get_filenameslist_within_modulefolder(self, pkgimport):
        '''
        returns list of filenames (string form) given a folder (pkgimport).  pkgimport is not a string, but is an imported module or pkg.
        e.g. import Modules.metriclibrary is used to import the metriclibrary folder (or package), so the pkgimport = Modules.metriclibrary (which is a folder in the github repository)
        '''
        pkgpath = os.path.dirname(pkgimport.__file__)
        return [name for _, name, _ in pkgutil.iter_modules([pkgpath])]

    # LOAD MODULE BY ITS LOCATION IN STRING FORM
    def getmodule(self, modulename):
        return importlib.import_module(modulename)

    # LOAD OBJECT WITHIN MODULE BY ITS NAME IN STRING FORM AND ITS MODULE IN STRING FORM
    def getobject_byvarname(self, modulename, varname):
        return getattr(importlib.import_module(modulename), varname)

    def get_function_parameternames(self, metricfuncobj):
        '''returns a list of a function's parameter names (string format)'''
        return inspect.getfullargspec(metricfuncobj)[0]
