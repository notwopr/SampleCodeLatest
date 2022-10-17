"""
Title: Stock Library
Date Started: July 28, 2020
Version: 1.0
Version Start Date: July 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Master sheet to view, add, remove stocks to/from new list or current list.
VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
from playsound import playsound
#   LOCAL APPLICATION IMPORTS
from STOCKLIBRARY_FUNCTIONS import addremove_stock, switchlist, save_stocklist, viewstocklist, constructportlib, renamestocklist
from STOCKLIBRARY_GRAPHGRADER import graphgrader
from computersettings import computerobject

# STOCKLIST FILE LOCATIONS
STOCKLISTS = computerobject.bot_important / 'stocklists'
GRAPHGRADEPARENT = STOCKLISTS / 'graphgrades'
CURRENT_SL = GRAPHGRADEPARENT / 'CURRENT'
PAST_SL = GRAPHGRADEPARENT / 'PAST'
PORTFOLIODIR = STOCKLISTS / 'portfolios'

# REMOVE STOCK FROM LIST
#addremove_stock('verbose', 'jan2021portfolio__20210115_reviewedrank', PORTFOLIODIR, PAST_SL, 'TTD', 'remove')

# ADD STOCK TO LIST
#addremove_stock('verbose', '2018methodv1_top10_2020-09-16', PORTFOLIODIR, PAST_SL, 'ZM', 'add')

# RENAME STOCK LIST
renamestocklist('verbose', 'manualfinviz_Feb2021pricelt100_top9_20210122_bestsalesindexscorerank', PORTFOLIODIR, PAST_SL, 'manualfinviz_Feb2021_pricelt100_age1to5yr_top9_20210122_bestsalesindexscorerank')
# MOVE STOCK FROM ONE LIST TO ANOTHER LIST
# destlist = 'GRADE2_STOCKLIST'
# originlist = 'GRADE1_STOCKLIST'
# listdir = CURRENT_SL
# archivedir = PAST_SL
# candidatestock = 'ARGX'
# switchlist('verbose', destlist, originlist, listdir, archivedir, candidatestock)

# VIEW A LIST
# viewstocklist('GRADE2_STOCKLIST', CURRENT_SL)

# GRADE A GIVEN LIST OF STOCKS
#graphgrader(stocklist, '2015-10-09', '2015fallcandidates', CURRENT_SL, PAST_SL)

# STORE A STOCKLIST
#stocklistloc = r'F:\BOT_DUMP\strattest_singles\D20210111T1\Stage3_parent\Stage3_STAGE3_reboundbotv2_finalists_as_of_2020-02-19.csv'
#resultdf = pd.read_csv(stocklistloc)
#stocklist = resultdf['stock'].tolist()[:10]
stocklist = [
    'FUV',
    'ATNX',
    'GRWG',
    'YETI',
    'JHG',
    'AZRE',
    'EVER',
    'SMPL',
    'TPIC'
]

#methodname = 'manualfinviz_Feb2021_pricelt100_age1to5yr'
#rankbatch = 'top9'
#existdate = '20210122'
#ranktype = 'bestsalesindexscore'
#listname = f'{methodname}_{rankbatch}_{existdate}_{ranktype}rank'
#stocklistdest = PORTFOLIODIR
#save_stocklist(listname, stocklistdest, stocklist)
#viewstocklist(listname, stocklistdest)

# UPDATE PORTFOLIO CSV LIBRARY
constructportlib(PORTFOLIODIR, STOCKLISTS)
playsound('C:\Windows\Media\Ring03.wav')
