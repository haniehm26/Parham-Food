from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class EditProfileApi(Resource):
    @jwt_required()
    def put(self):
        try:
            current_customer_id = get_jwt_identity()
            customers = mongo.db.customers
            found_customer = customers.find_one({"_id": ObjectId(current_customer_id)})
            if found_customer:
                body = request.get_json()
                first_name = body['first_name']
                last_name = body['last_name']
                area = body['area']
                address = ''
                credit = body['credit']
                orders_history = []
                favorits = []
                customer_id = customers.update({'_id': ObjectId(current_customer_id)},
                {"$set":
                    {'first_name': first_name, 
                    'last_name':last_name, 
                    'area': area, 
                    'address' : address,
                    'credit' : credit,
                    'orders_history' : orders_history,
                    'favorits' : favorits}
                })
                new_customer = customers.find_one({'_id': current_customer_id})
            else:
                raise UnauthorizedError
            return jsonify({'first_name': first_name, 'last_name':last_name, 'area': area, 'address' : address,
                            'credit' : credit, 'orders_history' : orders_history, 'favorits' : favorits, 'id' : str(current_customer_id)})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

class GetProfileApi(Resource):
    @jwt_required()
    def get(self):
        try:
            current_customer_id = get_jwt_identity()
            customers = mongo.db.customers
            found_customer = customers.find_one({"_id": ObjectId(current_customer_id)})
            if found_customer:
                print(found_customer)
                first_name = found_customer['first_name']
                last_name = found_customer['last_name']
                area = found_customer['area']
                address = found_customer['address']
                credit = found_customer['credit']
                orders_history = found_customer['orders_history']
                favorits = found_customer['favorits']
            else:
                raise UnauthorizedError
            return jsonify({'first_name': first_name, 'last_name':last_name, 'area': area, 'address' : address,
                            'credit' : credit, 'orders_history' : [], 'favorits' : favorits, 'id' : str(current_customer_id)})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError