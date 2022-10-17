"""
Title: Dates functions.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS


class DateOperations:

    def num_days(self, beg_date, end_date):
        '''RETURNS INTEGER DIFFERENCE IN DAYS BETWEEN datetime object DATES'''
        return (end_date - beg_date).days

    def num_days_string(self, beg_date, end_date):
        '''RETURNS INTEGER DIFFERENCE IN DAYS BETWEEN TWO STRING DATES'''
        return self.num_days(dt.date.fromisoformat(beg_date), dt.date.fromisoformat(end_date))

    def plusminusdays(self, date, integer):
        '''RETURN STRING DATE GIVEN DATE MINUS/PLUS SOME INTEGER
        you may use negative integers to subtract days
        '''
        return str(dt.date.fromisoformat(date) + dt.timedelta(days=integer))
