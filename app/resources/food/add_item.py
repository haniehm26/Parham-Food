from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class AddFoodItemApi(Resource):
    @jwt_required()
    def post(self):
        try:
            current_manager_id = get_jwt_identity()
            managers = mongo.db.managers
            found_manager = managers.find_one({"_id": ObjectId(current_manager_id)})
            if found_manager:
                restaurants = mongo.db.restaurants
                found_restaurant = restaurants.find_one({"id":current_manager_id})
                if found_restaurant :
                    foods = mongo.db.foods
                    body = request.get_json()
                    name = body['name']
                    cost = body['cost']
                    id = found_restaurant['_id']
                    menu = {'name': name, 'cost': cost}
                    food_id = foods.insert(menu)
                    new_food = foods.find_one({'_id': food_id})
                    updated_menu = found_restaurant['menu'].append(menu)
                    restaurants.update({'id': current_manager_id},
                                 {"$set":{'menu': updated_menu}})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify(str(new_food))

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

