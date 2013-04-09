#! /usr/bin/env python


import os
import drinkz.db
import drinkz.recipes
import sys
from drinkz.db import save_db, load_db


if __name__ == '__main__':
    args = sys.argv
    try:
        filename = args[1]
    except:
        filename = 'database'

    load_db('bin/'+filename)

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass


###

fp = open('html/index.html', 'w')
print >>fp, "<p><a href='recipes.html'>Recipes</a><p><a href='inventory.html'>Inventory</a> <p><a href='liquor_types.html'>Liquor Types</a>"



fp.close()

###

fp = open('html/recipes.html', 'w')

recipeList = drinkz.db.get_all_recipes()
print >> fp,"<ul>"
for recipe in recipeList:
    if recipe.need_ingredients():
        val = "no"
    else:
        val = "yes"
    print >> fp, "<li>"+recipe._recipeName + " " + val +"<p>"
print >> fp,"</ul>"
print >>fp, "<a href='index.html'>Home</a><p><a href='inventory.html'>Inventory</a> <p><a href='liquor_types.html'>Liquor Types</a>"

fp.close()

###

fp = open('html/inventory.html', 'w')
print >> fp,"<ul>"
for (m,l) in drinkz.db.get_liquor_inventory():
    print >> fp, "<li>" + str(m)+ " " + str(l)+ " "  + str(drinkz.db.get_liquor_amount(m,l))+" ml"+ "<p>"
print >> fp,"</ul>"

print >>fp, "<a href='index.html'>Home</a> <p><a href='recipes.html'>Recipes</a><p><a href='liquor_types.html'>Liquor Types</a>"

fp.close()

fp = open('html/liquor_types.html', 'w')
print >> fp,"<ul>"
for (m,l) in drinkz.db.get_liquor_inventory():
    print >> fp, "<li>" + str(m)+ " " + str(l) + "<p>"
print >> fp,"</ul>"
print >>fp, "<a href='index.html'>Home</a><p><a href='recipes.html'>Recipes</a><p><a href='inventory.html'>Inventory</a>"

fp.close()


