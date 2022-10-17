import numpy as np
import pandas as pd
import multiprocessing as mp
from pathos.multiprocessing import ProcessingPool as Pool
# pathos package is used for parallel processing over an entire dataframe as opposed to just row, or just column wise; https://www.machinelearningplus.com/python/parallel-processing-python/

# draw dataframe consisting of integers in range of 3 to 10, with 500 rows and 2 columns in size
df = pd.DataFrame(np.random.randint(3, 10, size=[500, 2]))


def func(df):
    return df.shape


if __name__ == '__main__':
    print(df.head())

    cores = mp.cpu_count()
    print(f'cores: {cores}')
    # split dataframe into n=cores subdfs; axis=0 splits along rows; axis=1 splits along columns; when splitting; index and col headers retained
    df_split = np.array_split(df, cores, axis=1)
    print(df_split)
    # create the multiprocessing pool
    pool = Pool(cores)

    # process the DataFrame by mapping function to each df across the pool (vstack stackes 1D arrays together into 2D array (1xN matrix))
    df_out = np.vstack(pool.map(func, df_split))

    # close down the pool and join (clear is pathos specific)
    pool.close()
    pool.join()
    pool.clear()

    print(df_out)
