from file_functions import readpkl_fullpath, savetopkl
from computersettings import computerobject
from Modules.dict_functions import gen_dict_from_listofdicts
from Modules.numbers_formulas import geometric_rate

for c in computerobject.strattester_testruns.iterdir():
    s = readpkl_fullpath(c)
    # if stat begins with 'period', convert to daily
    lofd = [{'daily_'+k[7:]: geometric_rate(s[k], s['investperiod'])} for k in s.keys() if k.startswith('period_')]
    s = {**s, **gen_dict_from_listofdicts(lofd)}
    savetopkl(c.stem, computerobject.strattester_testruns, s)
