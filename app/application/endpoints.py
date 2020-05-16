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

        # get Input
        parser = reqparse.RequestParser()
        parser.add_argument('ingred', type=str,  action='append')
        args = parser.parse_args()
        ingreds = args["ingred"]

        # stem to find stems in db
        stemmed = [migrate.stem(ingred)[0] for ingred in ingreds] 

        start = time.time()
        # returns ids of found recipes
        indx = search.search2(stemmed)
        print("get recipes",time.time() - start, "\n")  

        # returns dict with recipes, keys are the % of overlaps with recipes as values
        recs = search.getRecDict2(indx, stemmed)
        # ignored saved only the indices, has to be matched to the input before it's returned
        recs["ignored"] = [ingreds[x] for x in recs["ignored"]]
        print("calc overlay", time.time() - start, "\n")  

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



