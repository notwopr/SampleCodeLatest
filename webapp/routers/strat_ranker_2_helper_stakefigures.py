from Modules.numbers import twodecp
from Modules.numbers_formulas import func_ending_principal


class StakeFigures:
    def add_stakefigures(self, stake, stakeperiod, bdf):
        bdf[
            'Ending Cash ($)'
            ] = bdf[
                'growthrate_effectivedaily'
                ].apply(lambda x: twodecp(func_ending_principal(stake, x, stakeperiod)))
        bdf[
            'Ending Cash (Benchmark) ($)'
            ] = bdf[
                'growthrate_effectivedaily_bestbench'
                ].apply(lambda x: twodecp(func_ending_principal(stake, x, stakeperiod)))
        bdf[
            'Ending Cash over Benchmark ($)'
            ] = bdf['Ending Cash ($)']-bdf['Ending Cash (Benchmark) ($)']
        bdf[
            'Amount Earned ($)'
            ] = bdf[
                'Ending Cash ($)'
                ]-stake
        bdf[
            'Amount Earned (Benchmark) ($)'
            ] = bdf[
                'Ending Cash (Benchmark) ($)'
                ]-stake
        bdf[
            'Amount Earned over Benchmark ($)'
            ] = bdf['Amount Earned ($)']-bdf['Amount Earned (Benchmark) ($)']
        bdf[
            'Overall Growth'
            ] = bdf[
                'Amount Earned ($)'
                ]/stake
        bdf[
            'Overall Growth (Benchmark)'
            ] = bdf[
                'Amount Earned (Benchmark) ($)'
                ]/stake
        bdf[
            'Overall Growth over Benchmark'
            ] = bdf['Overall Growth']-bdf['Overall Growth (Benchmark)']
        bdf[
            'Earned per Day ($)'
            ] = bdf[
                'Amount Earned ($)'
                ]/stakeperiod
        bdf[
            'Earned per Day (Benchmark) ($)'
            ] = bdf[
                'Amount Earned (Benchmark) ($)'
                ]/stakeperiod
        bdf[
            'Earned per Day over Benchmark ($)'
            ] = bdf['Earned per Day ($)']-bdf['Earned per Day (Benchmark) ($)']
