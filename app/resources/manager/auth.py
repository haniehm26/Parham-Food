from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid
import datetime
from database.db import mongo
from database.hashing import hash_password, check_password
from resources.errors import EmailAlreadyExistsError, SchemaValidationError, UserNotExistsError, UnauthorizedError
from database.models.manager import Manager

class ManagerSignupApi(Resource):
    def post(self):
        try:
            managers = mongo.db.managers
            body = request.get_json()
            email = body['email']
            password = hash_password(body['password'])
            manager_found = managers.find_one({'email': email})
            if manager_found:
                raise EmailAlreadyExistsError
            else:
                manager_id = managers.insert({'email': email, 'password': password})
                manager = Manager(email, password, str(manager_id))
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=manager.id, expires_delta=expires)
            return {'token': access_token}, 200

        except CollectionInvalid:
            raise SchemaValidationError

class ManagerLoginApi(Resource):
    def post(self):
        try:
            managers = mongo.db.managers
            body = request.get_json()
            email = body['email']
            password = body['password']
            manager_found = managers.find_one({'email': email})
            if not manager_found:
                raise UserNotExistsError
            else:
                manager = Manager(manager_found['email'], manager_found['password'], str(manager_found['_id']))
                authorized = check_password(manager.password, password)
                if not authorized:
                    raise UnauthorizedError
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=str(manager.id), expires_delta=expires)
            return {'token': access_token}, 200

        except CollectionInvalid:
            raise SchemaValidationError