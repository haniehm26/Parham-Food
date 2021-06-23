from flask import jsonify, request
from flask_restful import Resource
from bson.objectid import ObjectId

from database.db import mongo

class SearchApi(Resource):
    def get(self):
        restaurant_id = request.args.get('restaurant') # id
        area_name = request.args.get('area') # name
        food_name = request.args.get('food') # name

        restaurants = mongo.db.restaurants
        all_restaurants = []
        if isinstance(restaurant_id, ObjectId):
            found_restaurant = restaurants.find_one({"_id":ObjectId(restaurant_id)})
            if found_restaurant:
                all_restaurants.append(found_restaurant)
            else:
                for r in restaurants.find():
                    all_restaurants.append({'name':r['name'],'area': r['area'], 'address' : r['address'], 
                                'service_areas' : r['service_areas'], 'work_hour' : r['work_hour'],
                                'deliver_cost' : r['deliver_cost'], 'foods':r['foods'], 'id': str(r['_id'])})
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
                if r['area'] == area_name:
                    filer_restaurant_area.append(r)

        all_foods = []
        for r in filer_restaurant_area:
            for f in r['foods']:
                all_foods.append(f)
        
        search_result = []
        if food_name == "":
            search_result = all_foods
        else:
            for f in all_foods:
                if f['name'] == food_name:
                    search_result.append(f)
        
        return jsonify({"foods" : search_result})