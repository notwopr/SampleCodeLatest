"""
Title: Best Part of the Year (BPOTY) Bot Grapher Script
Date Started: Sept 28, 2020
Version: 1.0
Version Start Date: Sept 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Graph results of BPOTYBOT.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from SCRATCHPAPER_GRAPHING import heatmap
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# DEFINE 'PART OF THE YEAR'
resultfileloc = r'F:\BOT_DUMP\bpotybot\D20201025T3\bestyear_nasdaq_1972_to_2020_median_ols_no_s_1.5.csv'
resultdf = pd.read_csv(resultfileloc)

# single column heatmap
heatmapsettings = {
    'heatmapregion': resultdf.iloc[:, 1:],
    'centerval': 0,
    'xticklabels': False,
    'yticklabels': resultdf['YEAR'].tolist(),
    'xlabel': 'PORTION OF THE YEAR',
    'ylabel': 'YEAR',
    'showcellvalues': True,
    'colorpalette': 'RdBu',
    'colorbar': True
}

heatmap(heatmapsettings)
