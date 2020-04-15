
from application.db import Session, Recipe, Ingredient, Link, Trunk
import nltk as nltk
from nltk.corpus import stopwords
import time

dbSession = Session()
inputArr = ["butter", "milch", "eier", "käse"] 
maxMissing = 4

def slow():
    recipes = dbSession.query(Recipe).all()


    arr = {}
    for recipe in recipes:
        rec = recipe
        recipe = recipe.ingredients()
        if len(recipe) > len(inputArr) + maxMissing:
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
        
#    for y, x in arr.items():
#        for xx in x:
#            print(xx)

def faster():
    indx = {}
    for inpu in inputArr:
        ids = [] 
        for x in dbSession.query(Ingredient).filter(Ingredient.name.contains(inpu)).all():

            for y in x.recipe:
                
                if dbSession.query(Link).filter(Link.recipe_id==y.recipe_id).count() > len(inputArr) + maxMissing:
                    continue   
                if str(y.recipe_id) not in indx:
                    indx[str(y.recipe_id)] = 0

                indx[str(y.recipe_id)] += 1
        

    outDict = {}
    for key, value in indx.items():
        ingred = dbSession.query(Recipe).filter(Recipe.recipe_id==key).first().ingredients()
        outDict[calcOverlay(inputArr, ingred)] = (dbSession.query(Recipe).filter(Recipe.recipe_id==key).first().name, key, ingred)
    
    print(outDict)


def fastes():
    indx = {}
    inputArr2 = []

    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    for word in inputArr:

        if word in stopset:
             continue
        inputArr2.append(snowball.stem(word))

    for inpu in inputArr2:
        ids = [] 
        for xx in dbSession.query(Trunk).filter(Trunk.name == inpu).all():
            for x in dbSession.query(Ingredient).filter(xx.ingredient_id == Ingredient.ingredient_id).all():
                for y in x.recipe:
                    
                    if dbSession.query(Link).filter(Link.recipe_id==y.recipe_id).count() > len(inputArr) + maxMissing:
                        continue   
                    if str(y.recipe_id) not in indx:
                        indx[str(y.recipe_id)] = 0

                    indx[str(y.recipe_id)] += 1
        
    outDict = {}
    for key, value in indx.items():
        ingred = dbSession.query(Recipe).filter(Recipe.recipe_id==key).first().ingredients()
        outDict[calcOverlay(inputArr, ingred)] = (dbSession.query(Recipe).filter(Recipe.recipe_id==key).first().name, key, ingred)
    
    print(outDict)
#

def calcOverlay(l1, l2):
    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    stopset |= set("(),")

    l1 =  [snowball.stem(l) for l in l1 ]
    counter = 0

    for x in l2:
        for token in nltk.word_tokenize(x): 
            if token in stopset:
                continue
            stemmed = snowball.stem(token)
            for l in l1:
                if l == stemmed:
                    counter +=1
                     
    return counter
#


start = time.time()
slow()
end = time.time()
print("\n", end - start, "\n")  


start = time.time()
faster()  
end = time.time()
print("\n", end - start, "\n")  


start = time.time()
fastes()
end = time.time()
print("\n", end - start, "\n")  