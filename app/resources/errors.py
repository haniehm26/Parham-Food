class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class UserNotExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class EmailDoesNotExistsError(Exception):
    pass


class BadTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UserNotExistsError": {
        "message": "User with given email doesn't exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid email or password",
        "status": 401
    },
    "EmailDoesNotExistsError": {
        "message": "Couldn't find the user with given email address",
        "status": 400
    },
    "BadTokenError": {
        "message": "Invalid token",
        "status": 403
    },
    "ExpiredTokenError": {
        "message": "Expired token",
        "status": 403
    },
    "EmailAlreadyExists": {
        "message": "Email already exists",
        "status": 400
    }
}