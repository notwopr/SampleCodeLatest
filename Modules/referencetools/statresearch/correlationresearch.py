"""
Title: Correlation Research
Version: 1.0
Date Started: May 1, 2020
Version Date: May 1, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Scratch paper for researching correlation functions.


"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import pandas as pd
#   LOCAL APPLICATION IMPORTS


# GRAPHS CORRELATION OF TWO LISTS
def twolistcorr(list1, list2, method):

    methods_dict = {'pearson': scipy.stats.pearsonr, 'spearman': scipy.stats.spearmanr, 'kendall': scipy.stats.kendalltau}

    arr1 = np.array(list1)
    arr2 = np.array(list2)
    r, pval = methods_dict[method](arr1, arr2)

    return r


# GRAPHS AND REPORTS PEARSON CORRELATION AS A DIGIT IN A LIST IS MOVED TO A DIFFERENT POSITION
def corrmove(origlist):
    modlist = origlist.copy()
    origlistarr = np.array(origlist)
    all_lists = []
    all_listnames = []
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for idx, val in enumerate(origlist):
        origidx = idx - 1
        if origidx < 0:
            origidx = 0
        modlist[origidx], modlist[idx] = modlist[idx], modlist[origidx]
        modlistarr = np.array(modlist)
        r = np.corrcoef(origlistarr, modlistarr)[0, 1]
        modlistname = 'first digit move {}: {}'.format(idx, r)
        modlistline, = ax1.plot(modlist, alpha=0.5, label=modlistname)
        all_lists.append(modlistline)
        all_listnames.append(modlistname)
        print(modlist, r)

    ax1.legend(all_lists, all_listnames)
    plt.show()
    print('\n')


def movingcorr(list1, list2, method):

    corr_results = []
    # ARE LISTS SAME LENGTH?
    if len(list1) != len(list2):
        print('The lengths of the two lists compared are not the same length.  Program exiting...')
        exit()
    elif len(list1) < 2 or len(list2) < 2:
        print('Both lists have a length of less than 2.  Both lists must have a length of 2 or greater to calculate correlation.  Program exiting...')
        exit()
    else:
        max_samp = len(list1)
        for i in range(2, max_samp+1):
            num_samp = i
            newlist1 = list1[:num_samp]
            newlist2 = list2[:num_samp]
            corr = twolistcorr(newlist1, newlist2, method)
            trialdict = {'num_samp': num_samp, 'corr': corr}
            corr_results.append(trialdict)

    corrdf = pd.DataFrame(data=corr_results)

    # GRAPH RESULTS
    xax = corrdf['num_samp']
    yax = corrdf['corr']
    plt.plot(xax, yax, marker='o')
    plt.xlabel('Number of Samples')
    plt.ylabel(f'{method} Correlation')
    plt.title('Correlation as a function of samples')
    plt.show()
