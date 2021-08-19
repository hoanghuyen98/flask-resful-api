import datetime

import flask_bcrypt
import jwt

from config import db, key, ma
from src.models.blacklist import BlacklistToken


class UserModel(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))
    currency_yen = db.Column(db.Float(precision=2), default=0.0)
    currency_baht = db.Column(db.Float(precision=2), default=0.0)
    currency_dong = db.Column(db.Float(precision=2), default=0.0)
    transactions = db.relationship('TransactionModel', backref='user', lazy=True)

    def password(password):
        return flask_bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def check_password(self, password_hash, password):
        return flask_bcrypt.check_password_hash(password_hash, password)

    @classmethod
    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

    def find_by_email(self, email):
        return self.query.filter_by(email=email).first()

    @classmethod
    def add_user(self, data):
        try:
            user = UserModel(email=data['email'], password_hash=self.password(data['password']))
            db.session.add(user)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
            }
            return response_object, 201
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Add user Fail: {}'.format(ex),
            }
            return response_object, 409


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
            return "<User '{}'>".format(self.email)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password_hash')
