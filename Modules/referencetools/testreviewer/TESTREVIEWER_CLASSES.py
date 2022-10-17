"""
Title: TESTREVIEWER - RANKVIEWER
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
from pathlib import Path
#   LOCAL APPLICATION IMPORTS
from computersettings import BOT_DUMP
from filelocations import readpkl


class TestMethodCandidate():

    def __init__(self, methodname, testfolder, testcode, trial):
        self.methodname = methodname
        self.testfolder = testfolder
        self.testcode = testcode
        self.trial = trial
        if self.methodname == 'sighit':
            self.fileloc = BOT_DUMP / 'sighit' / 'ranks'
        elif self.methodname == 'posnegcompare':
            self.fileloc = BOT_DUMP / self.testfolder / self.testcode / 'ranks'
        else:
            self.fileloc = BOT_DUMP / 'backtest_dump' / self.testfolder / self.testcode / 'trial_{}'.format(self.trial) / 'selper_1' / 'ranks'
        for child in self.fileloc.iterdir():
            if str(child).find('.pkl') != -1:
                self.filename = Path(child).stem
        if self.methodname == 'smooth':
            self.end_date = '2018-09-22'
        else:
            self.end_date = self.filename[-10:]

    def rankingfile(self):
        filedf = readpkl(self.filename, self.fileloc)
        return filedf

    def rankcolname(self):
        if self.methodname == 'postonegstandard':
            return 'RANK_posnegindex as of {} (w=1.0, vp_mod=mean)'.format(self.end_date)
        if self.methodname == 'postonegcomposite':
            return 'RANK_posnegindex as of {} (vp_mod=mean)'.format(self.end_date)
        if self.methodname == 'postonegsmooth':
            return 'FINAL RANK'
        if self.methodname == 'spanranker':
            return 'FINAL RANK as of {}'.format(self.end_date)
        if self.methodname == 'smooth':
            return 'FINAL RANK'
