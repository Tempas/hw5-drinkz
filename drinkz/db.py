"""
Database functionality for drinkz information.
"""
import drinkz.recipes
# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = set()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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
    total = 0.0
    amounts = amount.split(" ")
    if amounts[1] == "oz":
        total += float(amounts[0])*29.5735
    elif amounts[1] == "ml":
        total += float(amounts[0])
    elif amounts[1] == "gallon":
        total += float(amounts[0])*3785.41178
        
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
    found = false
    for recipe in _recipes_db:
        if(r[0] == recipe[0]):
            found = true
    if found == false:
        _recipes_db.add(r)
    
def get_recipe(name):
    for recipe in _recipes_db:
        if name == recipe._name:
            return recipe
    return null

def get_all_recipes():
    return _recipes_db
    
