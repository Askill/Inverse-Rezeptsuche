from flask_restful import Resource, reqparse
import flask
import requests
import application.config as config
import json
import base64
from application.db import Session, Recipe, Ingredient
import search
import migrate

class RecipeList(Resource):
    def get(self):
        """  """
    
        parser = reqparse.RequestParser()
        parser.add_argument('ingred', type=str,  action='append')
        args = parser.parse_args()
        ingreds = args["ingred"]
        ingreds = [migrate.stemWord(ingred)[0] for ingred in ingreds + search.defaultArr] 

        indx = search.fastes(ingreds )
        recs = search.getRecDict(indx, ingreds )
        
        #print(recs)

        return flask.make_response(flask.jsonify({'data': recs}), 200)


