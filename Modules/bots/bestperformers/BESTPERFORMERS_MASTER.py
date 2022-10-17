"""
Title: Best Performers Masterscript
Date Started: Dec 7, 2019
Version: 2.0
Version Start Date: Sept 23, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Find best stocks by overall growth for a given period.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from BESTPERFORMERS_BASE import bestperformer_cruncher

configdict = {
    # HYPOTHETICAL INVESTMENT PERIOD (HIP)
    'beg_date': '2016-10-29',
    'end_date': '2021-10-29',
    # DO YOU WANT TO COMPARE THE RESULTS TO BENCHMARKS?
    'benchmarks': 'yes',
    # DO YOU WANT TO SAVE YOUR RESULTS?
    'saveresults': 'yes',
    # DO YOU WANT TO SEE THE GROWTH RATES IN ANNUALIZED TERMS?
    'annualized': 'yes',
    # DO YOU ONLY WANT TO INCLUDE THOSE THAT BEAT THE BEST PERFORMING INDEX?
    'marketbeatersonly': 'yes',
    # DO YOU WANT TO ONLY INCLUDE THOSE THAT BEAT THE BEST PERFORMING INDEX BY A CERTAIN MARGIN? (marginal rate over the annualized best benchmark rate)
    'marginrate': 0.15,
    # REMOVE THOSE WHOSE HIP RAW BAREMAX FATSCORE EXCEED
    'fatscorecap_hip': 0.16,
    # REMOVE THOSE WHOSE HIP MAXDD EXCEED
    'maxddcap_hip': -.50,
    # REMOVE THOSE WHOSE LIFETIME RAW BAREMAX FATSCORE EXCEED
    'fatscorecap_life': 0.18,
    # REMOVE THOSE WHOSE LIFETIME MAXDD EXCEED
    'maxddcap_life': -.63,
    # FILTER BY HIP GROWTH / LIFE FATSCORE RATIO
    'hipgrolifefatcap': 100
}

if __name__ == '__main__':
    bestperformer_cruncher(configdict)
