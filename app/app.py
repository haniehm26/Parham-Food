from flask import Flask
from database.db import initialize_db

app = Flask(__name__)

# definition of database
app.config['MONGO_DBNAME'] = 'parham-food'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/parham-food'
initialize_db(app)