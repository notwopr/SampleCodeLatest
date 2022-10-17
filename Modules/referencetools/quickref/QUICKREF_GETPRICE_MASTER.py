"""
Title: RETRIEVE PRICE OF A STOCK ON GIVEN DATE
Date Started: Dec 14, 2020
Version: 1.00
Version Start: Dec 14, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Retrieve price of stock on given date.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from QUICKREF_GETPRICE_BASE import getsingleprice


portfolio = ['HCTI'
    ]
date = '2014-05-06'
for stock in portfolio:
    print(getsingleprice(stock, date))
