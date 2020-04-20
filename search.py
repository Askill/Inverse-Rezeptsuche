
from application.db import Session, Recipe, Ingredient, Trunk
import nltk as nltk
from nltk.corpus import stopwords
import time
import heapq
from collections import Counter 

dbSession = Session()


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
    k = Counter(indx) 
    # Finding 1000 highest values 
    indx = k.most_common(1000)  
    indx = dict(indx)
    for key, value in indx.items():
        ingred = dbSession.query(Trunk.name).filter(Trunk.recipe_id==int(key)).all()
        outDict[calcOverlay(inputArr, ingred)] = int(key)
        
    outDict2 = {}
    for key in heapq.nlargest(10, outDict.keys()):
        key2 = outDict[key]
        rec = dbSession.query(Recipe).filter(Recipe.recipe_id==key2).first()
        outDict2[key] = (key2, rec.name, rec.url,  [r[0] + ": " + r[1] for r in dbSession.query(Ingredient.name, Ingredient.ingredient_amount).filter(Ingredient.recipe_id==key2).all()], rec.img.decode('utf-8'))
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