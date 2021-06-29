from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from database.models.food import Food
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class EditFoodItemApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            current_manager_id = get_jwt_identity()
            managers = mongo.db.managers
            found_manager = managers.find_one({"_id": ObjectId(current_manager_id)})
            if found_manager:
                foods = mongo.db.foods
                restaurants = mongo.db.restaurants
                found_food = foods.find_one({"_id":ObjectId(id)})
                found_restaurant = restaurants.find_one({"_id":ObjectId(found_food['restaurant_id'])})
                if found_restaurant :
                    body = request.get_json()
                    name = found_food['name'] if body['name'] == None else body['name']
                    cost = found_food['cost'] if body['cost'] == None else body['cost']
                    orderable = found_food['orderable'] if body['orderable'] == None else body['orderable']
                    number = found_food['number'] if body['number'] == None else body['number']

                    updated_food = foods.find_one_and_update({'_id': ObjectId(id)},
                                 {"$set": 
                                 {'name': name,
                                  'cost': cost,
                                  'orderable': orderable,
                                  'number': number,
                                  'restaurant_id': found_food['restaurant_id']}})

                    food = Food(record=updated_food, id=id)

                    updated_food = []
                    for f in found_restaurant['foods']:
                        if f['id'] == id:
                            updated_food.append(food.to_json())
                        else:
                            food_record = Food(record=f, id=f['id'])
                            updated_food.append(food_record.to_json())
                    restaurants.update({'_id': ObjectId(ObjectId(found_food['restaurant_id']))},
                                 {"$set":{'foods': updated_food}})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'food':food.to_json()})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError
