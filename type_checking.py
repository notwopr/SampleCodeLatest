
class TypeChecker:
    type_glossary = {
        "string": str,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "float": float,
        "integer": int,
        "number": "custom",
        "str_or_num": "custom"
    }

    def _single_typecheck(self, inputobject, requiredtype):
        return 0 if type(inputobject) != self.type_glossary[requiredtype] else 1

    def is_valid(self, inputobject, requiredtype):
        if type(inputobject) == list:
            for item in inputobject:
                self.is_valid(item, requiredtype)
            return
        if not self.type_glossary.get(requiredtype, 0):
            raise ValueError(f"Data type {requiredtype} is not in the Type Glossary of TypeChecker class.")
        if requiredtype == "number":
            check = any([
                        self._single_typecheck(inputobject, "float"),
                        self._single_typecheck(inputobject, "integer")
                        ])
        elif requiredtype == "str_or_num":
            check = any([
                        self._single_typecheck(inputobject, "float"),
                        self._single_typecheck(inputobject, "integer"),
                        self._single_typecheck(inputobject, "string")
                        ])
        else:
            check = self._single_typecheck(inputobject, requiredtype)
        if not check:
            raise ValueError(f"{inputobject}'s data type is {type(inputobject)}.  It should be {requiredtype}.")

    def all_are_strings(self, inputlist, name):
        '''
        checks whether all elements of a given list are strings
        '''
        if all(map(lambda x: self.is_valid(x, "string"), inputlist)):
            print(f"Success! All items in list {name} are valid strings.")
