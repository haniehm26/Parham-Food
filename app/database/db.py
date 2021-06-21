from flask_pymongo import PyMongo
# from flask_mongoengine import MongoEngine

mongo = PyMongo()
# mongo = MongoEngine()

def initialize_db(app):
    mongo.init_app(app)