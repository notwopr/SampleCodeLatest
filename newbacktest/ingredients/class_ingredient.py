from newbacktest.ingredients.db_ingredient_settings import IngredientSettingsDatabase
from newbacktest.ingredients.db_metricfunction import MetricFunctionDatabase
from newbacktest.symbology.symbology import Symbology
from newbacktest.abstractclasses.class_abstract_dbitem import AbstractDatabaseItem
from newbacktest.ingredients.class_ingredient_colnamegenerator import ColNameGenerator


class Ingredient(AbstractDatabaseItem):
    '''
    ingredient_setting_sample = {
            'threshold_bybestbench_better': 'bigger',
            'metricfunc': 'getpctchange_single',
            'filterdirection': '>',
            'sourcedata': 'eodprices',
            'threshold_type': 'bybestbench',
            'filterby': 'value',
            'look_back': 0,
            'focuscol': 'rawprice',
            'threshold_buffer': 0
        }
    '''
    _item_term = "Ingredient"

    def __init__(self, itemdata, nickname=None, description=None):
        self._nickname = nickname
        self._description = description
        self._itemdata = itemdata
        self._itemcode = self._set_itemcode()
        self._itemtype = self._set_itemtype()
        self._colname = self._set_colname()
        self._creationdate = self._set_creationdate()

    def _set_itemcode_helper(self, k, v):
        setting_type_id = IngredientSettingsDatabase().igsdb[k]["id"]
        setting_value = MetricFunctionDatabase().view_item(v)[0] if k == "metricfunc" else v
        return f'{Symbology().igcode_type_pred}{setting_type_id}{Symbology().igcode_value_pred}{setting_value}'

    def _set_itemcode(self):
        igcodelist = [self._set_itemcode_helper(k, v) for k, v in self.itemdata.items()]
        igcodelist.sort()
        itemcode = f'{Symbology().igcode_pred}{"".join(igcodelist)}'
        print(f"{self._item_term} item code set to '{itemcode}'.")
        return itemcode

    def _set_colname(self):
        # exclusions = [
        #         'filterdirection',
        #         'threshold_bybestbench_better',
        #         'threshold_type',
        #         'threshold_buffer',
        #         'threshold_value',
        #         'filterby',
        #         'ranktype',
        #         'rankdirection',
        #         'weight']
        # colnamelist = [f"{k}{v}|" for k, v in self.itemdata.items() if k not in exclusions]
        # colnamelist.sort()
        # colname = ''.join(colnamelist)
        colname = ColNameGenerator().gen_colname(self.itemdata)
        print(f"{self._item_term} colname set to '{colname}'.")
        return colname

    @property
    def colname(self):
        return self._colname

    def _set_itemtype(self):
        allkeys = set(self.itemdata.keys())
        if 'ranktype' in allkeys:
            itemtype = 'sorter'
        elif 'filterby' in allkeys:
            itemtype = 'filter'
        print(f"Ingredient type set to '{itemtype}'.")
        return itemtype
