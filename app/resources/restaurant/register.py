from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class RegisterRestaurantApi(Resource):
    @jwt_required()
    def post(self):
        try:
            current_manager_id = get_jwt_identity()
            managers = mongo.db.managers
            found_manager = managers.find_one({"_id": ObjectId(current_manager_id)})
            if found_manager:
                restaurants = mongo.db.restaurants
                body = request.get_json()
                name = body['name']
                area = body['area']
                address = ''
                service_areas = body['service_areas']
                work_hour = body['work_hour']
                deliver_cost = body['deliver_cost']
                foods = []
                restaurant_id = restaurants.insert({'name': name, 'area': area, 'address' : address,
                                                    'service_areas' : service_areas, 'work_hour' : work_hour,
                                                    'deliver_cost' : deliver_cost, 'foods' : foods})
                new_restaurant = restaurants.find_one({'_id': restaurant_id})
            else:
                raise UnauthorizedError
            return jsonify({'name':name,'area': area, 'address' : address, 'id': str(restaurant_id), 
                            'service_areas' : service_areas, 'work_hour' : work_hour, 'deliver_cost' : deliver_cost,
                            'foods': foods })

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

