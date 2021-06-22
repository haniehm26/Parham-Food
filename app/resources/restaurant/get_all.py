from flask import jsonify
from flask_restful import Resource

from database.db import mongo

class AllRestaurantsApi(Resource):
    def get(self):
        restaurants = mongo.db.restaurants
        output = []
        for r in restaurants.find():
            output.append({'name':r['name'],'area': r['area'], 'address' : r['address'], 
                            'service_areas' : r['service_areas'], 'work_hour' : r['work_hour'],
                            'deliver_cost' : r['deliver_cost'], 'menu':r['menu']})
        return jsonify({'restaurants': output})