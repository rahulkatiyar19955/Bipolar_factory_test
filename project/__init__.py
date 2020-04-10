from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import datetime

'''initializing application object'''
app = Flask(__name__)


'''app configuration'''
app.config['SECRET_KEY'] = 'THISISHIDDEN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)

'''initializing database object'''
db = SQLAlchemy(app)

'''initializing jwt object'''
jwt_obj = JWTManager(app)

'''routes import'''
from project.routes import Routes