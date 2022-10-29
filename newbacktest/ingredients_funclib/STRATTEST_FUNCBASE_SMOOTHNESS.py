"""
Title: Layercake - Function Database - Smoothness Functions
Date Started: Feb 13, 2021
Version: 1.00
Version Start Date: Feb 13, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Most of the functions that relate to smoothness.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS


def accretionbooleanresults(accret_type, seriesdata):
    '''# return datadf with accretion boolean results'''
    if accret_type == 'pos':
        return seriesdata > seriesdata.shift(1)
    elif accret_type == 'neg':
        return seriesdata < seriesdata.shift(1)
    elif accret_type == 'zero':
        return seriesdata == seriesdata.shift(1)


def accretionscore_single(accret_type, seriesdata):
    '''# check if each successive data point is greater than the previous'''
    accretiontally = accretionbooleanresults(accret_type, seriesdata)
    return accretiontally.iloc[1:].mean()


'''UNREVISED CODE'''


# check if slope is positive
def positiveslope_single(datadf, focuscol):
    firstdatapoint = datadf.iloc[0][focuscol]
    lastdatapoint = datadf.iloc[-1][focuscol]
    positiveslope = lastdatapoint - firstdatapoint
    return positiveslope


# keeps running tally of next datapoint > previous data point.  if less than, subtract from total score.
def accretiontally_single(datadf, focuscol, accret_type):
    datadf = accretionbooleanresults(datadf, focuscol, accret_type)
    datadf[f'{focuscol}_{accret_type}_tally'] = datadf[f'{focuscol}_{accret_type}'].apply(lambda x: 1 if x is True else -1)
    accretiontallyscore = datadf[f'{focuscol}_{accret_type}_tally'][1:].sum() / (len(datadf)-1)
    return accretiontallyscore
