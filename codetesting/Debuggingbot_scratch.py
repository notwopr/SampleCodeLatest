"""
Title: Debugging Bot
Date Started: July 23, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the Debugging Bot is to be the platform for debugging and optimizing code.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import time
#import Resource
#import objgraph
#import random
#from pathlib import Path
#   THIRD PARTY IMPORTS
#import numpy as np
#   LOCAL APPLICATION IMPORTS
# from foliosizer_masterscript import testmod
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
#from TIMECALIB_COMPARISON_BASE import smoothnessarr_mean, timecalib_comparison_master
#from filelocations import readpkl


def runtime_logger(num_runs, func_name, targetfunc, targetinputs):
    results = []
    for i in range(0, num_runs):
        start = time.time()
        '''INSERT FUNCTION TO TEST HERE'''
        targetfunc(targetinputs)
        '''TESTFUNCTION END'''
        end = time.time()
        elapsed = end-start
        results.append(elapsed)
        print(f'Run {i}: {elapsed} secs')
    print(f'Ran {func_name} {num_runs} times. Average time per run is: {np.mean(results)} secs')


def run_custom(num, sortmeth, verbose, stocklist, metricfunc, rankdirection, end_date, avgmeth):
    results = []
    for i in range(0, num):
        start = time.time()
        '''INSERT FUNCTION TO TEST HERE'''
        print(timecalib_comparison_master(sortmeth, verbose, stocklist, metricfunc, rankdirection, end_date, avgmeth))
        '''TESTFUNCTION END'''
        end = time.time()
        elapsed = end-start
        results.append(elapsed)
        print(f'Run {i}: {elapsed} secs')
    avg = np.mean(results)
    print('Ran function', num, 'times. Average time per run is:', avg, 'secs')


def mem_cost():
    count = 10000
    test_object = myfunc()  # INSERT FUNCTION/OBJECT TO TEST HERE
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print("Memory usage is: {0} KB".format(mem))
    print("Size per obj: {0} KB".format(float(mem)/count))
    test_dict = {}
    test_dict['k'] = test_object
    objgraph.show_most_common_types()
    objgraph.show_backrefs(random.choice(objgraph.by_type('Foo')), filename="foo_refs.png")
    objgraph.show_refs(test_dict, filename='sample-graph.png')


# SET LOCATION OF STOCKLIST TO GRAPH
resultfileloc = Path(r'D:\BOT_DUMP\ONETIMETESTS\optimalparamfinder\D20200712T1\rankfiles')
resultfilename = 'mktbeatermetricsdf_testperiod2018-06-01_2019-06-01'
resultdf = readpkl(resultfilename, resultfileloc)
fullstocklist = resultdf['stock'].tolist()
random.shuffle(fullstocklist)
inputlist = fullstocklist[:8]

verbose = ''
avgmeth = 'mean'
metricfunc = smoothnessarr_mean
rankdirection = 1
end_date = '2018-06-01'

if __name__ == '__main__':

    for sortmeth in ['merge', 'tim']:
        stocklist = inputlist
        print(stocklist)
        run(1, sortmeth, verbose, stocklist, metricfunc, rankdirection, end_date, avgmeth)
