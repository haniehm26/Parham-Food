from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid
import datetime
from database.db import mongo
from bson.objectid import ObjectId
from database.hashing import hash_password, check_password
from resources.errors import EmailAlreadyExistsError, SchemaValidationError, UserNotExistsError, UnauthorizedError

class EditOrderApi(Resource):
    def put(self, id): # order id
        try:
            orders = mongo.db.orders
            # customers = mongo.db.customers
            # restaurants = mongo.db.restaurants

            body = request.get_json()
            found_order = orders.find_one({"_id": ObjectId(id)})

            orders.update({'_id': ObjectId(id)},
                {"$set":
                {'foods': found_order['foods'],
                'time': found_order['time'] ,
                'restaurant' : found_order['restaurant'],
                'customer': found_order['customer'],
                'status': body['status'],
                'sender': body['sender'] if body['sender'] is not None else found_order['sender']
                }
                })

            customer = found_order['customer']

            res_customer = {'first_name': customer['first_name'],
                'last_name': customer['last_name'], 
                'area': customer['area'], 
                'address' : customer['address'],
                'credit' : customer['credit'],
                'orders_history' : [],
                'favorits' : customer['favorits'],
                'id': str(customer['_id'])}

            restaurant = found_order['restaurant']

            res_restaurant = {'name':restaurant['name'],'area':restaurant['area'], 'address' :restaurant['address'], 'id':str(restaurant['_id']), 
                'service_areas' :restaurant['service_areas'], 'work_hour' :restaurant['work_hour'], 'deliver_cost' :restaurant['deliver_cost'],
                'foods':restaurant['foods']}
            
            updated_order = orders.find_one({"_id": ObjectId(id)})
            return jsonify({'id': str(id),'foods':found_order['foods'],
                            'time':found_order['time'] , 
                            'restaurant' :res_restaurant,
                            'customer':res_customer,
                             'status':body['status'],
                            'sender' :body['sender'] if body['sender'] is not None else found_order['sender']})

        except CollectionInvalid:
            raise SchemaValidationError