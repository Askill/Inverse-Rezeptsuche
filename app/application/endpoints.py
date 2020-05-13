from flask_restful import Resource, reqparse
import flask
from flask import g
import requests
import application.config as config
import json
import base64
from application.db2 import Session, Recipe
import application.search as search
import background.migrate as migrate
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

        ingreds = [migrate.stem(ingred)[0] for ingred in ingreds] 

        start = time.time()
        indx = search.search2(ingreds)
        end = time.time()
        print("get recipes",end - start, "\n")  

        recs = search.getRecDict2(indx, ingreds)
        end = time.time()
        print("calc overlay",end - start, "\n")  

        g.session.close()
        return flask.make_response(flask.jsonify({'data': recs}), 200)

class Images(Resource):
    def get(self, id = None):
        if id is None:
            flask.make_response(flask.jsonify({'error': "No ID supplied"}), 401)
        
        session = Session()
        image = session.query(Recipe.img).filter(Recipe.recipe_id == id).first()[0]
        image = base64.b64decode(image)
        session.close()
        return flask.Response(image,  mimetype='image/png')



