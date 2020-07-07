
import application.db2 as db
from flask import g
import nltk as nltk
from nltk.corpus import stopwords
import time
import heapq
from collections import Counter
import background.migrate
from sqlalchemy import exists

def search2(inputArr):
    ''' returns inputs with array of recipeID which use them  '''
    indx = {}
    dbSession = db.Session()
    for inpu in inputArr:
        x = dbSession.query(db.Trunk.name, db.Recipe.recipe_id).filter(db.Trunk.name == inpu).join(db.IngredTrunk).join(
            db.Ingredient).join(db.RecIngred).join(db.Recipe).all()

        indx[inpu] = [str(y[1]) for y in x]

    return(indx)

def stemInput(l1):
    ''' returns array of stemmed input '''
    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    stopset |= set("(),")
    l1 = [snowball.stem(l) for l in l1]
    return l1


def findUnrecognized(dbSession, inputArr):
    ''' check if any input is not in db.Trunk'''
    ignored = []
    for x in inputArr:
        if not dbSession.query(exists().where(db.Trunk.name == x)).scalar():
            ignored.append(inputArr.index(x))
    return ignored

def getIngredDict(ingred):
    ''' RezeptID, stemmed Ingred, full ingred Name
     Dict spiegelt DB wieder, key, full ingred, stemmed
     this structure makes calcOverlay() more efficient '''
    
    ingredDict = {}
    for k, v, i in ingred:
        if k not in ingredDict:
            ingredDict[k] = {}
        if i not in ingredDict[k]:
            ingredDict[k][i] = []
        ingredDict[k][i].append(v)
    return ingredDict

def calcOverlay(inputArr, ingredDict):
    '''checks overlay per recipeID 
    iterate over ingreds and checks per stemmed ingred
    returns accurate percentage of overlay
    since overlay scare is the key of dict it is reduced by insignificant number to preserve all values'''

    outDict = {}
    for key, value in ingredDict.items():
        overlay, missing = calcOverlay2(inputArr, value)
        while overlay in outDict.keys():
            overlay -= 0.0001
        outDict[overlay] = (int(key), missing)
    return outDict

def resolvRecipe(dbSession, outDict):
    ''' return Dict with 20 highest value keys
     creates dict which is returned'''

    outDict2 = {}
    for key in heapq.nlargest(20, outDict.keys()):
        key2 = outDict[key][0]
        missing = outDict[key][1]
        rec = dbSession.query(db.Recipe).filter(
            db.Recipe.recipe_id == key2).first()
        outDict2[key] = (key2, rec.name, rec.url,  [r[0] + ": " + r[1] for r in dbSession.query(db.Ingredient.name,
                                                                                                db.RecIngred.ingredient_amount).join(db.RecIngred).join(db.Recipe).filter(db.Recipe.recipe_id == key2).all()], missing)
    return outDict2

def getRecDict2(indx, inputArr):
    '''returns dict with percentage of overlay as keys and recipes as values'''
    dbSession = db.Session()
   
    # 2d to 1d
    indx = sum(indx.values(), [])
    k = Counter(indx)
    # keep 1000 most relevant to have consistent query time
    indx = k.most_common(1000)
    indx = dict(indx)

    # get ingredients for all recipes
    ingred = [x for x in dbSession.query(db.Recipe.recipe_id, db.IngredTrunk.trunk_name, db.IngredTrunk.ingredient_name).filter(
        db.Recipe.recipe_id.in_(indx.keys())).join(db.RecIngred).join(db.Ingredient).join(db.IngredTrunk).all()]
    
    ingredDict = getIngredDict(ingred)
    ignored = findUnrecognized(dbSession, inputArr)
    inputArr += stemInput(defaultArr)
    outDict = calcOverlay(inputArr, ingredDict)
    ingreds = resolvRecipe(dbSession, outDict)

    outDict = {}
    outDict["ignored"] = ignored
    outDict["ingred"] = ingreds
    return outDict

def calcOverlay2(l1, l2):
    '''Calculates overlay and returns missing ingredients, [score (float), missing([])]'''
    counter = 0
    notIn = []
    for key, ll in l2.items():
        missing = True
        for l in ll:
            if l in l1:
                counter += 1
                missing = False
                break
        if missing:
            notIn.append(key)

    counter = counter / len(l2)
    return counter, notIn


# it is assumed that everyone has this
defaultArr = ["wasser", "salz", "pfeffer"]
