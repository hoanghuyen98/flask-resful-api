"""
Account service
"""
import json
from src.models.user_model import UserModel
from src.service.blacklist_service import save_token


class AuthService:
    """
    Account service
    """

    def login_user(req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        # try:
        user = UserModel.query.filter_by(email=data['email']).first()
        if user and user.check_password(user.password_hash, data['password']):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'Authorization': auth_token.decode()
                }
                return response_object, 200
        else:
            response_object = {
            'status': 'fail',
            'message': 'email or password not exist.'
            }
        return response_object, 401
        # except Exception as e:
        #     response_object = {
        #         'status': 'fail',
        #         'message': 'Try again'
        #     }
        #     return response_object, 500

    def logout_user(req):
        auth_token = req.headers.get('Authorization')
        if auth_token:
            resp = UserModel.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = UserModel.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = UserModel.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401


