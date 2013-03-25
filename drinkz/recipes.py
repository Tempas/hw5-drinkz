import db


    
class Recipe(object):
    _recipeName = ""
    _myIngredients = set()
    def __init__(self, name, ingredientList):
        self._myIngredients = set()
        self._recipeName = name
        for ingredient in ingredientList:
            self._myIngredients.add(ingredient)

    def need_ingredients(self):
        myList = list()
        for currentIngredient in self._myIngredients:
            listOfMandLTuples = db.check_inventory_for_type(currentIngredient[0])

            amountInStock = 0
            for myTuple in listOfMandLTuples:
                val = db.get_liquor_amount(myTuple[0],myTuple[1])
                if val>amountInStock:
                    amountInStock = val
            amountInDebt = amountInStock - db.convert_to_ml(currentIngredient[1])
            
            if ( amountInDebt < 0 ):
                myList.append((currentIngredient[0],amountInDebt*-1.))
        return myList
                    
                


    def __eq__(self, other): 
        return self._recipeName == other._recipeName
            
        
