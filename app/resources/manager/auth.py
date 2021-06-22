from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid
import datetime
from database.db import mongo
from database.hashing import hash_password, check_password
from resources.errors import EmailAlreadyExistsError, SchemaValidationError, UserNotExistsError, UnauthorizedError

class SignupApi(Resource):
    def post(self):
        try:
            managers = mongo.db.managers
            body = request.get_json()
            manager_found = managers.find_one({'email': body['email']})
            if manager_found:
                raise EmailAlreadyExistsError
            else:
                password = hash_password(body['password'])
                manager_id = managers.insert({'email': body['email'], 'password': password})
                new_manager = managers.find_one({'_id': manager_id})
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=str(manager_id), expires_delta=expires)
            return {'token': access_token}, 200

        except CollectionInvalid:
            raise SchemaValidationError

class LoginApi(Resource):
    def post(self):
        try:
            managers = mongo.db.managers
            body = request.get_json()
            manager_found = managers.find_one({'email': body['email']})
            if not manager_found:
                raise UserNotExistsError
            else:
                authorized = check_password(manager_found['password'], body['password'])
                if not authorized:
                    raise UnauthorizedError
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=str(manager_found['_id']), expires_delta=expires)
            return {'token': access_token}, 200

        except CollectionInvalid:
            raise SchemaValidationError