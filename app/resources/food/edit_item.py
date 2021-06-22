from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class EditFoodItemApi(Resource):
    @jwt_required()
    def delete(self, r_id, f_id):
        try:
            current_manager_id = get_jwt_identity()
            managers = mongo.db.managers
            found_manager = managers.find_one({"_id": ObjectId(current_manager_id)})
            if found_manager:
                restaurants = mongo.db.restaurants
                found_restaurant = restaurants.find_one({"_id":ObjectId(r_id)})
                if found_restaurant :
                    foods = mongo.db.foods
                    foods.delete_one({'_id': ObjectId(f_id)})

                    updated_food = []
                    for f in found_restaurant['foods']:
                        if f['food_id'] == f_id:
                            found_restaurant['foods'].remove({'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'food_id': f_id})
                        else:
                            updated_food.append({'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'food_id': f['food_id']})
                    restaurants.update({'_id': ObjectId(r_id)},
                                 {"$set":{'foods': updated_food}})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'id': f_id, 'restaurant_id': r_id})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

