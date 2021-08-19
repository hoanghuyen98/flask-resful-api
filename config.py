import os
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False

key = Config.SECRET_KEY
db = SQLAlchemy()
ma = Marshmallow()
