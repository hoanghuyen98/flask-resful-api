"""
module Router for endpoint
"""
from .user_controller import UserController
from .transaction_controller import TransactionController
from .auth_controller import AuthController

class Router:
    """
     init route for all resource
     @param {*} app
    """

    def __init__(self, app, request):
        self.user_controller = UserController(app, request)
        self.transaction_controller = TransactionController(app, request)
        self.auth_controller = AuthController(app, request)