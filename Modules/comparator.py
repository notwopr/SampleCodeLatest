import operator


class Comparator:

    def is_valid(self, targetvalue, comparevalue, comparetype):
        if comparetype == "<":
            return operator.__lt__(targetvalue, comparevalue)
        if comparetype == "<=":
            return operator.__le__(targetvalue, comparevalue)
        if comparetype == ">":
            return operator.__gt__(targetvalue, comparevalue)
        if comparetype == ">=":
            return operator.__ge__(targetvalue, comparevalue)
