from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from database.models.food import Food
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
                    number = body['number']
                    
                    food_id = foods.insert({'name': name, 'cost': cost , 'orderable' : orderable, 'restaurant_id': id, 'number': number})
                    food = Food(record=foods.find_one({'_id': food_id}), id=food_id)

                    updated_food = []
                    for f in found_restaurant['foods']:
                        food_record = Food(record=f, id=f['id'])
                        updated_food.append(food_record.to_json())
                                             
                    updated_food.append(food.to_json())

                    restaurants.update({'_id': ObjectId(id)},
                                 {"$set":{'foods': updated_food}})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'food' : food.to_json()})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

