from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from config import db
from src.controller.router import Router

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost/db_cashier'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

migrate = Migrate(app, db)

jwt = JWTManager(app)

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo list api"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

with app.app_context():
    app.config['JSON_SORT_KEYS'] = False
    Router(app, request)

from src.models.user_model import UserModel
from src.models.transaction_model import TransactionModel
from src.models.blacklist import BlacklistToken

db.init_app(app)

if __name__ == '__main__':

    app.run()