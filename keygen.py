from computersettings import computerobject
from file_functions import readpkl, savetopkl

k = ''
savetopkl('auth', computerobject.auth, k)
kr = readpkl('auth', computerobject.auth)
print(kr==k, kr)
