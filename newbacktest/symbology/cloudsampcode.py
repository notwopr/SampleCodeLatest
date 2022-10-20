# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.symbology.symbology import Symbology


class CloudSampCode:

    def decode(self, cloudsampcode):
        cloudsamp_startdate = cloudsampcode[-10:]
        numperiodstartindex = cloudsampcode[:-11].rfind('.')+1
        num_periods = cloudsampcode[numperiodstartindex:-11]
        ipcodestartindex = cloudsampcode.find(Symbology().ipcode_pred)
        ipcode = cloudsampcode[ipcodestartindex:numperiodstartindex-1]
        stratcode = cloudsampcode[len(Symbology().cloudsampcode_pred):ipcodestartindex-1]
        return {
            'stratcode': stratcode,
            'ipcode': ipcode,
            'num_periods': int(num_periods),
            'cloudsamp_startdate': cloudsamp_startdate,
            'stratipcode': cloudsampcode[len(Symbology().cloudsampcode_pred):numperiodstartindex-1]
        }

    def generate(self, stratcode, ipcode, num_periods, cloudsamp_startdate):
        cloudsampcode = f'{Symbology().cloudsampcode_pred}{stratcode}.{ipcode}.{num_periods}.{cloudsamp_startdate}'
        print(f"Cloud Sample Code set to '{cloudsampcode}'.")
        return cloudsampcode
