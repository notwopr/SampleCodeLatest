# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from functools import partial
import multiprocessing as mp
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from machinesettings import _machine


class MultiProcessor:
    chunksize = 1

    def mp_mapasync_getresults(self, targetfunc, iterables, enumerateiters, targetvars):
        '''targetvars is a tuple. returns list?'''
        if enumerateiters == 'yes':
            mpiterables = enumerate(iterables)
        else:
            mpiterables = iterables
        fn = partial(targetfunc, *targetvars)
        pool = mp.Pool(_machine.use_cores)
        r = pool.map_async(fn, mpiterables, self.chunksize).get()
        pool.close()
        pool.join()
        return r

    def dataframe_reduce_bycol(self, pricematrixdf, metricfunc, metricfuncargs):
        '''given a dataframe and function, map function over each column and return the resulting 1xN series?
        while .iteritems() converts the dataframe into colwise iterables, each iterable is a tuple (colname, series)
        ('iteritems' is deprecated. use 'items' instead)
        '''
        r = self.mp_mapasync_getresults(metricfunc, pricematrixdf.items(), 'no', metricfuncargs)
        return r
