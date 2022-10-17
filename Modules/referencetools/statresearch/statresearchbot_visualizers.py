"""
Title: Best Weight Finder
Date Started: Feb 24, 2020
Version: 1.0
Version Start: Feb 24, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Runs test with given weights, returns results, review results, assigns new weights and repeats until results minimizes inaccuracies as low as possible.
"""
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import seaborn as sns


# SCATTER PLOT OF VARIABLE CORRELATIONS OF A DATAFRAME
def scattermatrix(dataframe):
    scatter_matrix(dataframe)
    plt.show()


# HEATMAP THE DATAFRAME
def heatmap(dataframe):
    corr = dataframe.corr()
    sns.heatmap(corr,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values)
    plt.show(sns)
