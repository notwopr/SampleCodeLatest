# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from newbacktest.symbology.symbology import Symbology
from newbacktest.stagerecipes.db_stagerecipe import StageRecipeDatabase
from newbacktest.stagerecipes.class_stagerecipe import StageRecipe
from newbacktest.abstractclasses.class_abstract_dbitem import AbstractDatabaseItem


class Strategy(AbstractDatabaseItem):
    '''
    input form (ordered list of stage recipes):
    [
        [
            {ingredient settings},
            {ingredient settings},
            ...
        ],
        [
            ...
        ],
        ...
    ]

    self._itemdata = {
        0: <srcode>,
        1: <srcode>,
        2: <srcode>,
        ...
    }
    '''
    _item_term = "Strategy"

    def __init__(self, itemdata, nickname=None, description=None):
        self._nickname = nickname
        self._description = description
        self._itemdata = self._set_itemdata(itemdata)
        self._itemcode = self._set_itemcode()
        self._creationdate = self._set_creationdate()

    @property
    def strategy_ingredients(self):
        return {f'STAGE {i}': StageRecipeDatabase().view_item(srcode).ingredientlist for i, srcode in self.itemdata.items()}

    def _set_itemdata_helper(self, stagerecipe):
        s = StageRecipe(stagerecipe)
        StageRecipeDatabase().add_item(s)
        return s.itemcode

    def _set_itemdata(self, itemdata):
        strategy = {i: self._set_itemdata_helper(stagerecipe) for i, stagerecipe in enumerate(itemdata)}
        print(f'Strategy Data set to {strategy}.')
        return strategy

    def _set_itemcode(self):
        srcodelist = [f'{Symbology().sr_divider}{k}{v}' for k, v in self.itemdata.items()]
        stratcode = ''.join(srcodelist)
        itemcode = f'{Symbology().stratcode_pred}{stratcode}'
        print(f"Strategy code set to '{itemcode}'.")
        return itemcode
