import json
import cv2
import base64
from application.db import Session, Recipe, Ingredient, Link, Trunk

def migrate(path):
    recs = ""
    with open(path, encoding="utf-8") as file:
        recs = json.load(file)
    
    dbSession = Session()
    for key, value in recs.items():
        name=key
        resString=value[0]
        link=value[2]
        img=value[3].encode()

        r = Recipe(name=name, instructions=resString, url=link, img=img)
        for x, y in value[1].items():
            a = Link(ingredient_amount=y)
            a.ingredient = Ingredient(name=x)
            r.ingredient.append(a)
        dbSession.add(r)
        dbSession.commit()

migrate('./data/recs.json')
