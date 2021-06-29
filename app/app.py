from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from flask import request, jsonify
from resources.errors import errors
from resources.errors import InternalServerError, SchemaValidationError, UserNotExistsError, UserWithMobileNotExistsError, UnauthorizedError, EmailDoesNotExistsError, BadTokenError, ExpiredTokenError, EmailAlreadyExistsError, PhoneNumberAlreadyExistsError
def email_already_exists_error(e):
    return jsonify(e.to_dict())
from database.db import initialize_db

app = Flask(__name__)

# for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
# (Use this when calling APIs from front-end browser)
CORS(app)

# Windows: Type in this command in 'cmd', before running the project
# $ set ENV_FILE_LOCATION=./.env
# 'ENV_FILE_LOCATION' stands for the relative location of '.env' file in Server directory
app.config.from_envvar('ENV_FILE_LOCATION')

# because of circular import it is imported here.
# do not change it.
from resources.routes import initialize_routes

# some errors are defined in app/resources/error.py, set here
api = Api(app, errors=errors)

# this is used to generate hashed passwords
bcrypt = Bcrypt(app)

# this is used for generate user token
jwt = JWTManager(app)

# definition of database
app.config['MONGO_DBNAME'] = 'parham-food'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/parham-food'

initialize_db(app)

# initialize api routes
initialize_routes(api)

@app.errorhandler(InternalServerError)
def internal_server_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(SchemaValidationError)
def schema_validation_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(UserNotExistsError)
def user_not_exists_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(UserWithMobileNotExistsError)
def user_with_mobile_not_exists_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(UnauthorizedError)
def unauthorized_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(EmailDoesNotExistsError)
def email_does_not_exists_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(BadTokenError)
def bad_token_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(ExpiredTokenError)
def expired_token_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(EmailAlreadyExistsError)
def email_already_exists_error(e):
    return jsonify(e.to_dict())

@app.errorhandler(PhoneNumberAlreadyExistsError)
def phone_number_already_exists_error(e):
    return jsonify(e.to_dict())

