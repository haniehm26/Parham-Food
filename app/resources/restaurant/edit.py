from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError
from database.models.restaurant import Restaurant

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
                    name =  found_restaurant['name'] if body['name'] == None else body['name']
                    area = found_restaurant['area'] if body['area'] == None else body['area']
                    address = found_restaurant['address']
                    service_areas = found_restaurant['service_areas'] if body['service_areas'] == None else body['service_areas']
                    work_hour = found_restaurant['work_hour'] if body['work_hour'] == None else body['work_hour']
                    deliver_cost = found_restaurant['deliver_cost'] if body['deliver_cost'] == None else body['deliver_cost']
                    restaurant_id = restaurants.find_one_and_update({'_id': ObjectId(id)},
                                 {"$set": 
                                 {'name': name,
                                  'area': area,
                                  'address': address,
                                  'service_areas': service_areas,
                                  'work_hour': work_hour,
                                  'deliver_cost': deliver_cost }})
                    
                    restaurant = Restaurant(name=name, area=area, address=address,
                        service_areas=service_areas, work_hour=work_hour,
                        deliver_cost=deliver_cost, foods=found_restaurant['foods'], id=str(id))              
                else:
                    raise UnauthorizedError
            else:
                raise UnauthorizedError
            return jsonify({'restaurant' : restaurant.to_json})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError