from flask import request, jsonify, Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from pymongo.errors import CollectionInvalid
import datetime
from database.db import mongo
from database.hashing import hash_password
# from database.models import Manager
from resources.errors import EmailAlreadyExistsError, SchemaValidationError

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
                access_token = create_access_token(identity=str(new_manager), expires_delta=expires)
            return jsonify({'token': access_token})

        except CollectionInvalid:
            raise SchemaValidationError

# class Alaki(Resource):
#     def get(self):
#         Manager({'email':'test@mail.com', 'password':'123456789'}).save()
#         m = Manager.objects.to_json()
#         return Response(m, mimetype="application/json", status=200)