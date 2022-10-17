"""
Title: Stock Pick Function Library
Date Started: August 7, 2019
Version: 1.1
Version Start Date: July 28, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Library of functions to manipulate stocklists.
VERSIONS:
1.1: Clean and update code.

"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import shutil
import os
import pickle as pkl
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import savetopkl, readpkl
from genericfunctionbot import removedupes


# Take stocklist, alphabetize, remove dupes, then checks if file already exists and cancels save if does
def save_stocklist(filename, directory, data):
    # IF FILE DOESN'T ALREADY EXIST...
    if os.path.exists(directory / f"{filename}.pkl") is False:
        # SORT LIST ALPHABETICALLY
        data.sort()
        # REMOVE DUPLICATES
        draftlist = removedupes(data)
        # WRITE NEW/OVERWRITE EXISTING FILE
        savetopkl(filename, directory, draftlist)
    else:
        print('The file you intend to write to already exists.  Please write the stocklist to a unique filename to save it.')


# Take stocklist, alphabetize, remove dupes, then overwrites existing file with same name and location
def overwrite_stocklist(filename, directory, data):
    # SORT LIST ALPHABETICALLY
    data.sort()
    # REMOVE DUPLICATES
    draftlist = removedupes(data)
    # WRITE NEW/OVERWRITE EXISTING FILE
    savetopkl(filename, directory, draftlist)


# takes list, saves a duplicate file as archive, renames file, saves new file
def renamestocklist(verbose, currentfilename, listdir, archivedir, newfilename):
    # IF ORIG FILE EXISTS:
    if os.path.exists(listdir / f"{currentfilename}.pkl") is True:
        # OPEN ORIG FILE
        data = readpkl(currentfilename, listdir)
        if verbose == "verbose":
            print(f"Original name:\n{currentfilename}")
            print(f"Original data:\n{data}")
        # CHECK TO SEE IF A FILE ALREADY EXISTS WITH NEW NAME
        if os.path.exists(listdir / f"{newfilename}.pkl") is True:
            print('File with that name already exists. Now exiting...')
        else:
            # SAVE ORIG FILE CONTENTS TO NEW FILENAME
            savetopkl(newfilename, listdir, data)
        # REOPEN NEW FILE AND REPORT CONTENTS
        data = readpkl(newfilename, listdir)
        if verbose == "verbose":
            print(f"New name:\n{newfilename}")
            print(f"New data (should be same as before):\n{data}")
        # create archive file name
        timestamp = str(dt.datetime.now())
        timestamp = timestamp.replace(".", "_")
        timestamp = timestamp.replace(":", "")
        timestamp = timestamp.replace(" ", "_")
        archfilename = f'{currentfilename}_{timestamp}'
        # MOVE CURRENT FILE TO ARCHIVE LOCATION
        shutil.move(
            listdir / f"{currentfilename}.pkl",
            archivedir / f"{archfilename}.pkl")
    else:
        print('Original file not found. Now exiting...')


# takes list, saves a duplicate file as archive, adds or removes item from list, saves new file
def addremove_stock(verbose, currentfilename, listdir, archivedir, candidate, action):
    # IF ORIG FILE EXISTS:
    if os.path.exists(listdir / f"{currentfilename}.pkl") is True:
        # MAKE AN ARCHIVE OF ORIGINAL FILE
        timestamp = str(dt.datetime.now())
        timestamp = timestamp.replace(".", "_")
        timestamp = timestamp.replace(":", "")
        timestamp = timestamp.replace(" ", "_")
        archfilename = f'{currentfilename}_old_{timestamp}'
        # MAKE ARCHIVE
        shutil.copy2(
            listdir / f"{currentfilename}.pkl",
            archivedir / f"{archfilename}.pkl")
        # OPEN ORIG FILE
        data = readpkl(currentfilename, listdir)
        if verbose == "verbose":
            print(f"Original list:\n{data}")
        # ADD/REMOVE MEMBER
        if action == "add":
            data.append(candidate)
        elif action == "remove":
            data.remove(candidate)
        if verbose == "verbose":
            print(f"Modified list:\n{data}")
        # OVERWRITE EXISTING FILE
        overwrite_stocklist(currentfilename, listdir, data)
    else:
        print('Original file not found. Cannot add or remove stocks to or from a nonexisting file.  Please find an existing file to add or remove stocks to or from.  Now exiting...')


# switch lists
def switchlist(verbose, destlistname, currentlistname, listdir, archivedir, candidate):
    # add to new list
    addremove_stock(verbose, destlistname, listdir, archivedir, candidate, 'add')
    # remove from old list
    addremove_stock(verbose, currentlistname, listdir, archivedir, candidate, 'remove')


# view list
def viewstocklist(listname, listdir):
    data = readpkl(listname, listdir)
    print(f"{listname}:\n{data}")
    return data


# construct csv library of currently saved portfolios
def constructportlib(sourcefolder, destfolder):
    alldata = []
    for child in sourcefolder.iterdir():
        with open(child, "rb") as targetfile:
            unpickled_raw = pkl.load(targetfile)
            portname = os.path.basename(child)[:-4]
        alldata.append({'PORTFOLIO NAME': portname, 'CONTENTS': unpickled_raw})
    # construct df
    portlibdf = pd.DataFrame(data=alldata)
    portlibdf['PORTFOLIO NAME'] = portlibdf['PORTFOLIO NAME'].str.lower()
    portlibdf.sort_values(ascending=True, by=['PORTFOLIO NAME'], inplace=True)
    portlibdf.reset_index(drop=True, inplace=True)
    # ARCHIVE TO FILE
    filename = "portfoliolibrary"
    portlibdf.to_csv(index=False, path_or_buf=destfolder / f"{filename}.csv")
    savetopkl(filename, destfolder, portlibdf)
