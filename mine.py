
from urllib.parse import urljoin
from lxml import html
import requests
import json
from time import sleep
import random

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
        for link in links:
            try:
                site = session.get(link,  headers=header_values)
                tree = html.fromstring(site.content)

                namePath = "/html/body/main/article[1]/div/div[2]/h1/text()"
                ingredPath = "/html/body/main/article[2]/table/tbody/tr/td/span/text()" # TODO: fix this
                recipPath = "/html/body/main/article[3]/div[1]/text()"

                name = tree.xpath(namePath)[0]
                ingred = tree.xpath(ingredPath)
                resip = tree.xpath(recipPath)
                resString = ""
                for x in resip:
                    resString += x + "\n\n"

                ingredDict = dict()
                for i in range(0, len(ingred)-1, 2):
                    ingredDict[ingred[i+1]] = ingred[i] 
                recs[name] = [resString, ingredDict]

                print("")
            except Exception as e:
                print(e)
                sleep(10)

            sleep(random.randint(0, 5))

#links = getLinks()
#with open('./data/links.json', 'w') as file:
#    jsonString = json.dumps(links)
#    file.write(jsonString)
with open('./data/links.json') as file:
    links = json.load(file)
    
    getRecipe(links)

