'''
PURPOSE: BANK OF RANDOM CODE SNIPPETS THAT MAY BE USEFUL.
'''
# FILL IN DATE GAPS OF A DATAFRAME WITHOUT CHANGING ITS FORM. NON-DATE COLUMNS ARE FILLED IN WITH NAN
'''
newdateindex = pd.date_range(start=mdf['date'].min(), end=mdf['date'].max())
mdf = mdf.set_index('date').reindex(newdateindex, method='ffill').rename_axis('date').reset_index()
'''
