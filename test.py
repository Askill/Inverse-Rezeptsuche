
from application.db import Session, Recipe, Ingredient, Link

dbSession = Session()
inputArr = ["kartoffeln", "zwiebel", "steak", "würfel"] 

def slow():
    recipes = dbSession.query(Recipe).all()


    arr = {}
    for recipe in recipes:
        rec = recipe
        recipe = recipe.ingredients()
        if len(recipe) > len(inputArr) + 2:
            continue
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
        

    print(arr)

def faster():
    indx = {}
    for inpu in inputArr:
        ids = [] 
        for x in dbSession.query(Ingredient).filter(Ingredient.name.contains(inpu)).all():

            for y in x.recipe:
                
                if dbSession.query(Link).filter(Link.recipe_id==y.recipe_id).count() > len(inputArr) + 5:
                    continue   
                if str(y.recipe_id) not in indx:
                    indx[str(y.recipe_id)] = 0

                indx[str(y.recipe_id)] += 1
        

    for key, value in indx.items():
        if value >= len(inputArr):


            print(dbSession.query(Recipe).filter(Recipe.recipe_id==key).first().ingredients())
            #print(key)
faster()    
slow()