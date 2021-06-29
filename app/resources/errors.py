from flask import jsonify, request

class InternalServerError(Exception):
    status_code = 500
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['InternalServerError']


class SchemaValidationError(Exception):
    status_code = 400
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['SchemaValidationError']


class UserNotExistsError(Exception):
    status_code = 400
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['UserNotExistsError']

class UserWithMobileNotExistsError(Exception):
    status_code = 400
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['UserWithMobileNotExistsError']

class UnauthorizedError(Exception):
    status_code = 401
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['UnauthorizedError']


class EmailDoesNotExistsError(Exception):
    status_code = 400
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['EmailDoesNotExistsError']


class BadTokenError(Exception):
    status_code = 403
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['BadTokenError']


class ExpiredTokenError(Exception):
    status_code = 403
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['ExpiredTokenError']


class EmailAlreadyExistsError(Exception):
    status_code = 400
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['EmailAlreadyExistsError']

class PhoneNumberAlreadyExistsError(Exception):
    status_code = 400
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return errors['PhoneNumberAlreadyExistsError']


errors = {
    "InternalServerError": {
        "message": "خطایی رخ داده است",
        "status_code": 500
    },
    "SchemaValidationError": {
        "message": "همه فیلدهای لازم پر نشده‌اند",
        "status_code": 400
    },
    "UserNotExistsError": {
        "message": "کاربر با ایمیل و پسورد وارد شده وجود ندارد",
        "status_code": 400
    },
    "UserWithMobileNotExistsError": {
        "message": "کاربر با شماره موبایل و پسورد وارد شده وجود ندارد",
        "status_code": 400
    },
    "UnauthorizedError": {
        "message": "به این عملیات دسترسی ندارید",
        "status_code": 401
    },
    "EmailDoesNotExistsError": {
        "message": "کاربری با ایمیل وارد شده وجود ندارد",
        "status_code": 400
    },
    "BadTokenError": {
        "message": "توکن شما نامعتبر است",
        "status_code": 403
    },
    "ExpiredTokenError": {
        "message": "توکن شما منقضی شده است",
        "status_code": 403
    },
    "EmailAlreadyExistsError": {
        "message": "کاربر با این ایمیل قبلا ثبت نام کرده است",
        "status_code": 400
    },
    "PhoneNumberAlreadyExistsError": {
        "message": "کاربر با این موبایل قبلا ثبت نام کرده است",
        "status_code": 400
    }
}