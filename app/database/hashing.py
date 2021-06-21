from flask_bcrypt import generate_password_hash, check_password_hash


# this method is used to hash the given password
def hash_password(password):
    return generate_password_hash(password).decode('utf8')


# this method is used to check real password and hashed password
def check_password(self, password):
    return check_password_hash(self, password)