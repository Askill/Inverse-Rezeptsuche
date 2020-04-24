from flask_restful import Resource, reqparse
import flask
from flask import g
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
        g.session = Session()
        g.session = Session()
        parser = reqparse.RequestParser()
        parser.add_argument('ingred', type=str,  action='append')
        args = parser.parse_args()
        ingreds = args["ingred"]

        ingreds = [migrate.stem(ingred)[0] for ingred in ingreds + search.defaultArr] 

        start = time.time()
        indx = search.search2(ingreds)
        end = time.time()
        print("get recipes",end - start, "\n")  

        start = time.time()
        recs = search.getRecDict(indx, ingreds)
        end = time.time()
        print("calc overlay",end - start, "\n")  

        g.session.commit()
        g.session.close()
        return flask.make_response(flask.jsonify({'data': recs}), 200)



