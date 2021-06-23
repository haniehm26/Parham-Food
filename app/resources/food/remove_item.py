from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class RemoveFoodItemApi(Resource):
    @jwt_required()
    def delete(self, id):
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
                    foods.delete_one({'_id': ObjectId(id)})

                    updated_food = []
                    for f in found_restaurant['foods']:
                        if f['food_id'] == id:
                            found_restaurant['foods'].remove({'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'food_id': id})
                        else:
                            updated_food.append({'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'food_id': f['food_id']})
                    restaurants.update({'_id': ObjectId(ObjectId(found_food['restaurant_id']))},
                                 {"$set":{'foods': updated_food}})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'id': id, 'restaurant_id': found_food['restaurant_id'], 'name':found_food['name'], 'cost':found_food['cost'], 'orderable':found_food['orderable']})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

