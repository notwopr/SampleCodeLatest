import time
import pandas as pd
import modin.pandas as mpd
from pathlib import Path
import ray
ray.init()

fn = Path(r'C:\Users\david\Downloads\esea_master_dmg_demos.part1.csv')
df = pd.read_csv(fn)
# pandas method
s = time.time()
df = pd.concat([df for _ in range(5)])
e = time.time()
print("Pandas Loading Time = {}".format(e-s))

fn = Path(r'C:\Users\david\Downloads\esea_master_dmg_demos.part1.csv')
df = mpd.read_csv(fn)
# modin method
s = time.time()
df = mpd.concat([df for _ in range(5)])
e = time.time()
print("Modin Loading Time = {}".format(e-s))
