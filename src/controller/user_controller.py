"""
Segment Image Service
"""

from ..service.user_service import UserService


try:
    from router_config import ROUTER_CONFIG
except ImportError:
    from src.controller.router_config import ROUTER_CONFIG


class UserController:
    """
    Account Controller
    """

    def __init__(self, app, req):
        """
        init
        :param app: object Flask
        :return:
        """
        self.user_service = UserService()
        self.addUser(app, req)

    def addUser(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        user_service = self.user_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["user"]["path_add_user"]), methods=['POST'])
        def addUser():
            """
            add account
            """
            return user_service.register(req)


