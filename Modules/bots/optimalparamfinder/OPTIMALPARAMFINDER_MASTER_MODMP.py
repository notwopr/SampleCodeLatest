"""
Title: OPTIMAL PARAM FINDER MASTER - MODIFY A CURRENT METRIC PANEL
Date Started: July 23, 2020
Version: 1.00
Version Start: July 23, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Given a metricpanel and mktbeatstats summary, change metricpanel settings and save new one.
VERSIONS:
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import copy
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from OPTIMALPARAMFINDER_BASE_METPANELACCURACY import getfiltermetricparams
from filelocations import savetopkl, readpkl
from computersettings import BOT_IMPORTANT


# SAVEFOLDER FOR METRICPANELS
mpsavefolder = BOT_IMPORTANT / 'METRICPANELS'

# SET EXISTENCE DATE UPON WHICH THE ORIG METRICPANEL WAS BASED
exist_date = '2018-06-01'

# SET METRICPANEL TO MODIFY
metricpanelfileloc = Path(r'D:\BOT_DUMP\optimalparamfinder\D20200722T1')
metricpanelfilename = 'newmetricstorun_exist2018-06-01_today2020-07-22'
origmetricpanelparams = readpkl(metricpanelfilename, metricpanelfileloc)

# SET METRIC RANGE FILE
metricrangefileloc = Path(r'D:\BOT_DUMP\optimalparamfinder\D20200722T1\metricpaneldump\resultfiles')
metricrangefilename = 'mktbeatstatsummdf_testperiod2018-06-01_2019-06-01'
metricrangedf = readpkl(metricrangefilename, metricrangefileloc)

# SET TESTCODE UPON WHICH THE ORIG METRICPANEL WAS BASED
testcode = 'D20200722T1'

# TURN OFF FILTERS
filterstate = 'doublebound'


if __name__ == '__main__':

    # MAKE DEEPCOPY OF ORIGINAL
    metricpanel_moddedparams = copy.deepcopy(origmetricpanelparams)
    # EXTRACT METRICS
    metrics_to_run = metricpanel_moddedparams[0]['method_specific_params']['fnlbatches'][0]['batch']
    # MODIFY FILTER STATE
    if filterstate == 'filtersoff':
        for metricitem in metrics_to_run:
            metricitem.update({'filterdirection': 'no'})
    elif filterstate == 'singlebound':
        metrics_to_run = getfiltermetricparams(metricrangedf, metrics_to_run, filterstate)
    elif filterstate == 'doublebound':
        for metricitem in metrics_to_run:
            metricitem.update({'filterdirection': 'between'})
        metrics_to_run = getfiltermetricparams(metricrangedf, metrics_to_run, filterstate)

    # SAVE CHANGES TO MODDED METRICPANEL
    metricpanel_moddedparams[0]['method_specific_params']['fnlbatches'][0]['batch'] = metrics_to_run

    # SAVE MODDED METRICPANEL TO FILE
    metricpanelversioncode = f"ED{exist_date.replace('-', '')}_{testcode}"
    savetopkl(f'{metricpanelversioncode}_{filterstate}', mpsavefolder, metricpanel_moddedparams)
    # REPORT
    metrics_to_run = metricpanel_moddedparams[0]['method_specific_params']['fnlbatches'][0]['batch']
    for metricitem in metrics_to_run:
        print(metricitem)
