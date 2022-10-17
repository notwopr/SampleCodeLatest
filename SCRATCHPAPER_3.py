import pandas as pd
from newbacktest.datasource import DataSource
s = pd.Series([1,4,3,2,43,2,3])
df = DataSource().opends('eodprices')
df = df[['PHI']]
print(df)
exit()
d = df.iloc[:, 0]
pd.set_option('display.max_rows', None)

print(d)
print(d.index[0])
DATE = '1990-01-01'
