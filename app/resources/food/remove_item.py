from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from database.models.food import Food
from resources.errors import UnauthorizedError, UserNotExistsError, SchemaValidationError


class RemoveFoodItemApi(Resource):
    @jwt_required()
    def delete(self, id):
        try:
            current_manager_id = get_jwt_identity()
            managers = mongo.db.managers
            found_manager = managers.find_one(
                {"_id": ObjectId(current_manager_id)})
            if found_manager:
                foods = mongo.db.foods
                restaurants = mongo.db.restaurants
                found_food = foods.find_one({"_id": ObjectId(id)})
                found_restaurant = restaurants.find_one({"_id": ObjectId(found_food['restaurant_id'])})
                if found_restaurant:
                    food = Food(record=found_food, id=id)
                    removed_food = foods.find_one_and_delete({'_id': ObjectId(id)})

                    updated_food = []
                    for f in found_restaurant['foods']:
                        if f['id'] != id:
                            food_record = Food(record=f, id=f['id'])
                            updated_food.append(food_record.to_json())
                    restaurants.update({'_id': ObjectId(ObjectId(found_food['restaurant_id']))},
                                       {"$set": {'foods': updated_food}})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'food': food.to_json()})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError
