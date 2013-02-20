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
            amountInDebt = amountInStock - self.convert_to_ml(currentIngredient[1])
            
            if ( amountInDebt < 0 ):
                myList.append((currentIngredient[0],amountInDebt*-1.))
        return myList
                    
                

    def convert_to_ml(self,amount):
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


        return mySet

    def __eq__(self, other): 
        return self._recipeName == other._recipeName
            
        
