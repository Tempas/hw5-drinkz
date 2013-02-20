#! /usr/bin/env python


import os
import drinkz.db
import drinkz.recipes


drinkz.db._reset_db()

drinkz.db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
drinkz.db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

drinkz.db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
drinkz.db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

drinkz.db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
drinkz.db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

drinkz.db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
drinkz.db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

r = drinkz.recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
drinkz.db.add_recipe(r)
r = drinkz.recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
drinkz.db.add_recipe(r)
r = drinkz.recipes.Recipe('vomit inducing martini', [('orange juice',
                                              '6 oz'),
                                             ('vermouth',
                                              '1.5 oz')])

drinkz.db.add_recipe(r)

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
