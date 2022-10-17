"""
Title: BOT Param Maker
Date Started: Jan 22, 2022
Version: 1.00
Version Start: Jan 22, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Functions to create dict used as the primary parameters input for a bot
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import re
from pathlib import Path
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_hierarchy import DirPaths


# brpb = bot run param builder
def brpb_base(testregimename, chunksize):
    fulltimestr = str(dt.datetime.now())
    return {
        'rootdir': Path(DirPaths().bot_dump),
        'todaysdate': fulltimestr[:10],
        'testnumber': re.sub(r'\.|\:', '', fulltimestr[11:]),
        'testregimename': testregimename,
        'chunksize': chunksize
        }
