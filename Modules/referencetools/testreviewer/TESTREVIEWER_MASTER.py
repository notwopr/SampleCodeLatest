"""
Title: TESTREVIEWER - RANK METHOD _MASTER SCRIPT
Date Started: Feb 25, 2020
Version: 1.0
Version Start: Feb 25, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Visually compare graphs and tally results and return scores of best method.
Remove test2 and add rankviewer.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from TESTREVIEWER_RANKMETHOD_BASE import rankmethods
from TESTREVIEWER_CLASSES import TestMethodCandidate
from TESTREVIEWER_INACCURACYTESTER import inaccuracytester, inaccpackage
from TESTREVIEWER_RANKVIEWER_BASE import squeezefactor_viewer

# GLOBAL PARAMETERS
reviewtype = ''
viewmod = 'baremin'
sortascend = True
dataloc = 'incsv'

# INACCURACY GLOBAL PARAMETERS
testsample = TestMethodCandidate('layercake', 'layercake', 'D20200318T1', 1)
min_age = ''
rankingtotal = 50

# INACCURACYTESTER PARAMETERS
rfile = testsample.rankingfile()
rankcolname = rfile.columns[-2]

# RANKMETHODS PARAMETERS
targetinacclen = 5
reviewamount = 5
rankcols = [
    'RANK_convertdgr',
    'RANK_geometricdpc',
    'RANK_convertdpc',
    'RANK_dpc'
    ]


'''COMPARE INACCURACY OF ONE METHOD AGAINST EVERY OTHER METHOD'''
#rankmethods(testsample, targetinacclen, reviewamount, viewmod, reviewtype, rankcols, dataloc)

'''GET INACCURACY SCORE FOR A SINGLE RANKCOL'''
inaccuracytester(testsample, min_age, rankingtotal, rankcolname, viewmod, reviewtype, sortascend, dataloc)

'''GET A DATAFRAME OF INACCURACY SCORES FOR ALL RANK COLUMNS FOR A GIVEN TEST'''
#inaccpackage(testsample, min_age, rankingtotal, viewmod, reviewtype, sortascend)
#squeezefactor_viewer(testsample, rankingtotal, sortascend, rankcolname)
