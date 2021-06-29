from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid
import datetime
from bson.objectid import ObjectId
from database.db import mongo
from database.hashing import hash_password, check_password
from resources.errors import EmailAlreadyExistsError, SchemaValidationError, UserNotExistsError, UnauthorizedError

class CustomerOrdersApi(Resource):
    def get(self, id):
        try:
            customers = mongo.db.customers
            found_customer = customers.find_one({"_id": ObjectId(id)})
            if found_customer:
                orders = mongo.db.orders
                all_orders=[]
                for o in orders.find():
                    customer = o['customer']
                    if customer['name'] == found_customer['name']:
                        all_orders.append(o)
            return jsonify({'orders': all_orders})

        except CollectionInvalid:
            raise SchemaValidationError

class AllOrdersApi(Resource):
    def get(self, id):
        try:
            orders = mongo.db.orders
            all_orders=[]
            for o in orders.find():
                all_orders.append(o)
            return jsonify({'orders': all_orders})

        except CollectionInvalid:
            raise SchemaValidationError