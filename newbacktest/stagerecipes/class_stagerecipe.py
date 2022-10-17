from newbacktest.symbology.symbology import Symbology
from newbacktest.ingredients.class_ingredient import Ingredient
from newbacktest.ingredients.db_ingredient import IngredientsDatabase
from newbacktest.abstractclasses.class_abstract_dbitem import AbstractDatabaseItem


class StageRecipe(AbstractDatabaseItem):
    '''
    A StageRecipe is a collection of ingredients.  It doesn't actually store the ingredient data, but rather a list of their corresponding codes.  When it comes time to actually use the recipe, the codes are used to search the Ingredients Database for the actual ingredient data.
    itemdata = [
            {<igcode>},
            {<igcode>},
            ...
        ]
    '''
    _item_term = "Stage Recipe"

    def __init__(self, itemdata, nickname=None, description=None):
        self._nickname = nickname
        self._description = description
        self._itemdata = self._set_itemdata(itemdata)
        self._itemtype = self._set_itemtype()
        self._itemcode = self._set_itemcode()
        self._creationdate = self._set_creationdate()

    def _set_itemdata(self, itemdata):
        igcodelist = []
        for ingredient in itemdata:
            tig = Ingredient(ingredient)
            IngredientsDatabase().add_item(tig)
            igcodelist.append(tig.itemcode)
        igcodelist.sort()
        print(f"{self._item_term} data set to {igcodelist}.")
        return igcodelist

    def _check_itemtype(self, srtype, igtype, settings):
        if not srtype:
            srtype = igtype
        elif srtype != igtype:
            raise ValueError(f"The previous ingredient in the list is a '{srtype}' but the next ingredient is a '{igtype}'. All ingredients in a stage recipe must be of the same type. Either remove the offending ingredient from the stage recipe or remove all '{srtype}' ingredients from the recipe. \nOffending ingredient:\n{settings}")
        return srtype

    def _set_itemtype(self):
        srtype = None
        for igcode in self.itemdata:
            ig = IngredientsDatabase().view_item(igcode)
            srtype = self._check_itemtype(srtype, ig.itemtype, ig.itemdata)
        print(f"{self._item_term} type set to '{srtype}'.")
        return srtype

    def _set_itemcode(self):
        stagecode = ''.join(self.itemdata)
        itemcode = f'{Symbology().srcode_pred}{self.itemtype[:1].lower()}{stagecode}'
        print(f"{self._item_term} code set to {itemcode}.")
        return itemcode

    @property
    def ingredientlist(self):
        return [IngredientsDatabase().view_item(i).itemdata for i in self.itemdata]
