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
#   THIRD PARTY IMPORTS
import numpy as np
#   LOCAL APPLICATION IMPORTS


def runtime_logger(num_runs, func_name, targetfunc, targetinputs):
    results = []

    for i in range(0, num_runs):
        start = time.time()
        '''INSERT FUNCTION TO TEST HERE'''
        other = targetfunc(*targetinputs)
        '''TESTFUNCTION END'''
        end = time.time()
        elapsed = end-start
        results.append(elapsed)
        # print(f'Run {i}: {elapsed} secs')
    print(f'Ran {func_name} {num_runs} times. Average time per run is: {np.mean(results)} secs')
