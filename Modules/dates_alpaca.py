"""
Title: Date functions using alpaca API
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
#   THIRD PARTY IMPORTS
import alpaca_trade_api as tradeapi
#   LOCAL APPLICATION IMPORTS


# returns the most recent trading day with respect to the input date
# if the input date is a trading day, it will return the input date
# return date as datetime object
# the way alpaca calendar works is that if you enter a nontrading day, it will return the first upcoming trading day.
def getmostrecenttradingdate(todaysdate):
    api = tradeapi.REST('PKF2XF4F056ZWUF3XBAG', 'VAhJMfNRmRYZMjvyQSd2K8xDlOmTrfC3ybNSoKuw', 'https://paper-api.alpaca.markets')
    mostrecenttradedate = dt.date.fromisoformat(todaysdate)
    tradedate = api.get_calendar(mostrecenttradedate, mostrecenttradedate)[0].date.date()
    while tradedate != mostrecenttradedate:
        mostrecenttradedate = mostrecenttradedate - dt.timedelta(days=1)
        tradedate = api.get_calendar(mostrecenttradedate, mostrecenttradedate)[0].date.date()
    return mostrecenttradedate
