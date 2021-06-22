from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class EditRestaurantApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            current_manager_id = get_jwt_identity()
            managers = mongo.db.managers
            found_manager = managers.find_one({"_id": ObjectId(current_manager_id)})
            if found_manager:
                restaurants = mongo.db.restaurants
                found_restaurant = restaurants.find_one({"_id":ObjectId(id)})
                if found_restaurant :
                    body = request.get_json()
                    name =  found_restaurant['name'] if body['name'] == "" else body['name']
                    area = found_restaurant['area'] if body['area'] == "" else body['area']
                    address = found_restaurant['address'] if body['address'] == "" else body['address']
                    service_areas = found_restaurant['service_areas'] if body['service_areas'] == "" else body['service_areas']
                    work_hour = found_restaurant['work_hour'] if body['work_hour'] == "" else body['work_hour']
                    deliver_cost = found_restaurant['deliver_cost'] if body['deliver_cost'] == "" else body['deliver_cost']
                    restaurant_id = restaurants.update({'_id': ObjectId(id)},
                                 {"$set": 
                                 {'name': name,
                                  'area': area,
                                  'address': address,
                                  'service_areas': service_areas,
                                  'work_hour': work_hour,
                                  'deliver_cost': deliver_cost }})

                    updated_restaurant = restaurants.find_one({'_id': ObjectId(id)})
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'name':updated_restaurant['name'],'area':updated_restaurant['area'], 'address' :updated_restaurant['address'], 
                            'service_areas' :updated_restaurant['service_areas'], 'work_hour' :updated_restaurant['work_hour'],
                            'deliver_cost' :updated_restaurant['deliver_cost'], 'foods':updated_restaurant['foods'], 'id': id})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError