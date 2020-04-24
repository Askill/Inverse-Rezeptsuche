import json
import cv2
import base64
import nltk as nltk
from nltk.corpus import stopwords
#import db as db1
#import db2 as db2

def stemWord(word):
    try:
        arr = []
        stopset = set(stopwords.words('german'))
        stopset |= set("(),")
        snowball = nltk.SnowballStemmer(language='german')
        for token in nltk.word_tokenize(word): 
            if token in stopset or len(token) < 4:
                continue
            stemmed = snowball.stem(token)
            arr.append(stemmed)
        if len(arr) == 0:
            arr.append("")
        return arr
    except:
        return [""]

#migrate('./data/recs.json')

def migrateRecsDb1ToDb2():

    session1 = db1.Session()
    session2 = db2.Session()
 

    count = 0
    length = session1.query(db1.Recipe).count()
    for r1 in list(session1.query(db1.Recipe).all())[int(length/2):]:
        try:
            if not bool(session2.query(db2.Recipe).filter(db2.Recipe.name == r1.name).first()):
                r2 = db2.Recipe(name=r1.name, instructions=r1.instructions, url=r1.url, img=r1.img)
                
                for ingred in r1.ingredient:
                    ri2 = db2.RecIngred()
                    ingredient2 = session2.query(db2.Ingredient).filter(db2.Ingredient.name == ingred.name).first()
                    if ingredient2 is None:
                        ingredient2 = db2.Ingredient(name=ingred.name)
                    ri2.ingredient_amount = ingred.ingredient_amount
                    ri2.ingredient = ingredient2
                    r2.ingredient.append(ri2)
                
                session2.add(r2)
                session2.commit()
            
        except:
            session1 = db1.Session()
            session2 = db2.Session()

        count+=1
        print(count/length)

def TrunkDb2():
    session2 = db2.Session()
 
    count = 0
    length = session2.query(db2.Ingredient).count()
    for i2 in session2.query(db2.Ingredient).all():
        try:
            for trunk1 in stem(i2.name):

                ri2 = db2.IngredTrunk()
                trunk = session2.query(db2.Trunk).filter(db2.Trunk.name == trunk1).first()
                if trunk is None:
                    trunk = db2.Trunk(name=trunk1)
                
                if session2.query(db2.IngredTrunk).filter(db2.IngredTrunk.ingredient_name == i2.name, db2.IngredTrunk.trunk_name == trunk1).first() is None:
                    ri2.trunk = trunk
                    i2.trunks.append(ri2)
            
                session2.commit()
            
        except Exception as e:
            print(e)
            session2 = db2.Session()

        count+=1
        print(count/length)


def stem(l1):
    '''Tokenize and stem word, result is 1d list'''
    snowball = nltk.SnowballStemmer(language='german')
    stopset = set(stopwords.words('german'))
    stopset |= set("(),")
    l2 = []

    for token in nltk.word_tokenize(l1): 
        token = snowball.stem(token)
        if token in stopset or not token.isalpha() or len(token) < 2:
            continue
        l2.append(token)

    return l2
#migrateDb1ToDb2()
#TrunkDb2()