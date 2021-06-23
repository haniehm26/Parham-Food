from bson.objectid import ObjectId
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError

from database.db import mongo
from resources.errors import UnauthorizedError, UserNotExistsError ,SchemaValidationError

class EditProfileApi(Resource):
    @jwt_required()
    def post(self):
        try:
            current_customer_id = get_jwt_identity()
            customers = mongo.db.customers
            found_customer = customers.find_one({"_id": ObjectId(current_customer_id)})
            if found_customer:
                body = request.get_json()
                first_name = body['first_name']
                last_name = body['last_name']
                area = body['area']
                address = body['address']
                credit = 1000000
                orders_history = []
                favorits = []
                customer_id = customers.insert({'first_name': first_name, 'last_name':last_name, 'area': area, 'address' : address,
                                                    'credit' : credit, 'orders_history' : orders_history, 'favorits' : favorits})
                new_customer = customers.find_one({'_id': customer_id})
            else:
                raise UnauthorizedError
            return jsonify({'first_name': first_name, 'last_name':last_name, 'area': area, 'address' : address,
                            'credit' : credit, 'orders_history' : orders_history, 'favorits' : favorits, 'id' : str(customer_id)})

        except CollectionInvalid or ConfigurationError:
            raise SchemaValidationError
        except CursorNotFound:
            raise UserNotExistsError

