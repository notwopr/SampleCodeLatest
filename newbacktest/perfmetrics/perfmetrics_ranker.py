'''
Ranker takes a ranking schema and the perfmetricdatabase dataframe and returns the dataframe in ranked form
'''
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.ingredients.db_ingredient_settings import IngredientSettingsDatabase
from newbacktest.perfmetrics.perfmetrics_perfprofileupdater import PerfProfileUpdater


class PerfMetricRanker:

    def _percentile_rankdir_correction(self, irankdir, iranktype):
        '''rankdir_choices is either ['a' or 'd']'''
        '''
        if i want values to be descending, then i want bigger values to have the better ranking.  So, then in percentile rank, the biggest value should be labeled 1.  Percentile rank of a value is the percent of the data that is <= to that value.  This ranking is in ascending percentile order.  Thus, when I say I want values to be ranked in descending order, if I want the ranking to be represented in percentile, then the rank order needs to be ascending.
        I want percentile 1 to represent the best rank.
        if a and ordinal, then a or 0
        if a and percentile, then d or 1
        if d and ordinal, then d or 1
        if d and percentile, then a or 0
        '''
        rankdir_choices = IngredientSettingsDatabase().igsdb['rankdirection']['vlimit_details']
        rankdir_choice_index = not any([all([irankdir == 'a', iranktype == 'ordinal']), all([irankdir == 'd', iranktype == 'percentile'])])
        return 'a' == rankdir_choices[rankdir_choice_index]

    def _rank_df(self, df, rankschema):
        w_total = 0
        sumcols = []
        for k in rankschema.keys():
            s = rankschema[k]
            r = f'RANK_{k} (w={s["weight"]})'
            rankdir = self._percentile_rankdir_correction(s['rankdirection'], s['ranktype'])
            df[r] = df[k].rank(ascending=rankdir, pct=s['ranktype'] == 'percentile')
            df[f'w_{k}'] = (df[r] * s['weight'])
            w_total += s['weight']
            sumcols.append(f'w_{k}')
        m = f'wRANK {w_total}'
        df[m] = df[sumcols].sum(axis=1, numeric_only=True)#, min_count=len(sumcols))
        f = 'FINAL RANK'
        df[f] = df[m].rank(ascending=s['ranktype'] != 'percentile')
        df.sort_values(ascending=True, by=[f], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def gen_rankdf(self, rankschema):
        perfmetricdf = PerfProfileUpdater().get_samplesdf()
        '''aggregate by stratipcode'''
        groupedbystratipdf = perfmetricdf.groupby(by=["stratipcode"], dropna=False, as_index=False).mean(numeric_only=True)
        '''populate rank cols'''
        rankdf = self._rank_df(groupedbystratipdf, rankschema)
        return rankdf

    def gen_rankdf_addperfmetricdf(self, perfmetricdf, rankschema):
        '''aggregate by stratipcode'''
        groupedbystratipdf = perfmetricdf.groupby(by=["stratipcode"], dropna=False, as_index=False).mean(numeric_only=True)
        '''populate rank cols'''
        rankdf = self._rank_df(groupedbystratipdf, rankschema)
        return rankdf
