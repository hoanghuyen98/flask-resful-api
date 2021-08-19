"""
Segment Image Service
"""
from src.service.auth_service import AuthService
try:
    from router_config import ROUTER_CONFIG
except ImportError:
    from src.controller.router_config import ROUTER_CONFIG


class AuthController:
    """
    Account Controller
    """

    def __init__(self, app, req):
        """
        init
        :param app: object Flask
        :return:
        """

        self.auth_service = AuthService
        self.logout(app, req)
        self.login(app, req)


    def login(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        auth_service = self.auth_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["auth"]["path_login"]), methods=['POST'])
        def login():
            """
            login
            """
            return auth_service.login_user(req)

    def logout(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        auth_service = self.auth_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["auth"]["path_logout"]), methods=['GET'])
        def logout():
            """
            logout
            """
            return auth_service.logout_user(req)
