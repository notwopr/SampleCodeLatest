# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from newbacktest.perfmetrics.perfmetrics_db_funcprofile import PerfMetricFunctionDatabase
from newbacktest.perfmetrics.perfmetrics_db_perfprof import PerfProfileLib
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater_perfmetricnames import PerfMetricNameDatabase
from newbacktest.perfmetrics.baselistofperfmetrics import baselineperfmetrics


class PerfProfileUpdater:

    def update_profiles(self):
        '''adds and updates profiles which are perfmetricvalues for each perfmetric requested for every sample available.  the point is so that we have a ready to go df from which to run aggregate analyses and rankings.'''
        '''update perfmetricfunc profiles'''
        PerfMetricFunctionDatabase().update_mfdb()
        '''view contents of perf metric function db'''
        # pprint(PerfMetricFunctionDatabase().view_database())
        '''update perfmetricnamedatabase'''
        PerfMetricNameDatabase().add_item(baselineperfmetrics)
        '''retrieve updated list of perfmetricfuncnames'''
        perfmetricnames = PerfMetricNameDatabase().view_database()
        '''add missing samples to perf profile library and update them with latest metrics'''
        p = PerfProfileLib()
        p.sync_samples(perfmetricnames)
        '''view changes'''
        print(p)
        # pprint(p.view_database())
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(pd.DataFrame(data=p.view_database()))

    def get_samplesdf(self):
        '''update perfmetric profiles'''
        self.update_profiles()
        '''generate perfmetric df'''
        p = PerfProfileLib()
        sdf = pd.DataFrame(data=p.view_database())
        neworder = []
        remainder = set(sdf.columns)
        for m in baselineperfmetrics:
            if m in remainder:
                neworder.append(m)
                remainder.remove(m)
        neworder.extend(remainder)
        sdf = sdf[neworder]
        return sdf
