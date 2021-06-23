from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid, CursorNotFound, ConfigurationError
import datetime
from database.db import mongo
from bson.objectid import ObjectId
from database.hashing import hash_password, check_password
from resources.errors import EmailAlreadyExistsError, SchemaValidationError, UserNotExistsError, UnauthorizedError

class OrderStatusApi(Resource):
    def get(self, id):
        try:
            orders = mongo.db.orders
            found_order = orders.find_one({"_id": ObjectId(id)})
            if found_order:
               return jsonify({"status" : found_order['status']})
            else:
                raise CursorNotFound
                
        except CollectionInvalid:
            raise SchemaValidationError