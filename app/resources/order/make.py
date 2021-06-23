from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid
import datetime
from database.db import mongo
from bson.objectid import ObjectId
from database.hashing import hash_password, check_password
from resources.errors import EmailAlreadyExistsError, SchemaValidationError, UserNotExistsError, UnauthorizedError

class MakeOrderApi(Resource):
    def post(self, id):
        try:
            orders = mongo.db.orders
            customers = mongo.db.customers
            restaurants = mongo.db.restaurants

            body = request.get_json()
            foods = body['foods']
            time = datetime.datetime.now()
            found_customer = customers.find_one({"_id": ObjectId(id)})
            found_restaurant = restaurants.find_one({"_id": ObjectId(foods[0]['restaurant_id'])})
            restaurant = found_restaurant
            customer = found_customer
            status = ""

            final_cost = 0
            for food in foods:
                final_cost = final_cost + food['cost']

            customer_credit = found_customer['credit'] - final_cost

            order_id = orders.insert({'foods': foods, 'time': time , 'restaurant' : restaurant,
                                    'customer': customer, 'status': status})
            new_order = orders.find_one({'_id': order_id})

            order_history = []
            order_history.append(new_order)

            customers.update({'_id': ObjectId(id)},
                {"$set":
                    {'first_name': found_customer['first_name'],
                    'last_name': found_customer['last_name'], 
                    'area': found_customer['area'], 
                    'address' : found_customer['address'],
                    'credit' : customer_credit,
                    'orders_history' : order_history,
                    'favorits' : found_customer['favorits']
                    }
                })

            return jsonify({'id': str(order_id),'foods': foods, 'time': time , 'restaurant' : restaurant, 'customer': customer, 'status': status})

        except CollectionInvalid:
            raise SchemaValidationError