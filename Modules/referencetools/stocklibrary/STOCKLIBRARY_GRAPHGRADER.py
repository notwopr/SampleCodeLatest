"""
Title: Stock Graph Grader
Date Started: Sept 22, 2020
Version: 1.00
Version Start Date: Sept 22, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Given list, sort list manually by grading its graph.
VERSIONS:

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
import datetime as dt
import shutil
#   THIRD PARTY IMPORTS
import pandas as pd
import easygui
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from SCRATCHPAPER_GRAPHING import graphsidebyside
from filelocations import create_nonexistent_folder, savetopkl


# takes list, assigns each stock in list to initialgrade, 'above', or 'below' categories and records it to gradesheet
def gradesorter(gradesheet, stocklist, initialgrade, existdate, gradecolname):
    # assign all stocklist the initialgrade
    gradesheet.loc[gradesheet['stock'].isin(stocklist), gradecolname] = initialgrade
    firststock = stocklist[0]
    challengers = [item for item in stocklist if item != firststock]
    if len(challengers) != 0:
        # retrieve stock graph data
        stockprices = grabsinglehistory(firststock)
        stockprices = fill_gaps2(stockprices, '', existdate)
        for challenger in challengers:
            # retrieve challenger graphdata
            chalprices = grabsinglehistory(challenger)
            chalprices = fill_gaps2(chalprices, '', existdate)
            # show graphs of stock and challenger side by side
            graphsidebyside(stockprices, chalprices, [firststock], [challenger], firststock, challenger)
            # ask whether stock or challenger is better
            choice = easygui.buttonbox('Which graph is better?', choices=[firststock, challenger, 'neither'])
            # if stock > challenger:
            if choice == firststock:
                chalgrade = f'below_{initialgrade}'
            # if stock < challenger:
            elif choice == challenger:
                chalgrade = f'above_{initialgrade}'
            # if stock == challenger:
            elif choice == 'neither':
                chalgrade = initialgrade
            # record change
            gradesheet.loc[gradesheet['stock'] == challenger, gradecolname] = chalgrade
    # sort above group
    abovegroup = gradesheet[gradesheet[gradecolname] == f'above_{initialgrade}']['stock'].tolist()
    abovegroupinitialgrade = initialgrade + len(abovegroup)
    # sort below group
    belowgroup = gradesheet[gradesheet[gradecolname] == f'below_{initialgrade}']['stock'].tolist()
    belowgroupinitialgrade = initialgrade - len(belowgroup)
    while len(abovegroup) > 0:
        gradesheet = gradesorter(gradesheet, abovegroup, abovegroupinitialgrade, existdate, gradecolname)
        abovegroup = gradesheet[gradesheet[gradecolname] == f'above_{abovegroupinitialgrade}']['stock'].tolist()
        abovegroupinitialgrade += len(abovegroup)
    while len(belowgroup) > 0:
        gradesheet = gradesorter(gradesheet, belowgroup, belowgroupinitialgrade, existdate, gradecolname)
        belowgroup = gradesheet[gradesheet[gradecolname] == f'below_{belowgroupinitialgrade}']['stock'].tolist()
        belowgroupinitialgrade = initialgrade - len(belowgroup)

    return gradesheet


# takes unsorted stocklist and sorts them by manual review; returns and saves dataframe of stocks and their grade
def graphgrader(stocklist, existdate, customfn, listdir, archivedir):
    gradecolname = f'grade_{existdate}'
    initialgrade = 0
    gradesheet = pd.DataFrame(data={'stock': stocklist, gradecolname: initialgrade})
    gradesheet = gradesorter(gradesheet, stocklist, 0, existdate, gradecolname)

    # sort and reset index of final gradesheet
    gradesheet.sort_values(ascending=False, by=[gradecolname], inplace=True)
    gradesheet.reset_index(drop=True, inplace=True)

    # archive gradesheet
    # make archive of old file if exists
    currentfilename = f'{customfn}_{existdate}'
    if os.path.exists(listdir / f"{currentfilename}.pkl") is True:
        # MAKE AN ARCHIVE OF ORIGINAL FILE
        timestamp = str(dt.datetime.now())
        timestamp = timestamp.replace(".", "_")
        timestamp = timestamp.replace(":", "")
        timestamp = timestamp.replace(" ", "_")
        archfilename = f'{currentfilename}_old_{timestamp}'
        # IF ARCHIVE FOLDER DOES NOT EXIST, CREATE:
        archivename = 'stockgrades_archive'
        archiveloc = archivedir / archivename
        create_nonexistent_folder(archiveloc)
        # MAKE ARCHIVE
        shutil.copy2(
            listdir / f"{currentfilename}.pkl",
            archiveloc / f"{archfilename}.pkl")
    savetopkl(currentfilename, listdir, gradesheet)
    print(gradesheet)


# takes an already created graphgraded dataframe and adds new stocks to the list
def addtogradesheet(gradesheetname, sheetdir, archivedir, newlist, existdate):
    gradecolname = f'grade_{existdate}'
    # load gradesheet
    gradesheet = readpkl(gradesheetname, sheetdir)
    # for each stock in newlist
    for newstock in newlist:
        currentlist = gradesheet['stock'].tolist()
        if newstock not in currentlist:
            # get newstock data
            newstockprices = grabsinglehistory(newstock)
            newstockprices = fill_gaps2(newstockprices, '', existdate)
            # for each graded stock
            for gradedstock in currentlist:
                # pull graded stock data
                gradedstockprices = grabsinglehistory(gradedstock)
                gradedstockprices = fill_gaps2(gradedstockprices, '', existdate)
                # show graphs of stock and challenger side by side
                graphsidebyside(newstockprices, gradedstockprices, [newstock], [gradedstock], newstock, gradedstock)
                # ask whether newstock or gradedstock is better
                choice = easygui.buttonbox('Which graph is better?', choices=[newstock, gradedstock, 'neither'])
                gradedstockgrade = gradesheet[gradesheet['stock'] == gradedstock][gradecolname].item()
                # if newstock > gradedstock:
                if choice == newstock:
                    newgrade = gradedstockgrade + 1
                    newrow = {'stock': newstock, gradecolname: newgrade}
                    gradesheet.append(newrow, ignore_index=True)
                    break
                # if newstock < gradedstock:
                elif choice == gradedstock:
                    if gradedstock != currentlist[-1]:
                        continue
                    else:
                        newgrade = gradedstockgrade - 1
                        newrow = {'stock': newstock, gradecolname: newgrade}
                        gradesheet.append(newrow, ignore_index=True)
                # if newstock == gradedstock:
                elif choice == 'neither':
                    newgrade = gradedstockgrade
                    newrow = {'stock': newstock, gradecolname: newgrade}
                    gradesheet.append(newrow, ignore_index=True)
                    break
            # resort and reindex gradesheet
            gradesheet.sort_values(ascending=False, by=[gradecolname], inplace=True)
            gradesheet.reset_index(drop=True, inplace=True)
        else:
            print(f'{newstock} is already graded.  Moving on to next candidate...')
            continue
    # archive gradesheet
    # make archive of old file if exists
    if os.path.exists(sheetdir / f"{gradesheetname}.pkl") is True:
        # MAKE AN ARCHIVE OF ORIGINAL FILE
        timestamp = str(dt.datetime.now())
        timestamp = timestamp.replace(".", "_")
        timestamp = timestamp.replace(":", "")
        timestamp = timestamp.replace(" ", "_")
        archfilename = f'{gradesheetname}_old_{timestamp}'
        # IF ARCHIVE FOLDER DOES NOT EXIST, CREATE:
        archivename = 'stockgrades_archive'
        archiveloc = archivedir / archivename
        create_nonexistent_folder(archiveloc)
        # MAKE ARCHIVE
        shutil.copy2(
            sheetdir / f"{gradesheetname}.pkl",
            archiveloc / f"{archfilename}.pkl")
    savetopkl(gradesheetname, sheetdir, gradesheet)
    print(gradesheet)
