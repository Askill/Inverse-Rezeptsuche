from flask_restful import Resource, reqparse
import flask
import requests
import application.config as config
import json
import base64
from application.db import Session, Recipe, Ingredient

class Recipe(Resource):
    def get(self):
        """  """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('useFace', type=bool, required=False)
            args = parser.parse_args()

            session = Session()

            return flask.make_response(flask.jsonify({'data': args}), 200)
        except Exception as e:
            print("error: -", e)
            return flask.make_response(flask.jsonify({'error': str(e)}), 400)

