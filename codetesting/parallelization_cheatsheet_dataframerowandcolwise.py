'''
df.itertuples() - iterate over dataframe rows as named tuples
df.iteritems() - iterate over dataframe columns as (colname, Series)
df.iterrows() - iterate over dataframe rows as (index, Series)


df
      num_legs  num_wings
dog          4          0
hawk         2          2
for row in df.itertuples():
    print(row)

Pandas(Index='dog', num_legs=4, num_wings=0)
Pandas(Index='hawk', num_legs=2, num_wings=2)

for row in df.itertuples(index=False):
    print(row)

Pandas(num_legs=4, num_wings=0)
Pandas(num_legs=2, num_wings=2)

for row in df.itertuples(name='Animal'):
    print(row)

Animal(Index='dog', num_legs=4, num_wings=0)
Animal(Index='hawk', num_legs=2, num_wings=2)

for row in df.itertuples(name=None):
    print(row)

(Index='dog', num_legs=4, num_wings=0)
(Index='hawk', num_legs=2, num_wings=2)
'''

import numpy as np
import pandas as pd
import multiprocessing as mp

df = pd.DataFrame(np.random.randint(3, 10, size=[5, 2]))


def hypotenuse(row):
    return round(row[1]**2 + row[2]**2, 2)**0.5


def sum_of_squares(column):
    return sum([i**2 for i in column[1]])


if __name__ == '__main__':
    print(df.head())

    # Row wise Operation
    with mp.Pool(4) as pool:
        result = pool.imap(hypotenuse, df.itertuples(name=None), chunksize=10)
        output = [round(x, 2) for x in result]

    print(output)

    # Column wise Operation
    with mp.Pool(2) as pool:
        result = pool.imap(sum_of_squares, df.iteritems(), chunksize=10)
        output = [x for x in result]

    print(output)
