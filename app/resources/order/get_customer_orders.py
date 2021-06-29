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
            restaurant = None
            if found_customer:
                orders = mongo.db.orders
                all_orders=[]
                for o in orders.find():
                    customer = o['customer']
                    if customer['first_name'] == found_customer['first_name']:
                        all_orders.append(o)
                        restaurant = o['restaurant']
            
            res_customer = {'first_name': found_customer['first_name'],
                            'last_name': found_customer['last_name'], 
                            'area': found_customer['area'], 
                            'address' : found_customer['address'],
                            'credit' : found_customer['credit'],
                            'orders_history' : [],
                            'favorits' : found_customer['favorits'],
                            'id': str(id)}
            res_restaurant = None
            if restaurant is not None:
                res_restaurant = {'name':restaurant['name'],'area':restaurant['area'], 'address' :restaurant['address'], 'id':str(restaurant['_id']), 
                    'service_areas' :restaurant['service_areas'], 'work_hour' :restaurant['work_hour'], 'deliver_cost' :restaurant['deliver_cost'],
                    'foods':restaurant['foods']}
            
            res_orders = []
            for order in all_orders:
                res_orders.append({
                    'id': str(order['_id']),
                    'foods': order['foods'],
                    'time': order['time'],
                    'restaurant' : res_restaurant, 
                    'status': order['status'],
                    'sender' : order['sender'],
                    'customer': res_customer,
                 })
            return jsonify({'orders': res_orders})

        except CollectionInvalid:
            raise SchemaValidationError

class AllOrdersApi(Resource):
    def get(self):
        try:
            orders = mongo.db.orders
            all_orders=[]
            restaurant = None
            customer = None
            for o in orders.find():
                all_orders.append(o)
                restaurant = o['restaurant']
                customer = o['customer']
            found_customer = customer
            res_customer = {'first_name': found_customer['first_name'],
                            'last_name': found_customer['last_name'], 
                            'area': found_customer['area'], 
                            'address' : found_customer['address'],
                            'credit' : found_customer['credit'],
                            'orders_history' : [],
                            'favorits' : found_customer['favorits'],
                            'id': str(found_customer['_id'])}
            res_restaurant = {'name':restaurant['name'],'area':restaurant['area'], 'address' :restaurant['address'], 'id':str(restaurant['_id']), 
                'service_areas' :restaurant['service_areas'], 'work_hour' :restaurant['work_hour'], 'deliver_cost' :restaurant['deliver_cost'],
                'foods':restaurant['foods']}
            
            res_orders = []
            for order in all_orders:
                res_orders.append({
                    'id': str(order['_id']),
                    'foods': order['foods'],
                    'time': order['time'],
                    'restaurant' : res_restaurant, 
                    'status': order['status'],
                    'sender' : order['sender'],
                    'customer': res_customer,
                 })
            return jsonify({'orders': res_orders})

        except CollectionInvalid:
            raise SchemaValidationError