"""
Title: Recession Detector Bot
Version: 1.0
Date Started: Dec 4, 2019
Version Date: Dec 4, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Chart that returns all possible date comparisons of a single stock, and returns the percent change.  This is useful in finding the dates of the greatest changes.


"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory as gsh
from fillgapbot import fill_gaps


def drop_chart(verbose, destfolder, stock):

    # GET FULL PRICE HISTORY OF STOCK
    prices = gsh(stock)

    # FILL IN GAPS
    prices = fill_gaps(prices)
    if verbose == 'verbose':
        print('FULL PRICE HISTORY OF STOCK:')
        print(prices)
        print('\n')

    # GET LENGTH OF PRICE HISTORY
    num_entries = len(prices)
    if verbose == 'verbose':
        print('NUMBER OF ENTRIES IN PRICE HISTORY:', num_entries)
        print('\n')

    # GET INDEX LIST OF PRICE HISTORY
    index_list = list(range(num_entries))
    if verbose == 'verbose':
        print('INDEX LIST OF PRICE HISTORY:')
        print(index_list)
        print('\n')

    # GET INDEX LIST OF FIRST DATE FOR ALL DATE PAIRS
    first_dates = index_list[:-1]
    if verbose == 'verbose':
        print('INDEX LIST OF FIRST DATE IN DATE PAIRS:')
        print(first_dates)
        print('\n')

    # GET INDEX PAIRS FOR ALL DATE PAIRS IN PRICE HISTORY
    all_index_pairs = [[x, x + (j + 1)] for x in first_dates for j in range(first_dates[-1] - x)]
    if verbose == 'verbose':
        print('LIST OF INDEX PAIRS FOR ALL DATE PAIRS IN PRICE HISTORY:')
        print(all_index_pairs)
        print('\n')

    # GET FIRST DATE INFO
    all_row_summaries = []
    for pair in all_index_pairs:
        first_date = prices.loc[pair[0], '___Date___']
        second_date = prices.loc[pair[1], '___Date___']
        time_span = (second_date - first_date).days
        first_price = prices.loc[pair[0], stock]
        second_price = prices.loc[pair[1], stock]
        change_in_price = second_price - first_price
        change_pct = (change_in_price / first_price) * 100
        row_summary = {'FIRST_DATE': first_date, 'SECOND_DATE': second_date, 'TIME_SPAN (DAYS)': time_span, 'FIRST_PRICE': first_price, 'SECOND_PRICE': second_price, 'PRICE_CHANGE': change_in_price, 'PCT_CHANGE (OVER FIRST_PRICE)': change_pct}
        all_row_summaries.append(row_summary)

    # ASSEMBLE DATAFRAME
    masterdf = pd.DataFrame(data=all_row_summaries, columns=['TIME_SPAN (DAYS)', 'PCT_CHANGE (OVER FIRST_PRICE)', 'PRICE_CHANGE', 'FIRST_PRICE', 'SECOND_PRICE', 'FIRST_DATE', 'SECOND_DATE'])

    # SAVE TO FILE
    filename = 'all_price_diffs_' + stock
    masterdf.to_csv(index=False, path_or_buf=destfolder / "{}.csv".format(filename))
