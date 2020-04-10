
from application.db import Session, Recipe, Ingredient, Link

dbSession = Session()
inputArr = ["wasser", "MEHL", "zucker", "zitrone", "stift"] 

def slow():
    recipes = dbSession.query(Recipe).all()


    arr = {}
    for recipe in recipes:
        rec = recipe
        recipe = recipe.ingredients()
        counter = 0
        for i in inputArr:
            for x in recipe:
                if i in x:
                    counter += 1
                    continue
        counter = str(counter)

        if counter not in arr:
            arr[counter] = []
            
            arr[counter].append(rec.ingredients())
        #print(rec.name)
        

    print(arr['5'])

def faster():
    indx = {}
    for inpu in inputArr:
        ids = [] 
        for x in dbSession.query(Ingredient).filter(Ingredient.name.contains(inpu)).all():
            for y in x.recipe:
                ids.append(y.recipe_id)
        
        for i in ids:
            if str(i) not in indx:
                indx[str(i)] = 0

            indx[str(i)] += 1
        

    for key, value in indx.items():
        if value >= len(inputArr):


            print(dbSession.query(Recipe).filter(Recipe.recipe_id==key).first().ingredients())
            #print(key)
faster()    
