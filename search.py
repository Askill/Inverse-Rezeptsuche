
from application.db import Session, Recipe, Ingredient, Trunk
import nltk as nltk
from nltk.corpus import stopwords
import time
import heapq

dbSession = Session()

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

def getRecDict(indx, inputArr):
    #inputArr = stem(inputArr)
    outDict = {}
    for key, value in indx.items():
        ingred = dbSession.query(Trunk.name).filter(Trunk.recipe_id==int(key)).all()
        outDict[calcOverlay(inputArr, ingred)] = int(key)
        
    outDict2 = {}
    for key in heapq.nlargest(10, outDict.keys()):
        key2 = outDict[key]
        outDict2[key] = (dbSession.query(Recipe).filter(Recipe.recipe_id==key2).first().name, key2, dbSession.query(Ingredient.name).filter(Ingredient.recipe_id==key2).all())
    return outDict2

def printDict(indx, inputArr):
    outDict = getRecDict(indx, inputArr)
    for key, value in sorted(outDict.items()):
        if key >= 0.3:
           
            print(key, value[0], value[1])
            for xx in value[2]:
                print("\t", xx[0])
    

def stem(l1):
    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    stopset |= set("(),")

    l1 =  [snowball.stem(l) for l in l1]
    return l1

def calcOverlay(l1, l2):
    counter = 0

    for x in l2:
        for l in l1:
            if l not in defaultArr and l == x[0]:
                #print(l)
                counter +=1
    counter = counter / len(l2)                 
    return counter


#inputArr = ["reis", "tofu", "bohnen", "kichererbsen", "hackfleisch"]
defaultArr = ["Wasser", "salz", "pfeffer"] # it is assumed that everyone has this
#inputArr += defaultArr
maxMissing = 10
#
#stemmed = stemInput(inputArr)
#
#start = time.time()
#indx = faster(stemmed)  
#end = time.time()
#printDict(indx)
#print("\n", end - start, "\n")  
#
#
#start = time.time()
#indx = fastes(stemmed)
#end = time.time()
#printDict(indx)
#print("\n", end - start, "\n")  