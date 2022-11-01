# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from file_hierarchy import DirPaths, FileNames
from newbacktest.abstractclasses.db_abstract_keyval import AbstractKeyValDatabase
from newbacktest.ingredients.db_ingredient_settings import IngredientSettingsDatabase
from newbacktest.ingredients.db_metricfunction import MetricFunctionDatabase
from type_checking import TypeChecker


class IngredientsDatabase(AbstractKeyValDatabase):
    '''
    When a Stage Recipe is proposed, each ingredient of that recipe is examined.  This database is searched to see whether that ingredient already exists.  If it doesnt exist, the proposed ingredient is validated.  If valid, a copy of that new ingredient is stored in this database.
    database structure = {
        code: Ingredientobject,
        code: Ingredientobject,
        ...
    }
    '''
    _emptydb = {}

    def __init__(self):
        self._dbname = "Ingredients Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_ingredient
        self._keyname_term = "igcode"
        self._item_term = "Ingredient"

    def _check_metricspecific_dependencies(self, itemdata):
        for argname in MetricFunctionDatabase().get_metricfuncargnames(itemdata['metricfunc']):
            if argname != 'seriesdata' and argname != 'invest_startdate' and not itemdata.get(argname, 0):
                raise ValueError(f'The metricfunc "{itemdata["metricfunc"]}" requires a "{argname}" parameter, but it is not found in the ingredient settings dict.\nOffending ingredient:\n{itemdata}')

    def _check_ingredient_dependencies(self, itemdata):
        allkeys = set(itemdata.keys())
        # check for missing required settings
        check = IngredientSettingsDatabase().required.difference(allkeys)
        if check:
            raise ValueError(f"The following required ingredient settings are missing from your proposed ingredient: '{check}'. \nOffending ingredient settings\n{itemdata}")
        # rank settings
        check = ['ranktype' in allkeys, 'rankdirection' in allkeys]
        if any(check) and not all(check):
            raise ValueError(f"The 'ranktype' and 'rankdirection' settings must both be present in an ingredient if one of them is.\nOffending ingredient settings\n{itemdata}")
        # filterby presence
        check = [{s for s in allkeys if s.startswith('threshold')}, 'filterby' not in allkeys]
        if all(check):
            raise ValueError(f"'threshold' settings were found.  They require the presence of a 'filterby' setting, but that is missing.\nOffending ingredient settings\n{itemdata}")
        # filter direction and filterby are always together
        check = ['filterby' in allkeys, 'filterdirection' in allkeys]
        if any(check) and not all(check):
            raise ValueError(f"The 'filterby' and 'filterdirection' settings must both be present in an ingredient if one of them is.\nOffending ingredient settings\n{itemdata}")
        # if threshold type byvalue or byticker threshold_value must be present
        check = ['threshold_type' in allkeys, any([itemdata.get('threshold_type', 0) == 'byvalue', itemdata.get('threshold_type', 0) == 'byticker']), 'threshold_value' not in allkeys]
        if all(check):
            raise ValueError(f"If the 'threshold_type' setting is set to 'byvalue' or 'byticker', a 'threshold_value' setting must be present, but none was found.\nOffending ingredient settings\n{itemdata}")
        # check threshold_bybestbench_better presence
        check = [itemdata.get('threshold_type', 0) == 'bybestbench', not itemdata.get('threshold_bybestbench_better', 0)]
        if all(check):
            raise ValueError(f"'threshold_type' setting is set to 'bybestbench' but is missing 'threshold_bybestbench_better' setting.\nOffending ingredient settings\n{itemdata}")
        # rank and filter dont mix
        check = ['ranktype' in allkeys, 'filterby' in allkeys]
        if all(check):
            raise ValueError(f"An ingredient cannot possess both filtering and ranking settings.  You must choose one or the other.\nOffending ingredient settings\n{itemdata}")
        if not any(check):
            raise ValueError(f"The proposed ingredient settings do not contain any ranking or filtering types.  It must contain settings of one type but not both.\nOffending ingredient settings\n{itemdata}")
        # check if weight setting present for sorter, and not present for filter.
        check = [all(['weight' in allkeys, 'ranktype' not in allkeys]), all(['weight' in allkeys, 'filterby' in allkeys])]
        if any(check):
            raise ValueError(f"A weight setting was found, but this is not a sorter ingredient.  This is a filter ingredient because (1) it does not contain rank settings and (2) it contains filter settings.  Either (a) remove the weight setting or (b) remove all filter-related settings and add required rank settings.\nOffending ingredient settings\n{itemdata}")
        check = [all(['weight' not in allkeys, 'ranktype' in allkeys]), all(['weight' not in allkeys, 'filterby' not in allkeys])]
        if any(check):
            raise ValueError(f"A weight was not found, but this is a sorter ingredient.  A weight setting is required for sorter ingredients.  This ingredient is a sorter ingredient because (1) it contains rank settings and (2) does not contain filter settings.  Either (a) remove the weight setting and all rank-related settings and add required filter settings or (b) add the required weight setting.\nOffending ingredient settings\n{itemdata}")
        self._check_metricspecific_dependencies(itemdata)
        print("All Ingredient settings dependencies tests passed.")

    def _check_item_integrity(self, itemdata):
        # check whether it is a dict
        TypeChecker().is_valid(itemdata, 'dict')
        # check each ingredient setting (key-val pair)
        for k, v in itemdata.items():
            # check whether setting is in settings database
            idb = IngredientSettingsDatabase()
            if not idb.igsdb.get(k, 0):
                raise ValueError(f"The setting '{k}' is not a part of the ingredient settings database.\nOffending ingredient settings\n{itemdata}")
            # check setting's value data type
            TypeChecker().is_valid(v, idb.igsdb[k]['vtype'])
            # check setting's value validity
            idb.is_value_valid(k, v)
        print("Ingredient settings integrity test passed.")
        self._check_ingredient_dependencies(itemdata)

    def _verify_item(self, item):
        self._check_item_integrity(item.itemdata)

    def _prep_item(self, item):
        pass
