from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid
import datetime
from database.db import mongo
from database.hashing import hash_password, check_password
from resources.errors import PhoneNumberAlreadyExistsError, EmailAlreadyExistsError, SchemaValidationError, UserNotExistsError, UserWithMobileNotExistsError, UnauthorizedError

class CustomerSignupApi(Resource):
    def post(self):
        try:
            customers = mongo.db.customers
            body = request.get_json()
            customer_found = customers.find_one({'phone': body['phone']})
            if customer_found:
                raise PhoneNumberAlreadyExistsError
            else:
                password = hash_password(body['password'])
                first_name = ""
                last_name = ""
                area = ""
                address = ""
                credit = 1000000
                orders_history = []
                favorits = []
                customer_id = customers.insert({
                    'phone': body['phone'],
                    'password': password,
                    'first_name': first_name, 
                    'last_name':last_name, 
                    'area': area, 
                    'address' : address,
                    'credit' : credit,
                    'orders_history' : orders_history,
                    'favorits' : favorits})
                new_customer = customers.find_one({'_id': customer_id})
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=str(customer_id), expires_delta=expires)
            return {'token': access_token}, 200

        except CollectionInvalid:
            raise SchemaValidationError

class CustomerLoginApi(Resource):
    def post(self):
        try:
            customers = mongo.db.customers
            body = request.get_json()
            customer_found = customers.find_one({'phone': body['phone']})
            if not customer_found:
                raise UserWithMobileNotExistsError
            else:
                authorized = check_password(customer_found['password'], body['password'])
                if not authorized:
                    raise UserWithMobileNotExistsError
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=str(customer_found['_id']), expires_delta=expires)
            return {'token': access_token}, 200

        except CollectionInvalid:
            raise SchemaValidationError