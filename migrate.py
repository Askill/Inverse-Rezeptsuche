import json
import cv2
import base64
import nltk as nltk
from nltk.corpus import stopwords
from application.db import Session, Recipe, Ingredient, Trunk

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

def migrate(path):
    recs = ""
    with open(path, encoding="utf-8") as file:
        recs = json.load(file)
    
    dbSession = Session()
    counter = 0
    leng = len(recs)
    for key, value in recs.items():
        name=key
        resString=value[0]
        link=value[2]
        img=value[3].encode()

        r = Recipe(name=name, instructions=resString, url=link, img=img)

        for x, y in value[1].items():
            a = Ingredient(name=x, ingredient_amount=y)
            r.ingredient.append(a)
            for x in stemWord(a.name):
                t = Trunk(name=x)
                r.trunk.append(t)
        dbSession.add(r)
        dbSession.commit()
        counter+=1
        print(counter/leng)

#migrate('./data/recs.json')
