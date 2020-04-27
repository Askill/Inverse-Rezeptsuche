
import application.db2 as db
from flask import g
import nltk as nltk
from nltk.corpus import stopwords
import time
import heapq
from collections import Counter
import background.migrate

def search2(inputArr):
    indx = {}
    dbSession = db.Session()
    for inpu in inputArr:
        x = dbSession.query(db.Trunk.name, db.Recipe.recipe_id).filter(db.Trunk.name == inpu).join(db.IngredTrunk).join(
            db.Ingredient).join(db.RecIngred).join(db.Recipe).all()

        indx[inpu] = [str(y[1]) for y in x]

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

def getRecDict2(indx, inputArr):
    dbSession = db.Session()

    outDict = {}
    # 2d to 1d
    indx = sum(indx.values(), [])
    k = Counter(indx)
    indx = k.most_common(1000)
    indx = dict(indx)

    ingred = [x for x in dbSession.query(db.Recipe.recipe_id, db.IngredTrunk.trunk_name, db.IngredTrunk.ingredient_name ).filter(db.Recipe.recipe_id.in_(indx.keys())).join(db.RecIngred).join(db.Ingredient).join(db.IngredTrunk).all()]
    ingredDict = {}
    for k,v, i in ingred:
        if k not in ingredDict:
            ingredDict[k] = {}
        if i not in ingredDict[k]:
            ingredDict[k][i] = []

        ingredDict[k][i].append(v)
    inputArr += defaultArr
    for key, value in ingredDict.items():
        overlay = calcOverlay2(inputArr, value)
        while overlay in outDict.keys():
            overlay -= 0.0001
        outDict[overlay] = int(key)

    outDict2 = {}
    for key in heapq.nlargest(20, outDict.keys()):
        key2 = outDict[key]
        rec = dbSession.query(db.Recipe).filter(db.Recipe.recipe_id == key2).first()
        outDict2[key] = (key2, rec.name, rec.url,  [r[0] + ": " + r[1] for r in dbSession.query(db.Ingredient.name,
                                                                                                db.RecIngred.ingredient_amount).join(db.RecIngred).join(db.Recipe).filter(db.Recipe.recipe_id == key2).all()])
    return outDict2

def stem(l1):
    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    stopset |= set("(),")
    l1 = [snowball.stem(l) for l in l1]
    return l1

def calcOverlay2(l1, l2):
    counter = 0
    for ll in l2.values():
        for l in ll:
            if l in l1:
                counter += 1
                break

    counter = counter / len(l2)
    return counter

# it is assumed that everyone has this
defaultArr = ["Wasser", "salz", "pfeffer"]

