'''
Parallelization Options
Using Pandas directly with two threads
Using Dask with threads and separate processes
Using Modin with a Ray backend
Using multiprocessing.Pool to launch separate processes
Using joblib.parallel to launch separate threads and processes


Map Async performed the best
serial method
elapsed: 8.658790826797485 secs
[497, 524, 480, 513, 506, 491, 479, 502, 503, 473]
map method
elapsed: 4.846298933029175 secs
[497, 524, 480, 513, 506, 491, 479, 502, 503, 473]
mapasync method
elapsed: 4.71025276184082 secs
[497, 524, 480, 513, 506, 491, 479, 502, 503, 473]
starmap method
elapsed: 5.518808841705322 secs
[497, 524, 480, 513, 506, 491, 479, 502, 503, 473]
starmapasync method
elapsed: 5.582961082458496 secs
[497, 524, 480, 513, 506, 491, 479, 502, 503, 473]
'''

import numpy as np
import time
import multiprocessing as mp


# Solution Without Paralleization
def howmany_within_range(row, minimum, maximum):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count


def serialmethod(data):
    results = []
    for row in data:
        results.append(howmany_within_range(row, minimum=4, maximum=8))
    return results


def applymethod(data):
    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())
    # Step 2: `pool.apply` the `howmany_within_range()`
    results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
    # Step 3: Don't forget to close
    pool.close()
    return results


# Redefine, with only 1 mandatory argument.
def howmany_within_range_rowonly(row, minimum=4, maximum=8):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count


# Step 1: Redefine, to accept `i`, the iteration number
def howmany_within_range2(i, row, minimum, maximum):
    """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return (i, count)


# Step 2: Define callback function to collect the output in `results`
def collect_result(result):
    global results
    results.append(result)


def applyasyncmethod(data):
    pool = mp.Pool(mp.cpu_count())
    # Step 3: Use loop to parallelize
    for i, row in enumerate(data):
        pool.apply_async(howmany_within_range2, args=(i, row, 4, 8), callback=collect_result)
    # Step 4: Close Pool and let all the processes complete
    pool.close()
    pool.join()  # postpones the execution of next line of code until all processes in the queue are done.
    # Step 5: Sort results [OPTIONAL]
    results.sort(key=lambda x: x[0])
    results_final = [r for i, r in results]
    return results_final


def applyasyncmethod_nocallback(data):
    pool = mp.Pool(mp.cpu_count())
    # Step 3: Use loop to parallelize
    result_objects = [pool.apply_async(howmany_within_range2, args=(i, row, 4, 8)) for i, row in enumerate(data)]
    # result_objects is a list of pool.ApplyResult objects
    results = [r.get()[1] for r in result_objects]
    # Step 4: Close Pool and let all the processes complete
    pool.close()
    pool.join()  # postpones the execution of next line of code until all processes in the queue are done.
    return results


def mapmethod(data):
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(howmany_within_range_rowonly, [row for row in data])
    pool.close()
    return results


def mapasyncmethod(data):
    pool = mp.Pool(mp.cpu_count())
    results = pool.map_async(howmany_within_range_rowonly, [row for row in data]).get()
    pool.close()
    return results


def starmapmethod(data):
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(howmany_within_range, [(row, 4, 8) for row in data])
    pool.close()
    return results


def starmapasyncmethod(data):
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap_async(howmany_within_range2, [(i, row, 4, 8) for i, row in enumerate(data)]).get()
    pool.close()
    results = [r for i, r in results]
    return results


if __name__ == '__main__':

    # Prepare data
    np.random.RandomState(100)
    arr = np.random.randint(0, 10, size=[200000, 1000])
    data = arr.tolist()

    start = time.time()
    results = serialmethod(data)
    end = time.time()
    print('serial method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])
    '''
    start = time.time()
    results = applymethod(data)
    end = time.time()
    print('apply method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])

    results = []
    start = time.time()
    results = applyasyncmethod(data)
    end = time.time()
    print('applyasync method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])

    start = time.time()
    results = applyasyncmethod_nocallback(data)
    end = time.time()
    print('applyasyncnocallback method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])
    '''
    start = time.time()
    results = mapmethod(data)
    end = time.time()
    print('map method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])

    start = time.time()
    results = mapasyncmethod(data)
    end = time.time()
    print('mapasync method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])

    start = time.time()
    results = starmapmethod(data)
    end = time.time()
    print('starmap method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])

    start = time.time()
    results = starmapasyncmethod(data)
    end = time.time()
    print('starmapasync method')
    print(f'elapsed: {end-start} secs')
    print(results[:10])
