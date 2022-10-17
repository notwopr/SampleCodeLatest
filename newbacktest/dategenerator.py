# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
from pathlib import Path
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from file_functions import readpkl_fullpath, join_str
from file_hierarchy import DirPaths, FileNames
from Modules.dates import DateOperations

daterangedb_source = Path(join_str([DirPaths().date_results, f"{FileNames().fn_daterangedb}.pkl"]))


class DateGenerator:

    # RANDOMLY GENERATE UNIQUE DATES
    def random_dates(self, start, end, n):
        # GET LIST OF ALL DATES BETWEEN START AND END
        dr = pd.date_range(start, end, freq='D')
        # CHECK IF AMOUNT REQUESTED EXCEEDS AVAILABLE AMOUNT
        if n > len(dr):
            raise ValueError(f"The number of random dates requested {n} exceeds the number of possible dates {len(dr)}.")
        # GET LIST OF THE DATE LIST INDICES
        a = np.arange(len(dr))
        # SHUFFLE THE INDEX LIST, RETURN THE FIRST N SAMPLES, SORT THE SAMPLE LIST
        b = np.sort(np.random.permutation(a)[:n])
        # RETRIEVE EACH DATE AND CHANGE TO ISOFORMAT
        answer = [str(date)[:10] for date in dr[b]]
        return answer

    # GET LATEST OR EARLIEST DATE AVAILABLE GIVEN DATE SOURCE
    def getfirstorlastdate(self, boundtype):
        daterangedb = readpkl_fullpath(daterangedb_source)
        if boundtype == 'earliest':
            answerdate = daterangedb['first_date'].apply(lambda x: dt.date.fromisoformat(x)).min()
        elif boundtype == 'latest':
            answerdate = daterangedb['last_date'].apply(lambda x: dt.date.fromisoformat(x)).max()
        return str(answerdate)

    # RETURN LAST POSSIBLE DATE GIVEN periodlen AND LATESTDATE IF GIVEN
    def getlastpossible_selectend(self, periodlen, latestdate):
        if latestdate == '':
            # get latest possible available date
            latestdate = self.getfirstorlastdate('latest')
        last_possible_selectend = str(dt.date.fromisoformat(latestdate) - dt.timedelta(days=periodlen))
        return last_possible_selectend

    # RETURN N RANDOM EXIST DATES GIVEN periodlen AND LATESTDATE IF GIVEN
    def getrandomexistdate_multiple(self, numdates, periodlen, earliestbound, latestbound):
        latestpossiblerandomdate = self.getlastpossible_selectend(periodlen, latestbound)
        if earliestbound == '':
            earliestbound = self.getfirstorlastdate('earliest')
        randomexistdates = self.random_dates(earliestbound, latestpossiblerandomdate, numdates)
        return randomexistdates

    def getevenlyspaced_dates(self, numdates, periodlen, startdate):
        '''given starting date, return a list of evenly spaced dates including the startdate, given number of dates you want returned and the size of the period'''
        alldates = [DateOperations().plusminusdays(startdate, i*periodlen) for i in range(numdates)]
        return alldates

    def getevenlyspaced_dates_randomset(self, numdates, periodlen, earliestbound, latestbound):
        latestpossiblestartdate = self.getlastpossible_selectend(numdates*periodlen, latestbound)
        random_startdate = self.random_dates(earliestbound, latestpossiblestartdate, 1)[0]
        return self.getevenlyspaced_dates(numdates, periodlen, random_startdate)

    def get_alltrialstartdates(self, num_trials, num_periods, periodlen, earliest_date, latest_date):
        '''system gets N randomized trial cloudsample startdates. A cloud sample encompasses X periods, each Y days long, for a total length of X*Y, so the random start dates generated cannot be such that the X*Yth date is later than the last available date in the datasource'''
        latestpossiblestartdate = self.getlastpossible_selectend(num_periods*periodlen, latest_date)
        alltrialstartdates = self.random_dates(earliest_date, latestpossiblestartdate, num_trials)
        return alltrialstartdates
