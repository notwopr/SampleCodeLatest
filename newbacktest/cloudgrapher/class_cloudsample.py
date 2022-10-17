from newbacktest.abstractclasses.class_abstract_dbitem import AbstractDatabaseItem


class CloudSample(AbstractDatabaseItem):
    '''
    A StageRecipe is a collection of ingredients.  It doesn't actually store the ingredient data, but rather a list of their corresponding codes.  When it comes time to actually use the recipe, the codes are used to search the Ingredients Database for the actual ingredient data.
    itemdata = {
            0: <sampcode>,
            1: <sampcode>,
            ...
            <period_num>: <sampcode>,
        }
    '''
    _item_term = "Cloud Sample"

    def __init__(self, itemdata, cloudsampcode, nickname=None, description=None):
        self._nickname = nickname
        self._description = description
        self._itemdata = self._set_itemdata(itemdata)
        self._itemcode = self._set_itemcode(cloudsampcode)
        self._creationdate = self._set_creationdate()

    def _set_itemdata(self, itemdata):
        print(f"{self._item_term} data set to {itemdata}.")
        return itemdata

    def _set_itemtype(self):
        pass

    def _set_itemcode(self, cloudsampcode):
        print(f"{self._item_term} code set to '{cloudsampcode}'.")
        return cloudsampcode
