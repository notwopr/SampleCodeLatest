from file_hierarchy import DirPaths, FileNames
from newbacktest.abstractclasses.db_abstract_keyval import AbstractKeyValDatabase
from newbacktest.ingredients.db_ingredient import IngredientsDatabase


class StageRecipeDatabase(AbstractKeyValDatabase):
    '''
    When a Stage Recipe is proposed, this database is searched by srcode to see whether it already exists.  If it doesnt exist, the stagerecipe is added.
    A stage recipe's main data consists of a list of igcodes that point to actual ingredients and their settings.  The recipe itself doesnt contain the ingredient data.
    database structure = {
            srcode: <stagerecipeobject>,
            srcode: <stagerecipeobject>,
            ...
        }
    <stagerecipeobject>.itemdata = <list of ingredient codes>
    '''
    _emptydb = {}

    def __init__(self):
        self._dbname = "Stage Recipe Database"
        self._parentdirpathstring = DirPaths().dbparent
        self._dbfilenamestring = FileNames().fn_db_stagerecipe
        self._keyname_term = "srcode"
        self._item_term = "Stage Recipe"

    def _check_ranktype(self, ranktype, settings):
        if not ranktype:
            ranktype = settings['ranktype']
        elif ranktype != settings['ranktype']:
            raise ValueError(f"The previous ingredient in the list had a ranktype of '{ranktype}' but the next ingredient is set to '{settings['ranktype']}' rank. All ingredients in a {self._item_term} must be of the same ranktype.\nOffending ingredient:\n{settings}")
        return ranktype

    def _check_weights(self, weight_total):
        if weight_total != 1:
            raise ValueError(f"{self._item_term} ingredient weights should total 1.  Instead, they total {weight_total}.")

    def _verify_item(self, item):
        ranktype = None
        weight_total = 0
        for igcode in item.itemdata:
            ig = IngredientsDatabase().view_item(igcode)
            ranktype = self._check_ranktype(ranktype, ig.itemdata) if ig.itemdata.get('ranktype', 0) else None
            weight_total += ig.itemdata.get('weight', 0)
        if item.itemtype != 'filter':
            self._check_weights(weight_total)
        print(f"{self._item_term} successfully verified.")

    def _prep_item(self, item):
        pass
