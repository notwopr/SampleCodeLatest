from file_functions import readpkl_fullpath, savetopkl
from computersettings import computerobject
import datetime as dt
for c in computerobject.strattester_testruns.iterdir():
    s = readpkl_fullpath(c)
    # if todaysdate < 2022-03-20 and 'strat_name' != 'S3_RBv9' append '_wrongweights'
    if dt.date.fromisoformat(s['todaysdate']) < dt.date.fromisoformat('2022-03-20') and s['strat_name'] != 'S3_RBv9':
        print(f"todaysdate: {s['todaysdate']}, lessthan? {dt.date.fromisoformat(s['todaysdate']) < dt.date.fromisoformat('2022-03-20')}, current name: {s['strat_name']}")
        s['strat_name'] = s['strat_name'] + '_wrongweights'
    savetopkl(c.stem, computerobject.strattester_testruns, s)
