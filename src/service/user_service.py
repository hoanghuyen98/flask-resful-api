"""
Account service
"""
import json

from ..Const import check_email, check_pwd
from ..models.user_model import UserModel
from src.service.blacklist_service import save_token


class UserService:
    """
    Account service
    """

    def __init__(self):
        self.user_model = UserModel()

    def register(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """

        if req.method == "POST":
            data = json.loads(req.data)
            email = data['email']
            pwd = data['password']

            if check_email(email) == None:
                response_object = {
                    'status': 'fail',
                    'message': 'Invalid Email',
                }
                return response_object, 409

            if check_pwd(pwd) == None:
                response_object = {
                    'status': 'fail',
                    'message': 'Password must contain at least eight characters, at least one number and both lower and uppercase letters and special characters.',
                }
                return response_object, 409

            user = self.user_model.find_by_email(email)
            if not user:
                result = self.user_model.add_user(data)
                return result
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return response_object, 409

    def login_user(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        user = self.user_model.find_by_email(data["email"])
        if user and user.check_password2(data('password')):
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
                    'message': 'email or password does not match.'
                }
                return response_object, 401
        return "fail"

    def logout_user(self, req):
        data = json.loads(req.data)
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = self.user_model.decode_auth_token(auth_token)
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
