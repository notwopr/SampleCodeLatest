"""
Title: Best Streaks Base - Current to Next
Date Started: Oct 13, 2020
Version: 1.0
Version Start Date: Oct 13, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Runs Best Streak Bot on two given time periods, ideally consecutive periods.  This was created to find out how likely if a stock is ranked high in winstreak for one period, that it would also be ranked high again in the following period.  You can adjust the criteria for each period to be compared, but ideally they should be set the same to make the comparisons less biased.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from BESTSTREAK_BASE import beststreak_cruncher
from filelocations import buildfolders_singlechild, savetopkl
from genericfunctionbot import intersectlists


# returns how many stocks were in common between current streak period and subsequent streak period
def curr_to_next(verbose, dumpdest, resultdest, streakparam_dict):
    # build folder for current streak
    currfolder = buildfolders_singlechild(dumpdest, 'currstreak')
    # get current streak list
    currdf = beststreak_cruncher(verbose, streakparam_dict['currbeg'], streakparam_dict['currend'], streakparam_dict['currbenchticker'], streakparam_dict['currperiodlen'], streakparam_dict['curravg_type'], currfolder)
    currlist = currdf['stock'].tolist()[streakparam_dict['curr_rankbeg']:streakparam_dict['curr_rankend']]

    # build folder for subsequent streak
    nextfolder = buildfolders_singlechild(dumpdest, 'nextstreak')
    # get next streak list
    nextdf = beststreak_cruncher(verbose, streakparam_dict['nextbeg'], streakparam_dict['nextend'], streakparam_dict['nextbenchticker'], streakparam_dict['nextperiodlen'], streakparam_dict['nextavg_type'], nextfolder)
    nextlist = nextdf['stock'].tolist()[streakparam_dict['next_rankbeg']:streakparam_dict['next_rankend']]

    # get intersection of two lists
    stocksincommon = intersectlists(currlist, nextlist)
    # proportion of the currlist that is in the nextlist
    prop_pct = len(stocksincommon) / len(currlist)

    currnextsumm = {
        'currlist': currlist,
        'nextlist': nextlist,
        'incommon': stocksincommon,
        'prop_pct': prop_pct
    }
    summarydict = {}
    summarydict.update(streakparam_dict)
    summarydict.update(currnextsumm)

    # report results
    if verbose == 'verbose':
        print('currdf:\n', currdf)
        print('nextdf:\n', nextdf)
        for i in summarydict:
            print(f'{i}: {summarydict[i]}')

    # save results
    resultfn = f'trial{streakparam_dict["trialno"]}_winstreak_currbeg{streakparam_dict["currbeg"]}_nextbeg{streakparam_dict["nextbeg"]}'
    savetopkl(resultfn, resultdest, summarydict)
