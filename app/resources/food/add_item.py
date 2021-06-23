from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class AddFoodItemApi(Resource):
    @jwt_required()
    def post(self, id):
        try:
            current_manager_id = get_jwt_identity()
            managers = mongo.db.managers
            found_manager = managers.find_one({"_id": ObjectId(current_manager_id)})
            if found_manager:
                restaurants = mongo.db.restaurants
                found_restaurant = restaurants.find_one({"_id":ObjectId(id)})
                if found_restaurant :
                    foods = mongo.db.foods
                    body = request.get_json()
                    name = body['name']
                    cost = body['cost']
                    orderable = False
                    number = 0
                    
                    food_id = foods.insert({'name': name, 'cost': cost , 'orderable' : orderable, 'restaurant_id': id, 'number': number})
                    new_food = foods.find_one({'_id': food_id})

                    updated_food = []
                    for f in found_restaurant['foods']:
                        updated_food.append({'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'id': f['id'], 'number': f['number']})
                    updated_food.append({'name': name, 'cost': cost , 'orderable' : orderable, 'id': str(food_id), 'number': number})

                    restaurants.update({'_id': ObjectId(id)},
                                 {"$set":{'foods': updated_food}})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'id': str(food_id),'name': name, 'cost': cost , 'orderable' : orderable, 'restaurant_id': id, 'number': number})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

