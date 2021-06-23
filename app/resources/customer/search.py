from flask import jsonify
from flask_restful import Resource

from database.db import mongo

class SearchApi(Resource):
    def get(self, tag):
        restaurants = mongo.db.restaurants
        foods_names = []
        areas = []
        restaurants_names = []
        for r in restaurants.find():
            areas.append(r['area'])
            restaurants_names.append(r['name'])
            foods = r['foods']
            for f in foods:
                foods_names.append(f['name'])
        if tag == 'food':
            return jsonify({'foods': foods_names})
        elif tag == 'restaurant':
            return jsonify({'restaurants': restaurants_names})
        elif tag == 'area':
            return jsonify({'areas': areas})