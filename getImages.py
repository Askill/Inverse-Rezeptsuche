

from urllib.parse import urljoin
from lxml import html
import requests
import json
from time import sleep
import random
import traceback
import cv2
import base64
from application.db import Session, Recipe
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import cv2
from urllib.request import urlopen
import numpy as np

def getImages():
    chromePath = 'C:/tools/chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(chromePath, chrome_options=chrome_options)

    dbSession = Session()
    counter = 0
    maxC = dbSession.query(Recipe).count()
    for recipe in dbSession.query(Recipe).all():

        url = recipe.url
        string1 = '//*[@id="recipe-image-carousel"]/div/div[1]/div[9]/div/a/amp-img'

        driver.get(url)
        element = WebDriverWait(driver, 30).until(
                    ec.presence_of_element_located((
                    By.XPATH, string1)))

        
        src =  driver.find_element_by_xpath(string1).get_attribute("src")
        print(src)
        resp = urlopen(src)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        ret, jpeg = cv2.imencode(".jpg", image)
        img = base64.b64encode(jpeg)
        recipe.img = img
        dbSession.flush()
        dbSession.commit()
        counter +=1
        print(counter/maxC)
        sleep(5)

        

getImages()