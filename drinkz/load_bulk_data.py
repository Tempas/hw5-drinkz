"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#
import yaml
import csv                              # Python csv package
from . import db                        # import from local package
from . import recipes
import pprint

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = data_reader(fp)

    x = []
    n = 0
    for line in reader:
        try:        
           (mfg, name, typ) = line
        except:
            print "Line formatted incorrectly"
            continue
           
        n += 1
        try:
            db.add_bottle_type(mfg, name, typ)
        except:
            print "Could not add bottle type"
    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = data_reader(fp)

    x = []
    n = 0
    for line in reader:
        try:
            (mfg, name, amount) = line;
        except:
            print "Line formatted incorrectly"
            continue
        n += 1
        try:
            db.add_to_inventory(mfg, name, amount)
        except:
            print "Could not add to inventory"
    return n

def load_recipes(fp):
    """
    Loads in recipe data using yaml
    r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                                      '6 oz'),
                                                     ('vermouth',
                                                      '1.5 oz')])
    """
    n = 0
    # use safe_load instead load
    dataMap = yaml.safe_load(fp)
    recipeDict = dataMap["recipeDict"]
    for recipeName in recipeDict:
        ingredients = set()
        dictOfIngredients = recipeDict[recipeName]
        for ingredient in dictOfIngredients:
            myTup = (name,amount) = ingredient, dictOfIngredients[ingredient]
            ingredients.add(myTup); 
        try:
            r = recipes.Recipe(recipeName,ingredients)
            print ingredients
            db.add_recipe(r)
            n+=1
        except:
            print "Could not add to inventory"
    return n
def data_reader(fp):

    reader = csv.reader(fp)

    for line in reader:
        if not line:
            continue
        if not line[0].strip():
            continue
        if line[0].startswith('#'):
            continue
        yield line
