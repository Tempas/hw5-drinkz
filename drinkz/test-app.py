"""
Test the app.py file 
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded;
import os

import db
import recipes
import app
import urllib

def initialize_db():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vodka martini', [('unflavored vodka', '7 oz'),('vermouth', '1.5 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                              '6 oz'),
                                             ('vermouth',
                                              '1.5 oz')])
    db.add_recipe(r)


def test_check_generated_page():
    
    initialize_db()
   
    myApp = app.SimpleApp()

    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(firstname='FOO',
                                                    lastname='BAR'))
    environ['PATH_INFO'] = '/recipesList'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    results = myApp.__call__(environ,my_start_response)

    text = "".join(results)
    
    assert text.find("vodka martini") != -1, text
    assert text.find("scotch on the rocks") != -1, text
    assert text.find("vomit inducing martini") != -1, text


#HW 5 tests start here
def test_check_recipe_possible():
    
    initialize_db()
   
    myApp = app.SimpleApp()

    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(firstname='FOO',
                                                    lastname='BAR'))
    environ['PATH_INFO'] = '/recipesList'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h
    results = myApp.__call__(environ,my_start_response)

    text = "".join(results)
    
    assert text.find("vodka martini no") != -1, text
    assert text.find("scotch on the rocks yes") != -1, text
    assert text.find("vomit inducing martini no") != -1, text



