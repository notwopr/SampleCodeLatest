"""
Title: Recession Bot
Date Started: Oct 11, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Find stocks that go up during recession.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS

#   THIRD PARTY IMPORTS

#   LOCAL APPLICATION IMPORTS
# FIND DATES OF RECESSIONS
# search benchmark price history for drops in price
target_loss_1day = 0.50
target_loss_1mo = 0.50
# PROBLEM: DIFFERENT PERIODS HAVE DIFFERENT DROP MAGNITUDES.
# USE A ROLLING WINDOW CALCULATION THAT CALCULATES THE DIFFERENCE FROM END TO START IN NORMALIZED PRICE CHANGES.
max_win_len = 365*3
min_win_len = 60
# FOR EACH WINDOW CALC, ASK IF THE DROP IS NEGATIVE, IF SO, THEN CALCULATE HOW MUCH. STORE THE FOLLOWING: DATES, DROP AMOUNT, WINDOW SIZE.

# THEN SORT LIST BY DROP AMOUNT
# SEARCH FOR STOCKS WHERE GROWTH WAS POSITIVE DURING THESE PERIODS.
recession_periods = []
