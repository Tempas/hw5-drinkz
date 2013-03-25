"""
Database functionality for drinkz information.
"""

import recipes


from cPickle import dump, load


# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = set()

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
class DuplicateRecipeName(Exception):
    pass
def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    total = convert_to_ml(amount)
        
    if (mfg,liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] += total
    else:
        _inventory_db[(mfg, liquor)] = total

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    total = 0
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            total = float(str(_inventory_db[(m,l)]))

    return float("%.2f" % total)

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l

def add_recipe(r):
    found = False
    for recipe in _recipes_db:
        if recipe._recipeName == r._recipeName:
            raise DuplicateRecipeName
    _recipes_db.add(r)
    
def get_recipe(name):
    for recipe in _recipes_db:
        if name == recipe._recipeName:            
            return recipe
    return 0

def get_all_recipes():
    return _recipes_db

def check_inventory_for_type(typ):
    myList = list()
    
    for (m, l, t) in _bottle_types_db:

        if(typ == t or typ == l): #checks for generic or label
            myList.append((m,l))
    return myList



def convert_to_ml(amount):
    amounts = amount.split(" ")
    total = 0
    if amounts[1] == "oz":
        total += float(amounts[0])*29.5735
    elif amounts[1] == "ml":
        total += float(amounts[0])
    elif amounts[1] == "liter":
        total += float(amounts[0])*1000.0
    elif amounts[1] == "gallon":
        total += float(amounts[0])*3785.41178
    return total      
