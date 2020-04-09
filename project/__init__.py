from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import datetime

'''initializing objects'''
app = Flask(__name__)
db = SQLAlchemy(app)
jwt_obj = JWTManager(app)

'''app configuration'''
app.config['SECRET_KEY'] = 'THISISHIDDEN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=1)

'''route import'''
from project.routes import Routes