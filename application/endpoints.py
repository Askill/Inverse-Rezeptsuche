from flask_restful import Resource, reqparse
import flask
import requests
import application.config as config
import json
import base64
from application.db import Session, Recipe, Ingredient
import search
import migrate
import time

class RecipeList(Resource):
    def get(self):
        """  """
    
        parser = reqparse.RequestParser()
        parser.add_argument('ingred', type=str,  action='append')
        args = parser.parse_args()
        ingreds = args["ingred"]

        start = time.time()
        ingreds = [migrate.stemWord(ingred)[0] for ingred in ingreds + search.defaultArr] 
        end = time.time()
        print("stem", end - start, "\n")  


        start = time.time()
        indx = search.fastes(ingreds)
        end = time.time()
        print("get recipes",end - start, "\n")  

        start = time.time()
        recs = search.getRecDict(indx, ingreds)
        end = time.time()
        print("calc overlay",end - start, "\n")  
      

        return flask.make_response(flask.jsonify({'data': recs}), 200)


