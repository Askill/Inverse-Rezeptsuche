# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from lxml import html
import requests
import json
from time import sleep
import random
import traceback
import cv2
import base64
from application.db import Session, Recipe, Ingredient, Trunk
import nltk as nltk
from nltk.corpus import stopwords


header_values = {
    'name': 'Michael Foord',
    'location': 'Northampton',
    'language': 'English',
    'User-Agent': 'Mozilla 4/0',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
    'Upgrade-Insecure-Requests': '0',
    'Referrer': 'https://www.google.com/'
}

def getLinks():
    links = []
    with requests.Session() as session:
        root = "https://www.chefkoch.de/rs/s0/Rezepte.html"
        site = session.get(root,  headers=header_values)
        tree = html.fromstring(site.content)

        # converts: 344.621 Ergebnisse to int(344621)
        #max = int(tree.xpath(
        #    '/html/body/main/div[1]/h1/span/text()')[0].split(" ")[0].replace(".", ""))
        max = 2000 # get 2000 recepies :)
        for i in range(0, max, 30):
            try:
                root = "https://www.chefkoch.de/rs/s" + \
                    str(i) + "/Rezepte.html"
                site = session.get(root,  headers=header_values)
                tree = html.fromstring(site.content)

                # converts: 344.621 Ergebnisse to int(344621)
                max = int(tree.xpath(
                    '/html/body/main/div[1]/h1/span/text()')[0].split(" ")[0].replace(".", ""))
                # only add new links
                for x in tree.xpath('/html/body/main/article/a/@href'):
                    if x not in links:
                        links.append(x)
                print(i)

            except Exception as e:
                # retry after 3 seconds
                print(e)
                i -= 30
                sleep(10)

            sleep(random.randint(0, 5))

        print(links)
    return links

def getRecipe(links):
    recs = dict()
    with requests.Session() as session:
        counter = 0
        for link in links:
            counter += 1
            try:
                site = session.get(link,  headers=header_values)
                tree = html.fromstring(site.content)

                namePath = "/html/body/main/article[1]/div/div[2]/h1/text()"
                ingredPath = "/html/body/main/article[2]/table/tbody/tr/td" # TODO: fix this
                recipPath = "/html/body/main/article[3]/div[1]/text()"
                imgPath = './data/images.jpeg'

                name = tree.xpath(namePath)[0]
                ingred = tree.xpath(ingredPath)
                resip = tree.xpath(recipPath)

                image = cv2.imread(imgPath)
                ret, jpeg = cv2.imencode(".jpeg", image)
                img = base64.b64encode(jpeg)

                resString = ""
                for x in resip:
                    resString += x 

                dbSession = Session()
                
                r = Recipe(name=name, instructions=resString, url=link, img=img)
                
                ingredDict = {}
                for i in range(0, len(ingred)-1, 2):
                    #print(ingred[i+1][0].text)
                    if ingred[i+1][0] is not None:
                        if ingred[i+1][0].text is None:
                            textFromLink = ingred[i+1][0][0].text.strip().replace("  ", "")
                            #print(textFromLink)
                            stuff = textFromLink
                        else:
                            stuff = ingred[i+1][0].text.strip().replace("  ", "")

                    if ingred[i] is not None:
                        try:
                            amount = ingred[i][0].text.strip().replace("  ", "")
                        except:
                            amount = ""
                    #print(stuff, amount)
                    a = Link(ingredient_amount=amount)
                    a.ingredient = Ingredient(name=stuff)
                    r.ingredient.append(a)
                    dbSession.add(r)
                    dbSession.commit()
                    
                    ingredDict[stuff] = amount
                recs[name] = [resString, ingredDict, link, img.decode("utf-8")]
                print("")
            except Exception as e:
                print(traceback.format_exc())
                
            print(format(counter/len(links), '.2f'), link)
            sleep(random.randint(0, 5))
    return recs



def stemIngred():
    dbSession = Session()
    stopset = set(stopwords.words('german'))
    stopset |= set("(),")

    count = dbSession.query(Ingredient).count()
    for x in dbSession.query(Ingredient).all():
        snowball = nltk.SnowballStemmer(language='german')
        for token in nltk.word_tokenize(x.name): 
            if token in stopset or len(token) < 4:
                continue
            stemmed = snowball.stem(token)

            x.trunks.append(Trunk(name=stemmed))
            dbSession.commit()
        print(x.ingredient_id/count)

#links = getLinks()
#with open('./data/links.json', 'w') as file:
#    jsonString = json.dumps(links)
#    file.write(jsonString)
links = ""
with open('./data/links.json') as file:
    links = json.load(file)
    

#recs = getRecipe(links)
#stemIngred()

#with open('./data/recs.json', 'w', encoding="utf-8") as file:
#    json.dump(recs, file, ensure_ascii=False)
    