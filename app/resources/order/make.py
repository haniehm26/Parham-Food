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
            status = ""
            sender = None

            final_cost = 0




            for food in foods:
                final_cost = final_cost + food['cost']

            customer_credit = found_customer['credit'] - final_cost - restaurant['deliver_cost']
            order_id = orders.insert({'foods': foods, 'time': time , 'restaurant' : restaurant,
                                    'customer': found_customer, 'status': status, 'sender': sender})

            new_order = orders.find_one({'_id': order_id})
           

        
            res_foods = []
            res_foods_names = []
            for f in foods:
                res_foods.append({'id':f['id'],'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'restaurant_id': f['restaurant_id'], 'number': f['number']-1})
                res_foods_names.append(f['name'])

            all_fooods = []
            for f in restaurant['foods']:
                if f['name'] in res_foods_names:
                    all_fooods.append(({'id':f['id'],'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'restaurant_id': f['restaurant_id'], 'number': f['number'] -1}))
                else:
                    all_fooods.append(({'id':f['id'],'name': f['name'], 'cost': f['cost'] , 'orderable' : f['orderable'], 'restaurant_id': f['restaurant_id'], 'number': f['number']}))

            
            res_restaurant = {'name':restaurant['name'],'area':restaurant['area'], 'address' :restaurant['address'], 'id':str(restaurant['_id']), 
                            'service_areas' :restaurant['service_areas'], 'work_hour' :restaurant['work_hour'], 'deliver_cost' :restaurant['deliver_cost'],
                            'foods':all_fooods}

            restaurants.update({'_id': ObjectId(foods[0]['restaurant_id'])},
                {"$set":
                    {'foods': all_fooods}
                })


            res_customer = {'first_name': found_customer['first_name'],
                            'last_name': found_customer['last_name'], 
                            'area': found_customer['area'], 
                            'address' : found_customer['address'],
                            'credit' : found_customer['credit'],
                            'orders_history' : [],
                            'favorits' : found_customer['favorits'],
                            'id': str(id)}

            order_history = found_customer['orders_history']

            order_history.append({'id': str(order_id), 'foods': foods, 'time': time, 'restaurant' : restaurant,
                                 'status': status, 'customer': res_customer, 'sender': sender})

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

            customer = customers.find_one({"_id": ObjectId(id)})

            res_customer = {'first_name': customer['first_name'],
                'last_name': customer['last_name'], 
                'area': customer['area'], 
                'address' : customer['address'],
                'credit' : customer['credit'],
                'orders_history' : [],
                'favorits' : customer['favorits'],
                'id': str(id)}

            # print(customer['id'])

            return jsonify({'id': str(order_id),'foods': res_foods, 'time': time , 'restaurant' : res_restaurant, 'customer': res_customer, 'status': status, 'sender' : sender})

        except CollectionInvalid:
            raise SchemaValidationError