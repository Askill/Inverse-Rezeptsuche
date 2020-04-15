
from application.db import Session, Recipe, Ingredient, Trunk
import nltk as nltk
from nltk.corpus import stopwords
import time

dbSession = Session()
inputArr = ["butter", "milch", "eier", "mehl", "zucker"] 
maxMissing = 10

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

def faster(inputArr):
    indx = {}
 

    for inpu in inputArr:
        ids = [] 
        for x in dbSession.query(Trunk.recipe_id).filter(Trunk.name.contains(inpu)).all():
            if str(x[0]) not in indx:
                indx[str(x[0])] = 0

            indx[str(x[0])] += 1
        

    return(indx)

def fastes(inputArr):
    indx = {}

    for inpu in inputArr:
        ids = [] 
        for recipe_id in dbSession.query(Trunk.recipe_id).filter(Trunk.name == inpu).all():
                

            if str(recipe_id[0]) not in indx:
                indx[str(recipe_id[0])] = 0

            indx[str(recipe_id[0])] += 1
    return(indx) 
    
def stemInput(inputArr):
    inputArr2 = []

    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    for word in inputArr:

        if word in stopset:
             continue
        inputArr2.append(snowball.stem(word))

    return inputArr2
#
def printDict(indx):
    outDict = {}
    for key, value in sorted(indx.items()):
        ingred = dbSession.query(Trunk.name).filter(Trunk.recipe_id==int(key)).all()
        outDict[calcOverlay(inputArr, ingred)] = (dbSession.query(Recipe).filter(Recipe.recipe_id==key).first().name, key, dbSession.query(Ingredient.name).filter(Ingredient.recipe_id==key).all())
    
    for key, value in outDict.items():
        if key >= 0.5:
            print(key, value)
    

def calcOverlay(l1, l2):
    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    stopset |= set("(),")

    l1 =  [snowball.stem(l) for l in l1 ]
    counter = 0

    for x in l2:
        for l in l1:
            if l == x[0]:
                #print(l)
                counter +=1
    counter = counter / len(l2)                 
    return counter
#


start = time.time()
#slow()
end = time.time()
print("\n", end - start, "\n")  

stemmed = stemInput(inputArr)

start = time.time()
indx = faster(stemmed)  
end = time.time()
printDict(indx)
print("\n", end - start, "\n")  


start = time.time()
indx = fastes(stemmed)
end = time.time()
printDict(indx)
print("\n", end - start, "\n")  