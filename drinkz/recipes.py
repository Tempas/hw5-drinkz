import db

class Recipe(object):
    _recipeName = ""
    _myIngredients = set()
    def __init__(self, name, ingredientList):
        _recipeName = name
        for ingredient in ingredientList:
            _myIngredients.add(ingredient)

    def need_ingredients():
        myList = list()
        for currentIngredient in _myIngredients:
            setOfCertainType = check_inventory_for_type(currenIngredient[0])
            for value in setOfCertainType:
                totalAmountOfCertainType = get_liqour_amount(value[0],value[1])
                ingredientAmount = convert_to_ml(currentIngredient[1])
                if( ingredientAmount > totalAmountOfCertainType ):
                    myList.append((currentIngredient[0],ingredientAmount - totalAmountOfCertainType))
        return myList
                    
                

    def convert_to_ml(amount):
        amounts = amount.split(" ")
        total = 0
        if amounts[1] == "oz":
            total += float(amounts[0])*29.5735
        elif amounts[1] == "ml":
            total += float(amounts[0])
        elif amounts[1] == "gallon":
            total += float(amounts[0])*3785.41178
        return total

    def check_inventory_for_type(liqourType):
        mySet = set()
        for m, l in db.get_liquor_inventory():
            if liqourType == l:
                mySet.add((m,l))

        return mySet
            
            
        
