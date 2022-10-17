from newbacktest.symbology.symbology import Symbology
from newbacktest.ingredients.class_ingredient import Ingredient
from newbacktest.ingredients.db_ingredient import IngredientsDatabase
from newbacktest.abstractclasses.class_abstract_dbitem import AbstractDatabaseItem


class WinLoseProfile(AbstractDatabaseItem):
    '''
    A WinLoseProfile is a collection of ingredients.  It doesn't actually store the ingredient data, but rather a list of their corresponding codes.  It is identical to a Stage Recipe except for the fact that stage recipes can come in two types: sorters and filters, whereas a WinLoseProfile is solely one type: filter.  When it comes time to actually use the profile, the codes are used to search the Ingredients Database for the actual ingredient data.
    itemdata = [
            {<igcode>},
            {<igcode>},
            ...
        ]
    '''
    _item_term = "Win Lose Profile"

    def __init__(self, itemdata, periodlen, nickname=None, description=None):
        self._nickname = nickname
        self._description = description
        self._periodlen = periodlen
        self._itemdata = self._set_itemdata(itemdata)
        self._itemcode = self._set_itemcode()
        self._creationdate = self._set_creationdate()

    @property
    def periodlen(self):
        return self._periodlen

    def _set_itemdata(self, itemdata):
        '''check each ingredient, check ingredient type, store igcode'''
        wlproftype = 'filter'
        igcodelist = []
        for ingredient in itemdata:
            tig = Ingredient(ingredient)
            IngredientsDatabase().add_item(tig)
            ig = IngredientsDatabase().view_item(tig.itemcode)
            if wlproftype != ig.itemtype:
                raise ValueError(f"All Win Lose Profiles must be composed of only {wlproftype} type ingredients.  The following ingredient is not:\n{ig.itemdata}")
            igcodelist.append(tig.itemcode)
        print(f"All the ingredients passed the '{wlproftype}' type check.")
        igcodelist.sort()
        print(f"{self._item_term} data set to {igcodelist}.")
        return igcodelist

    def _set_itemcode(self):
        wlprofcode = ''.join(self.itemdata)
        itemcode = f'{Symbology().wlprofcode_pred}{self.periodlen}{wlprofcode}'
        print(f"Win Lose Profile code set to '{itemcode}'.")
        return itemcode

    @property
    def ingredientlist(self):
        return [IngredientsDatabase().view_item(i).itemdata for i in self.itemdata]
