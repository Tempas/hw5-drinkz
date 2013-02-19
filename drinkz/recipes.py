class Recipe(object):
    _recipeName = ""
    _myIngredients = set()
    def __init__(self, name, ingredientList):
        _recipeName = name
        for ingredient in ingredientList:
            _myIngredients.add(ingredient)
        

    
            
            
        
