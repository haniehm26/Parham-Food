from flask import jsonify, request
from flask_restful import Resource
from bson.objectid import ObjectId

from database.db import mongo

class SearchApi(Resource):
    def get(self):
        restaurant_name = request.args.get('restaurant') # name
        area_name = request.args.get('area') # name
        food_name = request.args.get('food') # name

        restaurants = mongo.db.restaurants
        all_restaurants = []
        found_restaurant = restaurants.find_one({"name" : restaurant_name})
        if found_restaurant:
            all_restaurants.append(found_restaurant)
        else:
            for r in restaurants.find():
                all_restaurants.append({'name':r['name'],'area': r['area'], 'address' : r['address'], 
                            'service_areas' : r['service_areas'], 'work_hour' : r['work_hour'],
                            'deliver_cost' : r['deliver_cost'], 'foods':r['foods'], 'id': str(r['_id'])})
        
        filer_restaurant_area = []
        if area_name == "":
            filer_restaurant_area = all_restaurants
        else:
            for r in all_restaurants:
                if area_name in r['area']:
                    filer_restaurant_area.append(r)

        all_foods = []
        for r in filer_restaurant_area:
            for f in r['foods']:
                if f['orderable'] == True and f['number'] > 0:
                    all_foods.append(f)
        search_result = []
        if food_name == "":
            search_result = all_foods
        else:
            for f in all_foods:
                if food_name in f['name']:
                    search_result.append(f)
        
        return jsonify({"foods" : search_result})