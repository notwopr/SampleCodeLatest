"""
Title: GRAPH FUNCS - ANIMATION - MASTER
Date Started: Oct 27, 2020
Version: 1.0
Version Start: Oct 27, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Animate progression of price graph.

VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from computersettings import computerobject
from SCRATCHPAPER_GRAPHING_ANIMATE import animateprices


stock = '^IXIC'
beg_date = '2000-01-01'
end_date = ''
wintype = 'rolling'
winwidth = 360
margpct = 0.10
speed = 100
saveanim = 'no'
savefn = 'testanim'
savedir = computerobject.bot_dump / 'graphanimations'
animateprices(stock, beg_date, end_date, margpct, wintype, winwidth, speed, saveanim, savefn, savedir)
