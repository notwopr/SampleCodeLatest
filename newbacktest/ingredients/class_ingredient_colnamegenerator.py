class ColNameGenerator:

    def gen_colname(self, ingredient):
        exclusions = [
                'filterdirection',
                'threshold_bybestbench_better',
                'threshold_type',
                'threshold_buffer',
                'threshold_value',
                'filterby',
                'ranktype',
                'rankdirection',
                'weight']
        colnamelist = [f"{k}{v}|" for k, v in ingredient.items() if k not in exclusions]
        colnamelist.sort()
        return ''.join(colnamelist)
