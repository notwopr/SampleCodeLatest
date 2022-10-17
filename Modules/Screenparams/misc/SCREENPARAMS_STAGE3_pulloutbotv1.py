"""
Title: STAGE 3 - PULLOUT BOT
Date Started: Nov 20, 2020
Version: 1.00
Version Start Date: Nov 20, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.

"""
from computersettings import computerobject


# DEFINE STRUCTURE AND ORDER OF FILTERS AND LAYERS TO APPLY
filterinstructdict = [
    {
        'targetcol': 'Overall Pullout Pct',
        'comparecol': 'bydaypulloutpct_losers_max',
        'filtermeth': 'above'
    },
    {
        'targetcol': 'Difference (%)',
        'comparecol': 'bydaymargins_losers_max',
        'filtermeth': 'above'
    },
    {
        'targetcol': 'Gain/Loss Rate (%)',
        'comparecol': 'bydaygains_losers_max',
        'filtermeth': 'above'
    }
]



stage3_params = {
    'scriptname': 'pulloutbotv1',
    'benchticker': '^IXIC',
    'polibsource': computerobject.bot_important / 'PULLOUTBOT' / 'masterbydaystats.csv',
    'filterinstructdict': filterinstructdict,
    'testday': 15
}
