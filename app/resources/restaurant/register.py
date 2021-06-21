from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UserNotExistsError, SchemaValidationError

class RegisterRestaurant(Resource):
    # @jwt_required
    def post(self):
        try:
            # current_manager_email = get_jwt_identity()
            # managers = mongo.db.managers
            # found_manager = managers.find_one({'email': current_user_email})
            # if found_manager:
            restaurants = mongo.db.restaurants
            body = request.get_json()
            name = body['name']
            area = body['area']
            address = body['address']
            service_areas = body['service_areas']
            work_hour = body['work_hour']
            deliver_cost = body['deliver_cost']
            restaurant_id = restaurants.insert({'name': name, 'area': area, 'address' : address,
                                                'service_areas' : service_areas, 'work_hour' : work_hour,
                                                'deliver_cost' : deliver_cost})
            new_restaurant = restaurants.find_one({'_id': restaurant_id})
            # else:
                # raise UserNotExistsError
            return jsonify("done")

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError